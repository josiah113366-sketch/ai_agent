'''
프로그램 전체 환경 변수 로드, 관리
'''
import os
from dotenv import load_dotenv

# 환경 변수 로드 (.env)
load_dotenv() # 환경 변수 설정 완료됨 (os 레벨)

# 변수로 사용 
# .env -> load_dotenv() -> os단 환경 변수 자동 세팅 
# os.getenv(키 값, 기본 값(누락 시 사용))
# 리전 
AWS_REGION               = os.getenv('AWS_REGION', 'us-east-1')
# LLM 모델 
BEDROCK_CHAT_MODEL       = os.getenv('BEDROCK_CHAT_MODEL', 'us.anthropic.claude-sonnet-5')
# 임베딩 모델, 토크나이저 (api용 사용)
BEDROCK_EMBED_MODEL      = os.getenv('BEDROCK_EMBED_MODEL', 'amazon.titan-embed-text-v2:0')
# 벡터 DB 주소
DATABASE_URL             = os.getenv('DATABASE_URL', '')