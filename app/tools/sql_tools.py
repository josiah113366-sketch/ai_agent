'''
- 데이터베이스를 대상으로 특정 데이터를 추출, 작업하는 sql 도구 구성
- 패턴화된 작업을 도구화하여 에이전트가 자율적으로 사용하도록 구성 
'''
from langchain_core.tools import tool 
from app.database import connect 

@tool
def sales_summary(start_date: str, end_date: str) -> str: 
  '''
    특정 날짜 범위(YYYY-MM-DD) 내에서 결제 완료 매출과 주문 건수를 조회한다 -> 집계 
  '''
  with connect() as conn, conn.cursor() as cur: 
    sql = """

    """
    params = () 
    cur.execute(sql, params)
    revenue, count = cur.fetchone() 
  return f"revenue={revenue}, orders={count}, range={start_date}~{end_date}"

@tool
def top_products(start_date: str, end_date: str, limit:int=3) -> str: 
  '''
    특정 날짜 범위(YYYY-MM-DD) 내에서 결제 완료된 매출 기준 상위 제품 조회
    제품명(name), 수량(qty), 매출액(revenue)를 추출한다
  '''
  with connect() as conn, conn.cursor() as cur: 
    sql = """
      
    """
    params = () 
    cur.execute(sql, params)
    rows = cur.fetchall() 
  return "\n".join( f"{i+1}. {name}: qty={qty}, revenue={revenue} " for i, (name, qty, revenue) in enumerate( rows ) )