'''
사용자의 신호, 습관, 업무형태등 기억하게 지시 -> 이를 기억하는지 업무 지시
'''
import asyncio
from app.main import run


async def demo():
    # # 1. 명시적 기억 요청
    # await run("앞으로 답변은 짧은 bullet 형태를 선호한다. 이 선호를 기억해라.")

    # # 2. 확인
    # await run(
    #     "내가 선호하는 답변 방식이 무었이지?"
    # )

    print("\n--- 업무 규칙 등록 ---")
    await run(
        "우리 회사는 5만원 이상 환불 요청은 팀장 승인을 받은 후 처리해."
    )

    print("\n--- 업무 규칙 활용 ---")
    await run(
        "고객이 8만원 환불을 요청했어. 어떻게 처리해야 해?"
    )


asyncio.run(demo())