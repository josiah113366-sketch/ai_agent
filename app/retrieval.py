'''
- postgresql + pgvector를 이용하여 벡터 데이터를 검색, 유사도 등 진행 
- 벡터 검색, 메타데이터 필터링, 하이브리드 서치 기능까지 확장 
'''

from pgvector import vector
from app.database import connect
from app.embedding import get_embeddings

def vector_search(query:str, k:int=5):
  # 1. 사용자 질문 임베딩 -> 벡터 변환 처리 
  q = vector( get_embeddings().embed_query(query) )

  # 2. 디비 커넥션, 커서 획득 
  results = None 
  with connect() as conn, conn.cursor() as cur: 
    cur.execute()
    results = cur.fetchall() 
  return results