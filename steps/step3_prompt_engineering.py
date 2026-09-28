'''
- 실제 제품과 대상을 제시하여, LLM이 홍보 문구를 구성하는 서비스 수행
- 프롬프트는 사전에 준비된 구성(role, ... 제약)에 맞춰서 동적 생성 및 llm 전달
'''
from app.bedrock import runtime_client
from app.config import BEDROCK_CHAT_MODEL
from app.prompts import marketing_prompt

# 프롬프트 구성 함수를 이용하여 동적 생성
prompt = marketing_prompt("AI 고객 상담 솔루션", "온라인 쇼핑몰 CS팀")
# print( prompt )

response = runtime_client().converse(
  modelId         = BEDROCK_CHAT_MODEL,
  messages        = [ { "role":"user", "content":[{ "text":prompt }] }],
  inferenceConfig = {
    "maxTokens" : 600 
  }
)

print( response["output"]["message"]["content"][0]['text'] )