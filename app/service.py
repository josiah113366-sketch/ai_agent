'''
fastapi 기반 에이전트 서비스
'''
# 1. 모듈 가져오기 
from fastapi import FastAPI
from pydantic import BaseModel
from app.main import invoke_agent

# 2. FastAPI 객체 생성 
app = FastAPI(title="에이전트 서비스", description="랭그래프+bedrock+Agent", version="1.0.0")

# 3. 요청 시 데이터 구조 
class ChatRequest(BaseModel): 
  message:str

# 4. 라우팅 
# 4-1. /chat 
@app.post("/chat")
async def chat(req:ChatRequest): 
  pass

# 4-2. /health 
@app.post("/health")
async def health(): 
  pass