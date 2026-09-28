'''
bedrock llm 호출 테스트
'''
from app.bedrock import runtime_client
from app.config import BEDROCK_CHAT_MODEL

# 1. 런타임 클라이언트 획득 
client = runtime_client()

# 2. LLM 호출 (with 메시지(프롬프트, 질의))
response = client.converse(
  modelId         = BEDROCK_CHAT_MODEL,
  messages        = [ { "role":"user", "content":[{"text":"AI Agent를 5줄로 설명해 줘."}] }],
  # 창의성 조정하는 옵션은 최신 모델로 가면서 배제/대체, 직접 세팅 x 
  inferenceConfig = {
    "maxTokens" : 500 
  }
)

# 3. 응답 결과 파싱, 출력 
print( response["output"]["message"]["content"][0]['text'] )