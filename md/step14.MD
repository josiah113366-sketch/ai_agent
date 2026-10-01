# 목표
- Agent Memory 
- PostgreSQL + pgvector 방식으로 지식 저장(현재) + MEMORY 저장소 활용 
- MEMORY 저장소 활용하면 짧은 답변, 기존 질문에 대한 답변을 메모리에서 체크하여 LLM 사용 없이 응답 가능한 구조 구성 -> 중요도 관리 -> 토큰 비용(운영비) 절감 도움
- 장기 기억 활용

- 역할 
  - llm : 판단, 답변을 담당 두뇌 
  - RAG : 회사 문서, 규정 등 llm이 모르는 정보 
  - db : 실제 데이터들 저장, 조회 
  - MEMORY : 사용자의 맥락 기억, 패턴 기억 -> 사용자 주의, 답변 형태, 업무 형태, 기억 포인트 등 저장 -> 사용자 질문 시 해당 내용을 기반으로 답변할 때 제공
    - 사용자의 선호하는 방식으로 답변을 구성하게 도움 
    - llm이 추론을 할 때, 사용자가 누구고, 어떤 업무를 하고, 어떤 방식으로 답변 받기를 원하는지를 삽입 (프롬프트)
    - llm이 사용자를 처음 만난 사람처럼 행동하지 말고, 과거의 중요한 정보(맥락)을 제공하는 역할 담당 

# 구조
```
/
L sql 
  L 005_memory.sql    : 사용자의 정보를 저장하는 테이블, 검색
L app 
  L tools 
    L memory_tools.py : sql 역할 담당, 기능적으로 메모리 역할
  L agent (-> agent_langgraph)
    L graph.py        : 툴 등록 
  L config.py         : 사용자 아이디 환경 변수 구성
L steps
  L step14_memory.py  : 메모리 테스트 
L .env                : 사용자 아이디 더미 구성 (1명을 위한 아이디임, 실제 제거)
```

# sql 반영
```
python -m scripts.migrate   
---
\dt

# 테이블 구조 확인
\d agent_memories

# 컬럼명 잘못되어 있으면 수정
agentlab=# alter table agent_memories rename column used_id to user_id;
```

# 실행
```
python -m steps.step14_memory
---
++++++++++++++++++++++++++++++
[최종 답변]

 검색 결과, 저장된 선호 방식은 다음과 같습니다.

- **답변 형식**: 짧은 bullet 포인트 형태로 작성
- 중요도가 높게(0.9) 기록된 선호이며, 반복적으로(2건) 확인된 지속적인 패턴입니다.

앞으로도 이 형식에 맞춰 간결한 bullet 위주로 답변드리겠습니다. 혹시 특정 상황(예: 긴 분석/보고서)에서는 예외를 두고 싶으신가요?
++++++++++++++++++++++++++++++
```

