'''
# 기존 fixed-size 청킹 
  - [v] fixed-size 단위 청킹 처리하는 모듈 
  - 최대 길이는 700 설정 (글자 수), 토큰 최대는 1024이므로, 범위 안에 여유있게 들어옴 
  - 청킹의 trade-off 
    - chunk가 작으면 -> 검색 정밀도 상승 -> 문맥이 잘릴 수 있음 
    - chunk가 크면 -> 문맥 보전 상승 -> 불필요한 내용이 같이 포함될 수 있음 
  - 청크 사이즈는 rag 성능의 하이퍼 파라미터 -> 검색 평가를 통해서 최적 크기는 결정 
  - 고정 크기 -> overlap -> token 기반 -> 시맨틱/구조 기반 청킹 or 청킹 에이전트 개발 반영

# 시맨틱 청킹 
  - 말뭉치 -> 문장/문단 단위로 분절
'''

# 정규식 
import re

# 긴 문장(말뭉치)을 문장 단위로 분리
def _splite_sentencess(block: str) -> list[str]: 
  # 1. 좌우 공백 제거
  block = block.strip() 

# 시맨틱에 맞게 데이터 담는 작업
# 문단 = 문장 + 문장 + ... 
def _semantic_units(text: str) -> list[str]: 
  # 1. 문단의 끝 단위를 1차로 쪼개기 -> r"\n\s*\n" 
  blocks = [
    # 문단을 리스트의 멤버로 구성
    block.strip() 
    # 말뭉치에서 문단의 구분값 기준 쪼개기 -> 반복 
    for block in re.split(r"\n\s*\n" , text)
    # 문단의 내용이 비어있으면 배제 
    if block.strip()
  ]
  print( len(blocks), blocks )

  # 2. 청킹 단위 데이터를 담는 그릇 
  units: list[str] = list()

  # 3. 문단 단위로 순회 -> 1차적으로 청킹 진행 (최소 글자수 단위 나름 구성 -> 350(설정값) 기준)
  for block in blocks: 
    if len(block) <= 350:
      units.append()
    else: 
      # 350 글자수보다 많은 글자수를 가진 문단을 좀 더 쪼개기 위해서 _splite_sentencess()에 전달
      units.append(
        _splite_sentencess( block )  
      )

  return units

# 시맨틱 청킹 함수 
# 원문, 임계값(0.6 이하면 청킹), 최소 글자수, 최대 글자수(유사도가 계속 0.6 이상이어도 최대 글자수가 1200 넘어가면 청킹)
def semantic_splite_text( text:str, threshold: float=0.60, min_chars:int = 300, max_chars: int = 1200 ) -> list[str]:
  # 1. semantic 유닛 단위 분할
  units = _semantic_units( text )
  
  _splite_sentencess( text )
  
  return []




def splite_text(text: str, max_chars:int = 700):
  # 청크별로 모으는 그룻, 현재 순서상 문서 데이터 
  chunks, current_doc = [], ""
  # \n\n를 기준으로 분할 -> 문서마다 상이함 
  # print( text.split('\n\n') ) 
  paragraphs = [ p.strip() for p in text.split('\n\n') if p.strip() ] # 공백 제거 처리, 노이즈 제거

  # 순회하면서 청킹 처리
  for p in paragraphs: 
    # 1. 청킹 후보 (현재 보관 문서 + 줄 바꿈 + 하나씩 뽑아낸 문단)
    candidate_doc = (current_doc + "\n\n" + p).strip()

    # 2. 청킹 후보에 대한 길이 체크 (청킹의 분할 기준이 문자 수 = 700)
    if current_doc and len(candidate_doc) > max_chars: 
      # 3. 청크에 추가 -> 청크 1개 확정 
      chunks.append( current_doc ) # 현재 누적된 doc에 새로운 문단 추가하면 700을 넘어간다 -> 새로 추가분 제외 
      # 4. 리셋 
      current_doc = p 
    else: 
      # 현재 보관 문서에 후보군 문서를 설정
      current_doc = candidate_doc

  # 마지막까지 다 체크를 했는데, 마지막에서 700이 안 넘었다 -> 남은 문단이 존재함 
  if current_doc: 
    chunks.append( current_doc )

  # 청크 묶음 반환
  return chunks