'''
- 메타 데이터와 본문(규정) 분리
'''
from pathlib import Path 
import yaml

def load_markdown( path: Path ):
  '''
  parameters
    - path : 원소스 (*.md)의 실제 경로
  returns
    - meta 데이터 (yaml -> dict 형태 등)
    - body 본문 규정 데이터 (텍스트, 문자열)
  '''
  # 1. markdown 전체를 읽은 후 yaml 프런트 포맷터 존재하는지 체크 (---)
  text = path.read_text(encoding='utf=8')
  print( text )
  # 2. 구분자 체크 (---)
  if not text.startswith('---'): 
    # 메타 데이터가 없는 규정집 문서임 
    return {}, text
  pass