```
await run(
  "2026-09-01 ~ 2026-09-05 기간 내에 환불 현황을 확인하고 사내 환불 정책을 기준으로 "
  "주의해서 봐야 할 내용을 보고해줘."
)
--- 
(agent) PS C:\Users\NT551_11TH\Desktop\workspace\ai_agent> python -m steps.step14_memory
---
(agent) PS C:\Users\NT551_11TH\Desktop\workspace\ai_agent> python -m steps.step14_memory
TOOL RESULT :  2026-09-01 ~ 2026-09-05 기간 내에 환불 현황을 확인하고 사내 환불 정책을 기준으로 주의해서 봐야 할 내용을 보고해줘.
TOOL CALLS :  ['refund_summary', 'search_company_policy']
TOOL RESULT :  [{'type': 'reasoning_content', 'reasoning_content': {'text': '', 'signature': 'Es4CCnkIEhABGAIqQHQNM2aiyw3uJA5c/kx05QMiWtK3cHVmf8poSSL70Qahm32G4KgUiWu92Mbh/mQY7bMh9NkWvOzU99uS1HpMV1kyDmNsYXVkZS1zYWZmcm9uOABCCHRoaW5raW5nWgw4Mjc5MTM2MTc2MzWoAc/p99UGEgwvgsy55QsPQU9hRqcaDLAdPcRbrTvl5ul5ICIwdZyacYTksi8M/HYIc32/N0QckRUbaUXvpVayhAMfCoCD32LO7nzWgc4V/AVcoluXKoIBdTHlOWF00oFEEpPUvcruRuiNKUXEcZZ7GNLvpBjOBZi70ToZr9NU2dk53YbkS5NSIN+A0MOqLjoxi7yIZmwXPiv383b6gqtGjVDsvVLQ92DofhpCdC0YlXz8ZTWDc+y3oSlUReV6PhkVAwnmAnLUjIlK2DkOYMk2DdGzVugfe6kDkhgB'}}, {'type': 'tool_use', 'name': 'refund_summary', 'input': {'start_date': '2026-09-01', 'end_date': '2026-09-05'}, 'id': 'tooluse_6c42u0sXzh69H5gNvCQAuV'}, {'type': 'tool_use', 'name': 'search_company_policy', 'input': {'query': '환불 정책', 'department': 'CS'}, 'id': 'tooluse_o3baajm8e38TMQlpsk6IHJ'}]
TOOL RESULT :  Error: NameError("name 'reason' is not defined")
 Please fix your mistakes.
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
TOOL RESULT :  [{'type': 'reasoning_content', 'reasoning_content': {'text': '', 'signature': 'EvQCCnkIEhABGAIqQEdPkbXfLZq33FHtnU67Df93W98plh4gjIXk/YuREwyqRDT+y1q2CmjKM7oyuWlZfQYSLNPRpp/66r+Poutw6dcyDmNsYXVkZS1zYWZmcm9uOABCCHRoaW5raW5nWgw4Mjc5MTM2MTc2MzWoAdTp99UGEgxmmqU/O6XZnE7P+TsaDHmX2wHHiatRKwcpUyIwCezJnrpJn386a2h6+VvACmANpeUgF1Sz754lHyt4/7dDqiw9HH4VgMxaF3f3x1e5KqgBoCFtFhnWDe0+TyRdVFVxkGu6L/WRkimcmQUyKFqKCcDLi7tqpAp8DAyW40oMUoS9MCe+nKdUYcRUsm1s1fNnIG0kfyPOyt41Hr86tSPXm9Iwz7Hx817+5lPbqXIRKKkgzmWb6pkwYIEfI2RoapSVtTII0eEcSH+iDUtE/t4L5Ipn1icVIDLibW4qU8FIqjuybsxTOuLxItSF9fIXSLIgJ2PAh6/ovKzJGAE='}}, {'type': 'text', 'text': '환불 집계 조회 중 오류가 발생했어 다시 시도해볼게.'}, {'type': 'tool_use', 'name': 'refund_summary', 'input': {'end_date': '2026-09-05', 'start_date': '2026-09-01'}, 'id': 'tooluse_LqQIitkSx6kXIuKAE2TMiw'}]
TOOL RESULT :  Error: NameError("name 'reason' is not defined")
 Please fix your mistakes.
TOOL RESULT :  현재 `refund_summary` 도구에서 내부 오류(`NameError: name 'reason' is not defined`)가 발생하여 2026-09-01 ~ 2026-09-05 기간의 환불 건수/총액/사유 데이터를 조회할 수 없었습니다. 이는 제 입력값 문제가 아니라 도구 자체의 처리 오류로 보입니다. 재시도했으나 동일하게 실패했습니다.

따라서 **실제 환불 수치는 확인하지 못했으며, 숫자를 추정하거나 지어내지 않습니다.**

다만, 사내 환불 정책(문서 코드: **CS-REFUND-2026**)을 기준으로, 환불 현황을 검토할 때 반드시 주의해서 봐야 할 체크포인트는 아래와 같습니다. 환불 데이터가 복구되면 이 기준에 대입해 이상 유무를 재확인해야 합니다.

## CS-REFUND-2026 기준 주의 체크포인트

1. **검수 완료 여부 확인**
   - 환불은 반품 상품이 물류센터에 도착·검수된 이후에만 진행되어야 함. 검수 전 환불이 처리된 사례가 있는지 확인 필요.
   - 검수 시 사용 여부, 구성품 누락, 훼손 여부, 반품 사유가 함께 기록되었는지 확인.

2. **환불 거절/제한 사유의 명확성**
   - 반품 제한이나 환불 거절 건은 사유가 고객에게 명확히 안내되었는지 확인.
   - 판단이 어려운 품질 문제나 반복 분쟁 건을 상담원이 임의 처리했는지, 아니면 CS 책임자에게 정상적으로 이관되었는지 확인. (임의 처리 건이 있다면 정책 위반)

3. **반복 문의/분쟁 건 기록 여부**
   - 동일 유형 반복 문의가 있었다면 사례와 처리 결과가 기록되어 향후 정책 개선에 반영될 수 있도록 되어 있는지 확인.

4. **사은품/증정품 반환 처리**
   - 사은품이 포함된 주문의 환불 건에서, 사은품 미반환 또는 사용 시 정상 판매가/고지 금액이 환불금에서 차감되었는지 확인.
   - 세트 상품의 경우 전체 구성 기준으로 반품 여부가 판단되었는지 확인.

5. **배송비 차감 처리의 정확성**
   - 단순 변심 반품 시 왕복 배송비가 고객 부담으로 올바르게 처리되었는지 확인.
   - 무료배송 주문의 전체/부분 반품 시, 최초 배송비 포함 여부 및 무료배송 기준 재충족 여부에 따른 배송비 추가 부과가 정책대로 적용되었는지 확인.

## 다음 단계 제안
- `refund_summary` 도구 오류가 해결되면 2026-09-01~09-05 환불 건수·총액·사유를 재조회하여, 위 5가지 체크포인트(특히 **임의 처리 여부**, **배송비/사은품 차감 적용 여부**)와 대조 검토하는 것을 권장합니다.
- 필요하시면 도구 복구 후 다시 요청해 주세요.
++++++++++++++++++++++++++++++
[최종 답변]

 현재 `refund_summary` 도구에서 내부 오류(`NameError: name 'reason' is not defined`)가 발생하여 2026-09-01 ~ 2026-09-05 기간의 환불 건수/총액/사유 데이터를 조회할 수 없었습니다. 이는 제 입력값 문제가 아니라 도구 자체의 처리 오류로 보입니다. 재시도했으나 동일하게 실패했습니다.

따라서 **실제 환불 수치는 확인하지 못했으며, 숫자를 추정하거나 지어내지 않습니다.**

다만, 사내 환불 정책(문서 코드: **CS-REFUND-2026**)을 기준으로, 환불 현황을 검토할 때 반드시 주의해서 봐야 할 체크포인트는 아래와 같습니다. 환불 데이터가 복구되면 이 기준에 대입해 이상 유무를 재확인해야 합니다.

## CS-REFUND-2026 기준 주의 체크포인트

1. **검수 완료 여부 확인**
   - 환불은 반품 상품이 물류센터에 도착·검수된 이후에만 진행되어야 함. 검수 전 환불이 처리된 사례가 있는지 확인 필요.
   - 검수 시 사용 여부, 구성품 누락, 훼손 여부, 반품 사유가 함께 기록되었는지 확인.

2. **환불 거절/제한 사유의 명확성**
   - 반품 제한이나 환불 거절 건은 사유가 고객에게 명확히 안내되었는지 확인.
   - 판단이 어려운 품질 문제나 반복 분쟁 건을 상담원이 임의 처리했는지, 아니면 CS 책임자에게 정상적으로 이관되었는지 확인. (임의 처리 건이 있다면 정책 위반)

3. **반복 문의/분쟁 건 기록 여부**
   - 동일 유형 반복 문의가 있었다면 사례와 처리 결과가 기록되어 향후 정책 개선에 반영될 수 있도록 되어 있는지 확인.

4. **사은품/증정품 반환 처리**
   - 사은품이 포함된 주문의 환불 건에서, 사은품 미반환 또는 사용 시 정상 판매가/고지 금액이 환불금에서 차감되었는지 확인.
   - 세트 상품의 경우 전체 구성 기준으로 반품 여부가 판단되었는지 확인.

5. **배송비 차감 처리의 정확성**
   - 단순 변심 반품 시 왕복 배송비가 고객 부담으로 올바르게 처리되었는지 확인.
   - 무료배송 주문의 전체/부분 반품 시, 최초 배송비 포함 여부 및 무료배송 기준 재충족 여부에 따른 배송비 추가 부과가 정책대로 적용되었는지 확인.

## 다음 단계 제안
- `refund_summary` 도구 오류가 해결되면 2026-09-01~09-05 환불 건수·총액·사유를 재조회하여, 위 5가지 체크포인트(특히 **임의 처리 여부**, **배송비/사은품 차감 적용 여부**)와 대조 검토하는 것을 권장합니다.
- 필요하시면 도구 복구 후 다시 요청해 주세요.
++++++++++++++++++++++++++++++
```