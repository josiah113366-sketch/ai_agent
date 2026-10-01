# 목표
- Agent Memory 
- PostgreSQL + pgvector 방식으로 지식 저장(현재) + MEMORY 저장소 활용 
- MEMORY 저장소 활용하면 짧은 답변, 기존 질문에 대한 답변을 메모리에서 체크하여 LLM 사용 없이 응답 가능한 구조 구성 -> 중요도 관리 -> 토큰 비용(운영비) 절감 도움
- 장기 기억 활용