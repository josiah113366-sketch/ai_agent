'''
- 업무 문서를 chunking -> embedding -> PostgreSQL/pgvector 적재 
- RAG에서 사용하는 지식 베이스 구성에 대한 Ingestion pipeline 
'''

from pathlib import Path 
from .loader import load_markdown
from .splitter import splite_text

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
  chunks = splite_text(body# , 150)
  print( chunks )
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