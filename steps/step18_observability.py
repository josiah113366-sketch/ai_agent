'''
Agent 실행을 통해서 LLM/TOOL/랭그래프 등이 실행 -> 랭스미스에 tracing 기록 전송 -> 대시보드 모니터링, 분석 
'''
import asyncio
from app.main import run

def main():
  # 1. 랭스미스 상태 체크
  print("LangSmith Status", )
  query = "상품 자체 하자의 환불 조건을 근거와 함께 알려줘."

asyncio.run( 
  # run(query)
)
