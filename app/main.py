'''
랭그래프 기반 에이전트 실행하는 코드
'''
import asyncio
from app.langgraph_agent.graph import build_graph 

async def run(query: str): 
  '''
    사용자 질문 -> 랭그래프 기반 에이전트 전달
  '''
  await build_graph().ainvoke(
    
  )