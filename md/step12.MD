# 목표
- LangGraph + bedrock + LangChain + tools 
- LangGraph
  - StateGraph -> Agent -> ToolNode -> Agent 순환 루프를 구성하는 자율형 에이전트 기본 구성
  - Reason/Tool/Observe 루프 구성
- 질의 -> 적절한 Tool을 LLM이 선택하고, Tool 사용, 결과를 이용하여 관찰 -> 최종 답변까지 반복 진행 체크 
- 랭그래프 관점에서
  - 노드 : ToolNode, AgentNode 등 존재 
  - 순서, 방향성 지정
    - 시작점 지정
    - AI 노드에서 반드시 B 노드로 간다 
    - 끝점 지정 
  - 끝 노드의 출력값 -> 최종 추론 결과 
  - 노드를 순환하면서 다양한 노드 사용 -> 흔적이 남음 -> MessagesState를 상속받은 객체에 저장 
    - MessagesState는 messages(list) 변수에 순서대로 기록함 
    - 통상 MessagesState를 상속받아서 커스텀 변수를 추가하여 노드상 State 관리 수행

# 구조 
```
/
L app
  L agent (-> langgraph_agent)
    L __init__.py 
    L graph.py                : 랭그래프 구성 (노드 추가하는 등 구성)
    L prompts.py              : 에이전트의 프롬프트
    L state.py                : 상태 관리
  L main.py                   : 에이전트 구동 
L steps 
  L step12_langgraph_agent.py : 테스트 코드 
```

