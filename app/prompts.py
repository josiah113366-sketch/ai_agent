'''
본 서비스의 핵심 프롬프트 
- 재사용 가능한 구조 프롬프트 템플릿 구성 (핵심 키워드 인자로 세팅 - 변수)
- 퓨샷 예시 준비 (서비스에 따라 달라짐)
- 프롬프트 실행, 구성은 분리 개념
- 랭체인 도입 전이므로 f-string 포맷팅 활용
'''

def marketing_prompt( product: str, audience: str ) -> str:
  return '''
# Role 
당신은 B2B SaaS 전문 마케터입니다. 

# Context 
제품: {product}
대상: {audience}

# Task 
핵심 가치를 설명하는 홍보 문구를 작성하세요. 

# Constraints 
- 5줄 이내
- 과장된 수치 금지
- 마지막에 CTA 1문장 
'''