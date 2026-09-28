'''
- 제시된 임베딩 모델을 이용하여, 텍스트 벡터화 변환 처리
- 코사인 유사도 검사를 통해서 유사 문장을 체크
'''

from app.embedding import get_embeddings

# 샘플 텍스트
texts = [
  '선수가 먼저, 클럽도 함께 모레노의 배려 리더십'
  '감독이 경기 전 선발 명단을 공개하지 않는 것은 특별한 일이 아니다.'
  '선수에게 먼저 설명하고, 몸을 먼저 생각하며, 가진 능력을 최대한 살리는 데 집중하고 있다.'   
]
# 3개의 문장을 한 번에 임베딩 처리 
vectors = get_embeddings().embed_documents( texts )
# 문장별 벡터화 길이 체크
print( '차원 ->', len(vectors[0]) )
print( '차원 ->', len(vectors[1]) )
print( '차원 ->', len(vectors[2]) )