'''
텍스트 -> 임베딩하여 생성된 벡터 데이터를 postgreSQL pgvector에 저장하고, 유사도 검색 SQL 실행
'''

from pgvector import Vector
from app.embedding import get_embeddings