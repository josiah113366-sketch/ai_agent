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
    # 추론만 담당하는 LLM 
    model = get_chat_model() 
    # 도구를 사용하는 LLM, LLM에 Tool 연결
    bind_model = model.bind_tools( TOOLS )

    # Agent 노드 -> 추론만 할 것인가? 도구를 사용하여 결과를 가지고 추론을 할 것인가? 
    def call_model(state:AgentState): 
        # 1. 라운드 값 획득 (랭그래프 내에서 순환을 몇 번 했는가? LLM 추론을 몇 번 했는가?)  # Agent 수행 횟수 
        rounds = state.get('rounds', 0)
        # 2. 라운드를 기점으로 모델 선택 
        # 차후, 모델을 여러 케이스로 준비 (모델 id, 제품(gpt, claude, 도구 등록 상이하게))
        select_model = model if rounds >= 6 else bind_model # 6회 이상이면 그냥 추론, 이하면 도구를 이용한 추론 
        pass

    # 3-1. 그래프 생성
    graph = StateGraph(AgentState)  # 상태 정보를 가진 그래프 생성
    # ...

    # 3-2. 노드 등록 (LLM 추론, 도구)
    graph.add_node( )
    # handle_tool_error : 툴 실행 중에 에러 발생 시 에이전트 전체를 바로 실패시키지 않고 오류를 처리하여 agent 대응하게 할 것인가? 
    graph.add_node( ToolNode(TOOLS, handle_tool_error = True) )

    # 3-x. 그래프 컴파일 및 반환
    return graph.compile()