# 실행
- "상품 하자로 반품할 경우 환불 기간과 배송비 부담 주체를 알려주세요."
```
python -m steps.step12_langgraph_agent
---
HumanMessage -> AIMessage Tool use 판단 -> ToolMessage -> AIMessage END로 판단 -> 종료 
  [
    HumanMessage(content='상품 하자로 반품할 경우 환불 기간과 배송비 부담 주체를 알려주세요.', additional_kwargs={}, response_metadata={}, id='cad7a92b-0384-4afa-be48-903151fb278b'), 
    
    AIMessage(content=[{'type': 'reasoning_content', 'reasoning_content': {'text': '', 'signature': 'EtsCCnkIEhABGAIqQNRQwEOCPUbGDn6k4KJrxIIz89JFpvSmY5z1p0BszXoZ7BaJA5jX4eIdbNtak3U9jdkHXvklx6ejcpvbjcFoutoyDmNsYXVkZS1zYWZmcm9uOABCCHRoaW5raW5nWgw4Mjc5MTM2MTc2MzWoAcrq9tUGEgzlgeKdhXpqPLuqlq8aDJ4OMYP33JxINuXTMSIw9OEUeG5GoxQmCYdDIeHoMYodMa8JtdeeiJOdbGF2wUpTJZpdvHKcjzh9p5DalUOFKo8BaL95SzYEQTqX1rExXRVAGtgQw5uccSLwUOxqcF5hRReP5yJENK/64NX8Bka6xFkncTF8CLiVdQ9kqvoiKdGyxGwP1C/ZcUjQXzTOPkQ75A0ulRbTBkWI4r6lZBHq7re0asaJNv52iGoNQVhcXBQUYoFPQZhIA5QJeqzDzpVXuhjQcF0OVr3HhHjvgawapS8YAQ=='}}, {'type': 'tool_use', 'name': 'search_company_policy', 'input': {'query': '상품 하자 반품 환불 기간 배송비 부담 주체', 'department': 'CS'}, 'id': 'tooluse_GRwvJhytFhJe9SuXWyZHhN'}], additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': '6d1e7a6b-539d-40b2-baa1-92c3b776b0a3', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:20:11 GMT', 'content-type': 'application/json', 'content-length': '1049', 'connection': 'keep-alive', 'x-amzn-requestid': '6d1e7a6b-539d-40b2-baa1-92c3b776b0a3'}, 'RetryAttempts': 0}, 'stopReason': 'tool_use', 'metrics': {'latencyMs': [2726]},'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f50c-1e04-77b1-ad15-0ee7f3c0d85c-0', tool_calls=[{'name': 'search_company_policy', 'args': {'query': '상품 하자 반품 환불 기간 배송비 부담 주체', 'department': 'CS'}, 'id': 'tooluse_GRwvJhytFhJe9SuXWyZHhN', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1089, 'output_tokens': 131, 'total_tokens': 1220, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}), 
    
    ToolMessage(content='[source=CS-REFUND-2026 | hybrid=0.281]\n단순 변심에 의한 반품의 왕복 배송비는 원칙적으로 고객이 부담한다. 무료배송 주문을 전체 반품하는 경우 최초 배송비를 포함한 왕복 배송비가 환불금에서 차감될 수 있다. 일부 상품만 반품하는 경우에는 반품 이후의 주문 금액이 무료배송 기준을 충족하는지에 따라 최초 배송비가 추가로 부과될 수 있다.\n\n[source=CS-REFUND-2026 | hybrid=0.278]\n# 고객 반품 및환불 정책\n\n[source=CS-REFUND-2026 | hybrid=0.270]\n상품 자체의 제조상 하자나 기능상 문제가 확인되면 상품 수령 후 30일 이내 교환 또는 환불을 신청할 수 있다. 이 경우 고객에게 귀책사유가 없는 것으로 판단되면 회수 배송비와 교환상품의 재배송 비용은 회사가 부담한다. 필요한 경우 고객센터는 사진, 동영상 또는 제품 상태 확인 자료를 요청할 수 있다.\n\n[source=CS-REFUND-2026 | hybrid=0.257]\n일반 반품은 상품 수령 후 7일 이내 신청할 수 있다. 고객은 주문번호와 반품 사유를 고객센터 또는 온라인 반품 신청 화면을 통해 접수해야 한다. 단순 변심에 의한 반품은 상품이 사용되지 않았고 포장 및 구성품이 정상적으로 보존된 경우에 한해 처리한다.\n\n[source=CS-REFUND-2026 | hybrid=0.257]\n환불은 반품 상품이 물류센터에 도착하여 검수된 이후 진행한다. 검수 과정에서는 상품의 사용 여부, 구성품 누락 여부, 훼손 여부와 반품 사유를 확인한다. 정상 반품으로 확인된 경우 원결제 수단을 기준으로 환불하며, 카드사나 결제대행사의 처리 일정에 따라 실제 환불 완료 시점에는 차이가 발생할 수 있다.', name='search_company_policy', id='3b25e480-dae8-4d36-80b6-3038ea8ed4f2', tool_call_id='tooluse_GRwvJhytFhJe9SuXWyZHhN'), 
    
    AIMessage(content='**상품 하자(제조상 하자/기능상 문제)로 인한 반품 안내** (문서 코드: CS-REFUND-2026)\n\n- **환불/교환 신청 기간**: 상품 수령 후 **30일 이내** 교환 또는 환불 신청 가능\n- **배송비 부담 주체**: 고객에게 귀책사유가 없는 것으로 판단되면 **회수 배송비 및 교환상품 재배송비 모두 회사(판매자)가 부담**\n- **추가 참고사항**: 고객센터는 하자 확인을 위해 사진, 동영상 또는 제품 상태 확인 자료를 요청할 수 있으며, 환불은 반품 상품이 물류센터에 도착해 검수 완료된 이후 원결제 수단으로 진행됩니다.\n\n※ 참고로 단순 변심에 의한 반품은 7일 이내 신청, 왕복 배송비는 원칙적으로 고객 부담이라는 점에서 하자 반품과 차이가 있습니다.', additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': 'fc4870d8-a415-4930-aa61-d43cea135d33', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:20:18 GMT', 'content-type': 'application/json', 'content-length': '1159', 'connection': 'keep-alive', 'x-amzn-requestid': 'fc4870d8-a415-4930-aa61-d43cea135d33'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [5294]}, 'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f50c-32ec-7d62-87d6-c097503dcce2-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 2017, 'output_tokens': 362, 'total_tokens': 2379, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}})
  ]
  ++++++++++++++++++++++++++++++
  [최종 답변]

  **상품 하자(제조상 하자/기능상 문제)로 인한 반품 안내** (문서 코드: CS-REFUND-2026)

  - **환불/교환 신청 기간**: 상품 수령 후 **30일 이내** 교환 또는 환불 신청 가능
  - **배송비 부담 주체**: 고객에게 귀책사유가 없는 것으로 판단되면 **회수 배송비 및 교환 상품 재배송비 모두 회사(판매자)가 부담**
  - **추가 참고사항**: 고객센터는 하자 확인을 위해 사진, 동영상 또는 제품 상태 확인 자료를 요청할 수 있으며, 환불은 반품 상품이 물류센터에 도착해 검수 완료된 이후 원결제 수단으로 진행됩니다.

  ※ 참고로 단순 변심에 의한 반품은 7일 이내 신청, 왕복 배송비는 원칙적으로 고객 부담이라는 점에서 하자 반품과 차이가 있습니다.
  ++++++++++++++++++++++++++++++ 
```

