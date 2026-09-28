# 목표
- PostgreSQL(Docker compose) / pgvector + bedrock embedding 
- PostgreSQL(RDB)에 extension을 설치하여 벡터를 컬럼의 타입으로 사용 가능하게 확장
  - 테이블 내 특정 컬럼이 벡터를 저장할 수 있도록 구성
  - RDB 기능, 벡터 디비 기능 같이 사용

# 구성
```
/
L docker-compose.yml
```

# 디비 구성
```
docker compose up -d
```