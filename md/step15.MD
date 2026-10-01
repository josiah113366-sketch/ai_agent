# 목표
- MCP 이해, 직접 구성, 연동, tool로 사용
  - Model Context `Protocol`
  - `LLM/Agent`와 `외부` 도구/데이터/서비스를 연결하기 위한 `표준 통신 규격`
  - github 공식 MCP
    - https://github.com/github/github-mcp-server
  - 그 외 오피셜 MCP 
    - 국내
      - https://playmcp.kakao.com/
      - ...
    - 해외 
      - ...
    - 서비스 주체별 MCP 제공
  - 장점
    - Agent <-> MCP 표준화 <-> 서비스 등 
      - 누가 만들어도 MCP 규격을 준수하면 어떤 LLM/Agent도 호환 가능하게 됨 
    - 각 서비스 주체들은 오피셜 MCP 개발하여 개방해줌. 
      - 서비스명 + MCP -> 확인 or MCP 커뮤니티/공인(포털) 사이트 검색 사용 -> 바로 적용됨
    - 사내용 MCP 없음 -> 비공개용, 사내용임 

- 참고
  - MCP 구성 요소
    | 구성 | 역할 | 현재 예제 |
    |---|---|---|
    | **MCP Host** | MCP를 사용하는 전체 애플리케이션 | LangChain Agent |
    | **MCP Client** | MCP Server와 통신 | `FastMCP Client` |
    | **MCP Server** | Tool을 외부에 제공 | `exchange_server.py` |