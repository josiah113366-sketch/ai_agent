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
  pass

# 직접 실행 대비 
if __name__ == '__main__':
  main()