'''
- RAG 검색 성능을 MRR, 일치되는 히트 수 기준으로 평가
- advanced_search() 성능 테스트
  - 성능 표 구성하여 기준에 미달하면, 비율 조절(8:2 -> 7:3 등 미세 조정을 통해서 검색 정확도 상승)
'''

# 1. 데이터 셋
from app.evaluation.dataset import CASES
# 2. 검색 
from app.retrieval import advanced_search

# 성능 평가
# Tol-k 검색 결과 질문에 대한 기대 문서가 포함되었는지 체크 
def main(k:int = 5):
  # 결과를 담을 그릇
  # hits : 기대 문서가 Top-k 검색 결과에 포함되었는지 기록
  # reciprocal : 기대 문서의 검색 순위에 대한 역순위 기록 (1/rank)
  hits, reciprocal = list(), list() 

  for case in CASES: 
    # 1. 질문과 k를 세팅해서 문서 검색 (RAG)
    rows = advanced_search( case['question'], k=k )

    # 2. 결과에서 문서 코드만 추출 
    # row[0] : 결과셋의 첫번째 컬럼이 문서 코드임
    codes = [ row[0] for row in rows ]

    # 3. 기대 정답 (문서 코드) 획득
    expected = case['expected_source']

    # 4. 기대 문서 코드(정답)이 Tok-K 결과에 포함되었는지 체크
    hit = expected in codes # True | False 
    hits.append(int(hit))

    # 5. 기대 문서(정답)이 몇 번째에 검색되었는지 체크, 없었다면 None 
    # hit가 참이면 -> 문서가 존재했다 (기대처럼 검색되었다) -> 순위 세팅, 거짓이면 -> None 
    rank = (codes.index(expected) + 1) if hit else None

    # 6. MRR 지표 계산을 위해서 순위의 역수 저장
    #    1등 -> 1/1, 2등 -> 1/2, 3등 -> 1/3 ... 
    reciprocal.append( 1/rank if rank else 0 )

    # 7. 질문별 검색 결과, 정답 문서 순위 등 출력 
    print( f"{case['question']} -> {codes} | expected={expected} | rank={rank}" )

    pass
  
  pass

# 직접 실행 대비 
if __name__ == '__main__':
  main()