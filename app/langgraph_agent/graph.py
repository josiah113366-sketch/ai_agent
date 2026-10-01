'''
- 랭그래프 구성
- Agent 구성
- 랭그래프에 agent, tools 등을 등록, 순서 지정, 사용 가능한 형태로 빌드 
'''

# 1. 필요 모듈 획득
from langchain_core.messages import SystemMessage # Agent 구성 시 프롬프트에 System 프롬프트용 
from langgraph.graph import StateGraph, START, END # 랭그래프의 구성 요소 
from langgraph.prebuilt import ToolNode, tools_condition # Tool 실행, 호출 여부 판단 
from app.llm import get_chat_model # LLM 모델 
from app.langgraph_agent.state import AgentState # 랭그래프 상에서 상태 관리용 
from app.tools.sql_tools import sales_summary, top_products # SQL Tool 
from app.tools.rag_tools import search_company_policy # rag tool 

# 2. 툴 목록 구성
TOOLS = [sales_summary, top_products, search_company_policy]

# 3. 그래프 빌드 
def build_graph(): 
  
  # 3-1. 그래프 생성
  graph = StateGraph( AgentState ) # 상태 정보를 가진 그래프 생성
  # ... 

  # 그래프 컴파일 및 반환 
  return graph.compile()
