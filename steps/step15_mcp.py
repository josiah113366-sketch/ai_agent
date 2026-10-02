'''
MCP HOST 역할, 실제 만들고자 하는 앱/서비스
'''

import asyncio
from app.main import run

async def demo():
  # 존재하는 환율 정보
  # await run("달러 대비 원화 환율을 확인해.") 
  # 없는 환율 정보
  # await run("위안화 대비 원화 환율을 확인해.")

  await run(
    "2026-09-01 ~ 2026-09-05 기간내에 환불 현황을 확인하고," 
    "해당 비용을 원화와 달러 2개 통화로 알려주고, "
    "사내 환불 정책을 확인해서"
    "내가 선호하는 보고 방식으로 정리해 줘."  
  ) 

asyncio.run( demo() )