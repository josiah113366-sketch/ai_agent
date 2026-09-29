# 목표
- PostgreSQL(Docker compose) / pgvector + bedrock embedding 
- PostgreSQL(RDB)에 extension을 설치하여 벡터를 컬럼의 타입으로 사용 가능하게 확장
  - 테이블 내 특정 컬럼이 벡터를 저장할 수 있도록 구성
  - RDB 기능, 벡터 디비 기능 같이 사용

# 구성
```
/
L docker-compose.yml
L app
  L database.py       : PostgreSQL 접속 커넥션 구성 
L steps 
  L step7_pgvector.py : 간단한 텍스트(문장)을 테이블 upsert(insert or update) 처리
```

# 디비 구성
```
# 디비 설치 
docker compose up -d

# 연결 정보 추가 (postgresql://agent:agent@localhost:5432/agentlab)
.env
app.config.py
```

# 초기 sql 구성
```
/
L sql 
  L migrations
    L 001_pgvector.sql 
```

# 테이블 구성 및 초기 작업
```
python -m scripts.migrate
---
applied: 001_pgvector.sql

# 확인
docker exec -it agent-postgres psql -U agent -d agentlab  
---
psql (16.15 (Debian 16.15-1.pgdg12+2))
Type "help" for help.

agentlab=# 

# 현재 존재하는 모든 스키마(테이블) 확인
agentlab=# \dt
             List of relations
 Schema |       Name        | Type  | Owner 
--------+-------------------+-------+-------
 public | demo_vectors      | table | agent
 public | schema_migrations | table | agent
(2 rows)

# 구조 확인 -> q로 탈출
\d demo_vectors
                                Table "public.demo_vectors"
  Column   |     Type     | Collation | Nullable |                 Default                  
-----------+--------------+-----------+----------+------------------------------------------
 id        | bigint       |           | not null | nextval('demo_vectors_id_seq'::regclass)
 content   | text         |           | not null | 
 embedding | vector(1024) |           | not null | 
Indexes:
    "demo_vectors_pkey" PRIMARY KEY, btree (id)
    "demo_vectors_content_key" UNIQUE CONSTRAINT, btree (content)

# sql 수행 
agentlab=# select * from demo_vectors;
 id | content | embedding 
----+---------+-----------
(0 rows)
```