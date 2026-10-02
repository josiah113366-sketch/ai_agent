# 목표
- MCP 이해, 직접 구성, 연동, tool로 사용
  - Model Context `Protocol`
  - `LLM/Agent`와 `외부` 도구/데이터/서비스를 연결하기 위한 `표준 통신 규격`
  - github 공식 MCP
    - https://github.com/github/github-mcp-server
  - 그 외 오피셜 MCP 
    - 국내
      - https://playmcp.kakao.com/
      - ...
    - 해외 
      - ...
    - 서비스 주체별 MCP 제공
  - 사용 
    - 이미 구성된 MCP 사용 -> 서비스 업체 (노션, 슬랙 등에서 개방된 규격 사용하면 본인 앱에서 연동 가능)
    - playmcp 등 해당 사이트는 사용의 제한(클로드, OPENAI 등 특정 회사를 거쳐서 사용 가능함)
  - 장점
    - Agent <-> MCP 표준화 <-> 서비스 등 
      - 누가 만들어도 MCP 규격을 준수하면 어떤 LLM/Agent도 호환 가능하게 됨 
    - 각 서비스 주체들은 오피셜 MCP 개발하여 개방해줌. 
      - 서비스명 + MCP -> 확인 or MCP 커뮤니티/공인(포털) 사이트 검색 사용 -> 바로 적용됨
    - 사내용 MCP 없음 -> 비공개용, 사내용임 

- 참고
  - MCP 구성 요소
    | 구성 | 역할 | 현재 예제 |
    |---|---|---|
    | **MCP Host** | MCP를 사용하는 전체 애플리케이션 | LangChain Agent |
    | **MCP Client** | MCP Server와 통신 | `FastMCP Client` |
    | **MCP Server** | Tool을 외부에 제공 | `exchange_server.py` |

  - MCP Server를 개발하여 24시간 운영되는 어딘가의 호스팅/클라우드 등에서 운영
    - 운영/관리 비용 발생
    - playmcp, 기타 벤더들에서 운영하는 곳에 등록 해당 비용 상쇄할 수 있음 
  - MCP Server와 통신하여서 해당 서비스를 이용하기 위해서는 MCP Client를 개발해야함.
    - FastMCP 패키지를 이용하여 개발
  - 개발자가 만드는 AI 서비스에서 MCP를 사용한다면, MCP Client가 개발/설치되어서 사용되어야 함
    - LLM/Agent가 도구로서 MCP Client를 사용 -> MCP Server로 요청이 가고 -> 외부 서비스와 엑세스 요청/응답 -> 응답 -> LLM/Agent까지 도달함 
    - 개발자가 만드는 AI 서비스 -> MCP host라고 부름 

# 구조 
```
/
L mcp_servers
  L exchange_server.py : 편의상 MCP Server 역할, MCP host에 위치시킴 
L app
  L tools 
    L mcp_tools.py     : MCP Client 역할, 랭그래프상 도구로 등록 -> Agent에서 사용
  L agent (-> langgraph_agent)
    L graph.py         : 도구 등록
L steps
  L step15_mcp.py      : MCP 테스트용, MCP host 포지션
```

