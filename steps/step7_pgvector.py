'''
텍스트 -> 임베딩하여 생성된 벡터 데이터를  pgvector에 저장하고, 유사도 검색 SQL 실행
'''

# 1. 모듈 가져오기 
from pgvector import Vector
from app.embedding import get_embeddings
from app.database import connect

# 2. 검색어로 사용될만한 샘플 문장 준비 (hr, sales, cs)
samples = ["환불 정책", "연차 휴가 규정", "월 매출 분석"]

# 3. 임베딩 : [ [...], [...], [...(1024)] ]
vectors = get_embeddings().embed_documents( samples )

# 4. db 쿼리 수행 
with connect() as conn, conn.cursor() as cur: # with문 2개 사용한 것과 같은 결과 
  # 데이터 : 원문 텍스트, 임베딩된 벡터
  for text, vec in zip( samples, vectors ): # 순서대로 쌍으로 묶어서 하나씩 꺼냄 
    # print( text, vec )
    # sql 수행 
    cur.execute("""
      insert into demo_vectors(content, embedding) values (%s, %s)
      on conflict(content)
      do update set embedding=EXCLUDED.embedding
    """, (text, Vector(vec) ) )
    # break
  conn.commit()
  pass  

# 5. 유사도 검사 (질문 벡터 <-> DB상에 적재된 데이터 벡터 간 거리를 측정)
# 5-1. 질문의 벡터화 
q = get_embeddings().embed_query('상품을 반품하고 싶어요') # cs 관련 질문 
with connect() as conn, conn.cursor() as cur: 
  cur.execute()
  # 결과 출력 
  for result in cur.fetchall(): 
    print( result )