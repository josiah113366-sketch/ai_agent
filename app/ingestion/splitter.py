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
from app.embedding import get_embeddings
import math
# Vector 타입 힌트 
from typing import Sequence

# 350 글자수(설정값) 이상을 가진 문단을 재료로 쪼개기 진행
def _splite_sentencess(block: str) -> list[str]: 
  # 1. 좌우 공백 제거
  block = block.strip() 
  # 2. 값 체크
  if not block: return []
  # 3. 줄 단위로 분절 -> 제목/목록 등등 문서 형식에 따라서는 의미가 있음 
  print( "block.splitlines() : ", block.splitlines() )
  lines = [
    line.strip()
    for line in block.splitlines() 
    if line.strip()  
  ]
  # 최종 분절 데이터 담는 그릇 
  units: list[str] = list() 

  # 라인별 순회 -> 문장의 끝 기호(.!?。 ！ ？) 체크 -> 기반으로 순회를 하여 units에 포함
  '''
  # 라인 1개에 문장 개 들어... 
  "환불 가능합니다. 배송비가 발생합니다."
  # 처리 
  [
    "환불 가능합니다.", 
    "배송비가 발생합니다."
  ]
  '''
  for line in lines: 
    # 후방 검색 "(?<=[탐색문자들표시])".  바로 앞 문자가 문장 종결 기호인지 체크
    sentences = re.split(r"(?<=[.!?。 ！ ？])\s+", line)
    # units에 담기 -> 문장 끝 기호로 분절된 문장을 리스트에 담기
    units.extend(
        sentence.strip() 
        for sentence in sentences
        if sentence.strip() 
    )
  # units의 구성원은 온전한 문장 1개 혹은 문장이 길어서 쪼개진 문장의 조각들이 포함될 수 있음 
  # 구성원 내부에 2개의 문장은 존재 x 
  # 단, 문서가 완결되는 표시(.!?。 ！ ？)가 있다는 전제하에 구성
  return units

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

# 코사인 유사도 검사 함수 
def _cosine_similarity(
    vector_a: Sequence[float],
    vector_b: Sequence[float],
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    norm_a = math.sqrt(
        sum(
            value * value
            for value in vector_a
        )
    )

    norm_b = math.sqrt(
        sum(
            value * value
            for value in vector_b
        )
    )

    # 0인 경우 처리 
    if norm_a == 0 or norm_b == 0:
        return 0.0

    # 공식 = 두 벡터의 내적 / (a벡터크기) * (b벡터크기)
    return dot_product / (norm_a * norm_b)

# 시맨틱 청킹 함수 
# 원문, 임계값(0.6 이하면 청킹), 최소 글자수, 최대 글자수(유사도가 계속 0.6 이상이어도 최대 글자수가 1200 넘어가면 청킹)
def semantic_splite_text( text:str, threshold: float=0.60, min_chars:int = 300, max_chars: int = 1200 ) -> list[str]:
  # 1. semantic 유닛 단위 분할
  units = _semantic_units( text )
  # 2. 값 체크 -> 분절의 결과
  if not units: return []
  # 3. 유닛 개수가 1개면 그대로 반환
  if len(units) == 1: return units

  # 4. 쪼개진 문장 혹은 문장 조각 -> 임베딩 처리
  embeddings = get_embeddings().embed_documents( units )

  # 5. 담는 그릇 
  chunks: list[str] = list() 
  current = units[0] 

  # 6. 유닛간, 이전 벡터와 다음 벡터간 유사도 검사 (순회)
  for index in range(1, len(units)): 
    # 6-1. 대상 벡터 획득
    # 이전 벡터 : 0 -> 1 -> 2 
    pre_vec = embeddings[ index - 1 ]
    # 현재 벡터 : 1 -> 2 -> 3 
    cur_vec = embeddings[ index ]

    # 6-2. 유사도 검사 
    similarity = _cosine_similarity( pre_vec, cur_vec )

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