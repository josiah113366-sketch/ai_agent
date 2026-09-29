'''
- 업무 문서를 chunking -> embedding -> PostgreSQL/pgvector 적재 
- RAG에서 사용하는 지식 베이스 구성에 대한 Ingestion pipeline 
'''

from pathlib import Path 
from .loader import load_markdown
from .splitter import splite_text
from app.embedding import get_embeddings
from app.database import connect

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
# print( DATA )
# rglob() : 하위 경로까지 다 찾아가서 해당 파일을 찾는다. 
# print( DATA.rglob("*.md") )

# md 파일별로 처리 
def ingest_file( path: Path ): 
  # 1. 문서 내에서 메타 데이터와 본문 분리(혹은 로드) -> '---' 기준 분할 
  meta, body = load_markdown( path )
  # print( meta )
  # print( '-' * 30 )
  # print( body )

  # 2. body(규약 원문) 관련 rag에서 검색 가능한 작은 단위로 chunk 처리 (fixed-size 단순 청킹 수행)
  chunks = splite_text(body)# , 150)
  # print( chunks )

  # 3. 임베딩 처리 
  vectors = get_embeddings().embed_documents( chunks )

  # 4. 메타데이터, 벡터를 데이터베이스에 입력 -> 하나의 트랜잭션으로 관리
  # documents, document_chunks 각각 테이블에 입력 
  with connect() as conn, conn.cursor() as cur: 
    # 1회 documents 저장 
    cur.execute() 
    document_id = cur.fetchone()[0]
    # 같은 문서로 저장된 청크가 존재한다면 -> 삭제 
    cur.execute() 
    # n회 document_chunks 저장 
    for i, (chunk, vector) in enumerate( zip(chunks, vectors) ): 
      cur.execute() 

    # 커밋 
    conn.commit()
    pass 
  pass 

def main():
  # 파일별 처리 
  for path in sorted(DATA.rglob("*.md")):
      print( path )
      ingest_file( path )
      break
  pass

if __name__ == "__main__":
  main()