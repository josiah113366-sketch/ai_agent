# 프롬프트 
from langchain_core.prompts import ChatPromptTemplate
# llm 
from app.llm import get_chat_model
# 응답 결과 파싱
from langchain_core.output_parsers import StrOutputParser

# 신입 개발자 에이전트 
developer_prompt = ChatPromptTemplate.from_messages([
  # 페르소나를 통해 신입 개발자 에이전트를 규정
    ("system", "당신은 열정적인 '신입 파이썬 개발자'입니다. 요청받은 기능을 코드로 작성하세요. 설명은 최소화하고 코드 위주로 작성하세요."),
    ("human", "{request}"), 
])
# 체인 구성 
developer_agent = developer_prompt | get_chat_model() | StrOutputParser()

# 전문 리뷰어 에이전트 
# 피드백 반영 에이전트 