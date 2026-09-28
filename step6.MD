# 목표
- bedrock의 임베딩 모델 활용하여 텍스트를 벡터로 표현
- amazon.titan-embed-text-v2:0 모델 사용 (토크나이저)
- 텍스트를 벡터로 변경하여 코사인 유사도 계산 직접 수행
- 기초 내용 : 딥러닝의 NLP에서 벡터화/토큰화 등에서 확인

# 구조
```
/
L app
  L embedding.py             : bedrock에서 지원하는 임베딩 모델 재사용 모듈
L steps
  L step6_embedding_basic.py : 텍스트 임베딩(벡터화 처리), 유사도 검사
```