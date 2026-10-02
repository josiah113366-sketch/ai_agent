'''
- MCP Client 담당 
- MCP Server와 통신 담당
- 랭그래프에 툴 노드에 등록이 됨 
- Agent가 필요하면 도구로 사용 
'''

# 1. 모듈 가져오기
from pathlib import Path
from fastmcp import FastMCP
from langchain_core.tools import tool 

# 2. MCP 서버가 백엔드 등에서 구동되어 있지 않으므로 직접 경로를 접근하여 실행
#    경로 획득
ROOT = Path(__file__).resolve().parents[2] # 프로젝트 루트까지 Path 경로 획득
#    실제 MCP Server 경로
SERVER = ROOT / "mcp_servers" / "exchange_server.py"