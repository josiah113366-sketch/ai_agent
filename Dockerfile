FROM python:3.12-slim
WORKDIR /app
# 패키지 목록 갱신 -> PostgreSQL 클라이언트 런타임 설치 (pgvector 등 사용할 수 있게 구성) -> 불필요한 목록 제거 -> 용량 다이어트
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*