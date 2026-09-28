# 목표
- 랭체인 이해, 간단한 체인 구성, llm 호출
- 체인 구성
  - 프롬프트 구성 -> llm 호출
  - 해당 구성은 향후 복잡한 agent 구성으로 확장

# 구조 
```
/
L app
  L llm.py : llm 모듈
L steps 
  L step4_langchain_basic.py :  체인 구성 (prompt | llm)
```

# 실행
```
python -m steps.step4_langchain_basic
---
# LangChain Runnable 파이프라인 핵심 정리

## 개념
LangChain의 **Runnable**은 "입력 → 처리 → 출력"이 가능한 모든 컴포넌트(프롬프트, LLM, 파서 등)가 구현하는 공통 인터페이스입니다. 이를 파이프(`|`) 연산자로 연결하면 **LCEL(LangChain Expression Language)** 파이프라인이 됩니다.

## 핵심 메서드
- `invoke()` : 단일 실행
- `batch()` : 여러 입력 병렬 처리
- `stream()` : 스트리밍 출력
- `ainvoke()` : 비동기 실행

## 예시 코드

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1. 각 컴포넌트 정의 (모두 Runnable)
prompt = ChatPromptTemplate.from_template(
    "다음 주제로 짧은 슬로건을 만들어줘: {topic}"
)
model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 2. 파이프 연산자로 체인 구성
chain = prompt | model | parser

# 3. 실행
result = chain.invoke({"topic": "친환경 자동차"})
print(result)
# 출력 예: "지구를 위한 한 걸음, 친환경 자동차와 함께"
```

## 동작 흐름
```
{"topic": "친환경 자동차"}
   ↓ prompt (딕셔너리 → 메시지)
ChatPromptValue
   ↓ model (메시지 → AI 응답)
AIMessage
   ↓ parser (메시지 → 문자열)
"지구를 위한 한 걸음..."
```

## 왜 유용한가
- **일관된 인터페이스**: 모든 컴포넌트가 같은 방식으로 동작
- **자동 병렬화·스트리밍·재시도** 지원 내장
- **가독성**: 복잡한 체인도 `|`로 직관적 표현
- **LangGraph** 등 상위 프레임워크의 기반이 됨

간단히 말해, Runnable 파이프라인은 **"레고 블록처럼 AI 컴포넌트를 조립"**하는 방식입니다.
```