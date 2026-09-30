'''
- 랭그래프 구성 시 노드들이 등록됨 
- 노드 사이에 공유할 Agent 상태 스키마 제공 
- 메시지, tool 반복 사용 횟수, 최종 구조화 응답 상태 등등 관리 
'''

# MessagesState를 상속받은 클래스는 랭그래프의 상태 관리용 사용 가능함 
from langgraph.graph import MessagesState

class AgentState(MessagesState): 
  # 라운드라는 정보만 일단 구성 
  rounds: int 