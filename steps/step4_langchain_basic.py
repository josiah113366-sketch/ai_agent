'''
- 랭체인 적용
- 업무 프로세스를 체인으로 연결 후 작동
  - 프롬프트, llm 호출
'''

# 1. 프롬프트 
from langchain_core.prompts import ChatPromptTemplate
# 2. llm 
from app.llm import get_chat_model

# 3. 체인을 구성할 요소 생성 
# 3-1. system/human으로 구성된, 역할을 명시한 대화형 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 최신 트렌드에 민감한 AI 전문가입니다. 핵심만 설명합니다."),
    ("human", "{topic}을 예시 1개와 함께 설명해 주세요."), 
])

# 4. 랭체인의 체인 구성, 단계별로 진행할 내용 연결 (앞 단계의 출력은 뒷 단계의 입력). LCEL 형태를 따름, Runnable 파이프라인
# ChatPromptTemplate | ChatBedrockConverse
chain = prompt | get_chat_model()

# 5. 체인 호출 -> LLM 호출 
result = chain.invoke( {"topic":"LangChain Runnable 파이프라인"} )

# 6. 결과 출력 
print( result.content )