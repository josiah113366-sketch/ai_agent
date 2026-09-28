'''
bedrock 런타임 클라이언트 획득 코드 (코랩 참고)
'''
import boto3
from .config import AWS_REGION

def runtime_client():
  return boto3.client(service_name='bedrock-runtime', region_name = AWS_REGION)