# 실행
```
python -m steps.step15_mcp
---
(agent) PS C:\Users\NT551_11TH\Desktop\workspace\ai_agent> python -m steps.step15_mcp
MCP 서버 연결 완료
TOOL RESULT :  2026-09-01 ~ 2026-09-05 기간내에 환불 현황을 확인하고,해당 비용을 원화와 달러 2개 통화로 알려주고, 사내 환불 정책을 확인해서내가 선호하는 보고 방식으로 정리해 줘.
TOOL CALLS :  ['recall_user_memory', 'refund_summary', 'get_exchange_rate', 'search_company_policy']
TOOL RESULT :  [{'type': 'reasoning_content', 'reasoning_content': {'text': '', 'signature': 'EoEDCnkIEhABGAIqQBMo4VPk4mq/6lIv/44ZMrU6SQluANGv4gzdfjtSEX42U1OHZIDZKNgKN3d4/in+CbogWc73eOZd99IADeDcNkYyDmNsYXVkZS1zYWZmcm9uOABCCHRoaW5raW5nWgw4Mjc5MTM2MTc2MzWoAfOH/NUGEgygtdpzX+6HWEQowI4aDMmVwg2WoWmvAfIZJiIwJqOe60QTMAXs5YkcFWaZml9DKdeQtcz/h1psBmpqlPvWGT7RMMzl0iOivDsM6JJUKrUBeoKl7dSQVytsTJIrqkWzG9A3s1a6m6BYBCDW313KMRwMWNvRmlA3ovDWMLDceMU0Iz5mIcH04bFSbBtMIJCDN9pdq+bezSKEcgNrEM5dBCc88UvHfcVuzVL970LfeekiZIyG4yTJoqiQ4jOHbH0ybbcvomB3Q5te6vDe2tbggTPmlw4Ej0gCjjVP0Jcz/77MTuG6tKXiHcPuKnTC5QqZD9s6tWvkny6RnRqQo1lol8pNpcmEnxgB'}}, {'type': 'text', 'text': '사용자의 선호 보고 방식을 확인하고, 환불 현황·환율·정책을 함께 조회하겠습니다.'}, {'type': 'tool_use', 'name': 'recall_user_memory', 'input': {'query': '보고 방식 선호'}, 'id': 'tooluse_xReEMgYzyXwAiIFiQNjLMh'}, {'type': 'tool_use', 'name': 'refund_summary', 'input': {'start_date': '2026-09-01', 'end_date': '2026-09-05'}, 'id': 'tooluse_1YWWyjf8Q1hmaTWvcHaQH6'}, {'type': 'tool_use', 'name': 'get_exchange_rate', 'input': {'base': 'USD', 'quote': 'KRW'}, 'id': 'tooluse_rKuL23aY0bn7PQLFNH2dIj'}, {'type': 'tool_use', 'name': 'search_company_policy', 'input': {'query': '환불 정책', 'department': 'CS'}, 'id': 'tooluse_VkbGnuAtnT0KrZ6UdOzl6z'}]
TOOL RESULT :  [preference score=0.425 importance=0.8] 보고서 작성 시 매출(Sales) 요약보다 CS 이슈 및 환불(Refund) 현황을 먼저 보여주는 순서를 선호함.
[preference score=0.324 importance=0.9] 답변은 짧은 bullet 형태로 작성하는 것을 선호함
[preference score=0.110 importance=0.8] 회사 정책: 5만원 이상 환불 요청은 팀장 승인을 받은 후 처리해야 함
TOOL RESULT :  Error: NameError("name 'reason' is not defined")
 Please fix your mistakes.
TOOL RESULT :  {'base': 'USD', 'quote': 'KRW', 'rate': 1364.3, 'meta': 'dummy-exchange-rate'}
TOOL RESULT :  [source=CS-REFUND-2026 | hybrid=0.454]
# 고객 반품 및 환불 정책

[source=CS-REFUND-2026 | hybrid=0.301]
환불은 반품 상품이 물류센터에 도착하여 검수된 이후 진행한다. 검수 과정에서는 상품의 사용 여부, 구성품 누락 여부, 훼손 여부와 반품 사유를 확인한다. 정상 반품으로 확인된 경우 원결제 수단을 기준으로 환불하며, 카드사나 결제대행사의 처리 일정에 따라 실제 환불 완료 시점에는 차이가 발생할 수 있다.

[source=CS-REFUND-2026 | hybrid=0.171]
고객센터 담당자는 반품 제한 또는 환불 거절이 필요한 경우 그 사유를 고객에게 명확하게 안내해야 한다. 판단이 어려운 품질 문제나 반복 분쟁 건은 임의로 처리하지 않고 CS 책임자에게 이관한다. 동일 유형의 문의가 반복될 경우 사례와 처리 결과를 기록하여 향후 정책 개선과 상담 기준 정비에 활용한다.

[source=CS-REFUND-2026 | hybrid=0.171]
반품 상품에 사은품이나 증정품이 포함되어 있었던 경우 해당 구성품도 함께 반환해야 한다. 사은품이 사용되었거나 반환이 불가능한 경우 회사는 사은품의 정상 판매가 또는 사전에 고지한 금액을 환불금에서 차감할 수 있다. 세트 상품은 특별한 안내가 없는 한 전체 구성을 기준으로 반품 여부를 판단한다.

[source=CS-REFUND-2026 | hybrid=0.167]
단순 변심에 의한 반품의 왕복 배송비는 원칙적으로 고객이 부담한다. 무료배송 주문을 전체 반품하는 경우 최초 배송비를 포함한 왕복 배송비가 환불금에서 차감될 수 있다. 일부 상품만 반품하는 경우에는 반품 이후의 주문 금액이 무료배송 기준을 충족하는지에 따라 최초 배송비가 추가로 부과될 수 있다.
TOOL CALLS :  ['refund_summary']
TOOL RESULT :  [{'type': 'reasoning_content', 'reasoning_content': {'text': '', 'signature': 'EosCCnkIEhABGAIqQBewKSLVRNT1Gb9vnFmW8C1F5Mtqi/oBPQNVApOKYsBCdpl458AQLDdV3fC78CqiDVN+d6Dg7i6N0RKGyCAlZcwyDmNsYXVkZS1zYWZmcm9uOABCCHRoaW5raW5nWgw4Mjc5MTM2MTc2MzWoAfyH/NUGEgxpAIkUk/S0/OI/exQaDOKfcxDf93GOBjNBkCIwFF1hsICkgbGEmylS0LL9q9coM6n08HzBkScRbvhtseYd831TIOes/DUhyR5Bec9eKkAIo/fpewmI3tfV6p9leMyNPDzn1cdiOkFOU9HMEHUeanNk2o8paTdMvZa+tCf/cySxOgh4gdmSEx541EkfkdcVGAE='}}, {'type': 'text', 'text': '환불 현황 조회에 오류가 발생했습니다. 다시 시도하겠습니다.'}, {'type': 'tool_use', 'name': 'refund_summary', 'input': {'end_date': '2026-09-05', 'start_date': '2026-09-01'}, 'id': 'tooluse_iPK0C4hMJnV67J7GS1TIxT'}]
TOOL RESULT :  Error: NameError("name 'reason' is not defined")
 Please fix your mistakes.
TOOL RESULT :  도구 자체 오류로 재시도해도 동일하게 실패합니다. 현재까지 확보된 정보로 정리해 드립니다 (환불 건수/총액은 시스템 오류로 조회 불가 상태이며, 추정치를 임의로 만들지 않았습니다).

**[2026-09-01 ~ 2026-09-05] 환불 현황 리포트**

- ⚠️ **환불 데이터 조회 실패**: `refund_summary` 툴에서 내부 오류(`NameError: reason`) 발생 → 건수/총액/사유 확인 불가. 재시도 필요 또는 시스템 담당자 확인 요청.

- **환율 정보** (참고용, 실시간 아님)
  - USD/KRW: **1,364.3원**
  - → 환불 총액 확정되면 KRW ÷ 1,364.3 으로 USD 환산 가능 (현재 금액 미확정으로 환산 불가)

- **사내 환불 정책 요약** (source=CS-REFUND-2026)
  - 환불은 반품 상품이 물류센터 도착 후 검수(사용여부/구성품누락/훼손/반품사유 확인) 완료 시 진행
  - 원결제 수단 기준 환불, 실제 완료 시점은 카드사/PG사 일정에 따라 차이 가능
  - 판단 어려운 품질문제·반복분쟁은 CS 책임자에게 이관
  - 사은품 미반환/사용 시 환불금에서 차감 가능
  - 단순변심 반품 왕복배송비는 고객 부담 원칙 (무료배송 전체반품 시 최초배송비 포함 차감 가능)
  - 참고(기억된 정책): **5만원 이상 환불 요청은 팀장 승인 필요**

- **Action Item**
  - refund_summary 재조회 필요 (시스템 오류 해결 후)
  - 금액 확정 시 5만원 이상 건은 팀장 승인 여부 확인 필요

데이터가 복구되면 바로 재조회해서 KRW/USD 금액을 포함한 완성된 리포트로 업데이트해 드리겠습니다.
++++++++++++++++++++++++++++++
[최종 답변]

 도구 자체 오류로 재시도해도 동일하게 실패합니다. 현재까지 확보된 정보로 정리해 드립니다 (환불 건수/총액은 시스템 오류로 조회 불가 상태이며, 추정치를 임의로 만들지 않았습니다).

**[2026-09-01 ~ 2026-09-05] 환불 현황 리포트**

- ⚠️ **환불 데이터 조회 실패**: `refund_summary` 툴에서 내부 오류(`NameError: reason`) 발생 → 건수/총액/사유 확인 불가. 재시도 필요 또는 시스템 담당자 확인 요청.

- **환율 정보** (참고용, 실시간 아님)
  - USD/KRW: **1,364.3원**
  - → 환불 총액 확정되면 KRW ÷ 1,364.3 으로 USD 환산 가능 (현재 금액 미확정으로 환산 불가)

- **사내 환불 정책 요약** (source=CS-REFUND-2026)
  - 환불은 반품 상품이 물류센터 도착 후 검수(사용여부/구성품누락/훼손/반품사유 확인) 완료 시 진행
  - 원결제 수단 기준 환불, 실제 완료 시점은 카드사/PG사 일정에 따라 차이 가능
  - 판단 어려운 품질문제·반복분쟁은 CS 책임자에게 이관
  - 사은품 미반환/사용 시 환불금에서 차감 가능
  - 단순변심 반품 왕복배송비는 고객 부담 원칙 (무료배송 전체반품 시 최초배송비 포함 차감 가능)
  - 참고(기억된 정책): **5만원 이상 환불 요청은 팀장 승인 필요**

- **Action Item**
  - refund_summary 재조회 필요 (시스템 오류 해결 후)
  - 금액 확정 시 5만원 이상 건은 팀장 승인 여부 확인 필요

데이터가 복구되면 바로 재조회해서 KRW/USD 금액을 포함한 완성된 리포트로 업데이트해 드리겠습니다.
++++++++++++++++++++++++++++++
```