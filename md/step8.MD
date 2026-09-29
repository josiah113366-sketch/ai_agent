# 목표 
- 문서 레벨로 디비에 데이터 삽입
- 문서(말뭉치) -> 쪼개는 과정 필요함(청킹, chunk 단위 자름)
  - [v] 단순 크기 -> ... -> 시맨틱 청킹(주제가 변경되면 자름)
  - RAG 서비스 -> 질문의 포인트는 청킹 기준을 어떻게 수행하였는가? 
  - 문서 테이블(1) -> 청킹 테이블(n)
  - 문서 (md + 텍스트 형태 제공)
    - Markdown formatter 처리(메타 데이터), document chunking 처리 (임베딩 처리)

# 데이터
- cs, sales, hr 관련 사내 규정 문서
- 현재 = 메타 데이터 + 규정 
- 향후 규정 내용을 더 확대 예정 (청킹이 n개로 확장되는 것 확인)

# 구조 
```
/
L sql
  L migrations
    L 002_documents.sql
L steps 
  L step8_document_ingestion.py
L app
  L ingestion
    L __init__.py
    L ingest.py
    L loader.py 
    L splitter.py 
```

# 데이터를 벡터화 디비 입력 절차
- 002_documents.sql

- 테이블 생성
```
python -m scripts.migrate 
---
# 테이블 생성 확인
agentlab=# \dt
             List of relations
 Schema |       Name        | Type  | Owner 
--------+-------------------+-------+-------
 public | demo_vectors      | table | agent
 public | document_chunks   | table | agent
 public | documents         | table | agent
 public | schema_migrations | table | agent
(4 rows)
```

# 실행 
```
python -m steps.step8_document_ingestion
```