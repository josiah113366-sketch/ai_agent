'''
- 루프 엔지니어링을 구성한 에이전틱 루프 처리 체크 
'''
import asyncio
from app.loop_engine import run_agentic_loop

async def main():
  result = await run_agentic_loop("9월 초 환불 상황과 회사 환불 정책을 함께 분석해 줘.")
  print( result )

asyncio.run( 
  main() 
)
