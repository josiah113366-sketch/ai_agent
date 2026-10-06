'''
- 에이전트가 툴 사용 시 제한 사항, 정책 등 반영
'''

# 리소스 한도 -> dataclass 데커레이터 사용
from dataclasses import dataclass
# 시간 한도 
import time 
# 툴 사용 한도 -> 툴 사용 목록 제한 -> 툴을 제한을 하면 -> 도구 제한을 받음 
ALLOWED_TOOLS = {"sales_summary", "top_products", "refund_summary", "search_company_policy", "remember_user_preference", "recall_user_memory", "get_exchange_rate"}
