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

# 이전 에이전트의 출력이 다음 에이전트의 입력이 됨 
# 전문 리뷰어 에이전트 
reviewer_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 까다로운 '전문 개발자'입니다. 신입 개발자가 작성한 코드를 리뷰하세요. \n"
               "보안 취약성, 비효율적인 부분, 스타일 가이드를 점검하고 수정 제안을 하세요. \n" 
               "코드가 완벽하다면 'pass'라고만 답변하세요. \n" 
    ),
    ("human", "다음 코드를 리뷰해 주세요.\n\n{code}"), 
])
# 체인 구성 (고도화된 전문 기능, 심도있는 추론 -> 모델 상위로 적용)
reviewer_agent = reviewer_prompt | get_chat_model() | StrOutputParser()

# 피드백 반영 에이전트 