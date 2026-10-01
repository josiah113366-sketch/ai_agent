# 목표
- 랭그래프 + 정형 데이터(postgresql) + 비정형 데이터(pgvector) 같이 추론의 지식(배경)으로 사용
- 환불 통계 (SQL Tool)와 환불 정책 (Rag Tool)을 한 질문에서 함께 처리/사용

# sql 
- 환불 통계를 위한 sql 처리 
```
python -m scripts.migrate   
---
agentlab=# select * from refunds;
 refund_id | order_id |      requested_at      |     reason     |  amount  |  status  
-----------+----------+------------------------+----------------+----------+----------
         1 |        8 | 2026-09-04 09:00:00+00 | product_defect | 99000.00 | approved
(1 row)
```

# 구조 
```
/
L app
  L tools
    L sql_tools.py          : 추가로 특정 날짜 내에 환불 요청 건수, 금액, 사유 등 조회
L steps
  L step13_sql_rag_agent.py : 질문을 가지고 llm 추론 진행 
```

# 실행
```
python -m steps.step13_sql_rag_agent
---
-> 도구가 현재 제공되어 있지 않습니다. 특정 미션 해결 x 
[최종 답변]

 ## 1. 2026-09-01 ~ 2026-09-05 환불 현황

죄송하지만, 현재 제공된 도구에는 **환불 건수/환불 금액을 직접 조회할 수 있는 SQL Tool이 없습니다.**
- `sales_summary`: 결제 완료 매출·주문 건수만 집계 (환불 데이터 미포함)
- `top_products`: 결제 완료 매출 기준 상위 제품 조회 (환불 데이터 미포함)

따라서 해당 기간의 환불 현황(건수, 금액 등)은 **사실 확인이 불가능**하여 임의로 답변드릴 수 없습니다. 환불 데이터를 조회하려면 별도의 환불/반품 테이블에 접근 가능한 도구가 필요합니다. 필요하시면 해당 기간의 **결제 매출/주문 건수**(참고용, 환불 아님)는 조회해드릴 수 있으니 요청해주세요.

...
```