# 판단 흐름
```
result["messages"]

[0] HumanMessage
    └─ 사용자 질문

[1] AIMessage
    └─ Tool Calls
      ├─ sales_summary
      └─ top_products

[2] ToolMessage
    └─ sales_summary 결과
    └─ top_products 결과

[3] AIMessage
    └─ 최종 답변

rounds = 2 (LLM 두번 추론)
```

# 요구 사항 분석 2 
- query = "2026-09-01부터 2026-09-05까지 매출과 상위 3개 상품을 알려줘"
```
[
  HumanMessage(content='2026-09-01부터 2026-09-05까지 매출과 상위 3개 상품을 알려줘', additional_kwargs={}, response_metadata={}, id='e5027b58-4c3f-420e-9b26-9329d2da0bd0'), 

  AIMessage(content=[{'type': 'reasoning_content', 'reasoning_content': {'text': '', 'signature': 'EpoCCnkIEhABGAIqQOQJrCzFifEp5IU/B9/cIyNUnPqsl/PxrVMFTK5/t+BfWiI9eh7YidwN6595g+eN8W7TPPjW4vPDz9i7yBbMgPcyDmNsYXVkZS1zYWZmcm9uOABCCHRoaW5raW5nWgw4Mjc5MTM2MTc2MzWoAZHu9tUGEgzZx8fPm6QZE05LfS0aDP1Bz6sqUeCyTJ9VVyIwcSQyPfZKWDArbBmOCnOSv6043b3HHTpO1q8ppDgE6T+FNGuvELwGcPY/BIVE5WeiKk+7GMXWPh8rz4HKWcTdWlFNPs0tshvYQgwmCEUDjFGhxL3qsccqYSMeFx3bVVOxb+nVKycQJlRtZ3ZmNktlmOgS0B0aZwr9P3ig/uv+zgchGAE='}}, {'type': 'text', 'text': '사실 확인을 위해 2026-09-01 ~ 2026-09-05 기간의 매출 집계와 상위 상품 데이터를 조회하겠습니다.'}, {'type': 'tool_use', 'name': 'sales_summary', 'input': {'start_date': '2026-09-01', 'end_date': '2026-09-05'}, 'id': 'tooluse_8u5T4v1pp2d780uqI5TFHM'}, {'type': 'tool_use', 'name': 'top_products', 'input': {'start_date': '2026-09-01', 'end_date': '2026-09-05', 'limit': 3}, 'id': 'tooluse_cuwW5m2eWfVPndyUhnwKTv'}], additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': '60bda207-c8a7-4808-99a0-9ae1e70e7250', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:27:48 GMT', 'content-type': 'application/json', 'content-length': '1221', 'connection': 'keep-alive', 'x-amzn-requestid': '60bda207-c8a7-4808-99a0-9ae1e70e7250'}, 'RetryAttempts': 0}, 'stopReason': 'tool_use', 'metrics': {'latencyMs': [4610]}, 'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f513-110c-7152-9e1a-32d44f14347b-0', tool_calls=[{'name': 'sales_summary', 'args': {'start_date': '2026-09-01', 'end_date': '2026-09-05'}, 'id': 'tooluse_8u5T4v1pp2d780uqI5TFHM', 'type': 'tool_call'}, {'name': 'top_products', 'args': {'start_date': '2026-09-01', 'end_date': '2026-09-05', 'limit': 3}, 'id': 'tooluse_cuwW5m2eWfVPndyUhnwKTv', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1087, 'output_tokens': 266, 'total_tokens': 1353, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}), 

  ToolMessage(content='revenue=3586000.00, orders=8, range=2026-09-01~2026-09-05', name='sales_summary', id='25fee7b4-ad4f-4b70-add4-600f6fec31a7', tool_call_id='tooluse_8u5T4v1pp2d780uqI5TFHM'), ToolMessage(content='1. 사내 AI Agent 구축: qty=1, revenue=1200000.00 \n2. RAG 구축 컨설팅: qty=1, revenue=800000.00 \n3. 데이터 분석 패키지: qty=4, revenue=600000.00 ', name='top_products', id='a7492821-337e-4d68-a52d-14569d17d1dc', tool_call_id='tooluse_cuwW5m2eWfVPndyUhnwKTv'), 

  AIMessage(content='## 📊 2026-09-01 ~ 2026-09-05 매출 요약\n\n**전체 매출 집계**\n- 총 매출: **3,586,000원**\n- 총 주문 건수: **8건**\n\n**상위 3개 상품 (매출 기준)**\n\n| 순위 | 상품명 | 판매 수량 | 매출액 |\n|---|---|---|---|\n| 1 | 사내 AI Agent 구축 | 1 | 1,200,000원 |\n| 2 | RAG 구축 컨설팅 | 1 | 800,000원|\n| 3 | 데이터 분석 패키지 | 4 | 600,000원 |\n\n위 데이터는 결제 완료 기준으로 집계된 결과입니다. 추가로 특정 상품의 상세 내역이나 다른 기간 비교가 필요하시면 알려주세요.', additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': 'a307ce4e-c838-47b8-bb58-00f1ee934dc9', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:27:52 GMT', 'content-type': 'application/json', 'content-length': '898', 'connection': 'keep-alive', 'x-amzn-requestid': 'a307ce4e-c838-47b8-bb58-00f1ee934dc9'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [3807]}, 'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f513-26fb-7443-a970-a4ee594126dc-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 1529, 'output_tokens': 293, 'total_tokens': 1822, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}})
]
++++++++++++++++++++++++++++++
[최종 답변]

 ## 📊 2026-09-01 ~ 2026-09-05 매출 요약

**전체 매출 집계**
- 총 매출: **3,586,000원**
- 총 주문 건수: **8건**

**상위 3개 상품 (매출 기준)**

| 순위 | 상품명 | 판매 수량 | 매출액 |
|---|---|---|---|
| 1 | 사내 AI Agent 구축 | 1 | 1,200,000원 |
| 2 | RAG 구축 컨설팅 | 1 | 800,000원 |
| 3 | 데이터 분석 패키지 | 4 | 600,000원 |

위 데이터는 결제 완료 기준으로 집계된 결과입니다. 추가로 특정 상품의 상세 내역이나 다른 기간 비교가 필요하시면 알려주세요.
++++++++++++++++++++++++++++++
```