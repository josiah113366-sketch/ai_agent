'''
bedrock 임베딩 모델을 생성, 재사용 모듈
텍스트 입력 -> 벡터로 변환 처리 시 사용할 수 있다 
'''
from langchain_aws import BedrockEmbeddings
from .config import AWS_REGION, BEDROCK_EMBED_MODEL

# 싱글톤 스타일로 구성 
_embeddings = None

def get_embeddings():
  global _embeddings
  if _embeddings is None:
    # 최초 1회만 초기화 
    # dimensions : 차원 조정 가능 (기본 1024)
    _embeddings = BedrockEmbeddings(model_id=BEDROCK_EMBED_MODEL, region_name=AWS_REGION)
  return _embeddings