'''
fastapi 기반 에이전트 서비스
'''
# 1. 모듈 가져오기 
from fastapi import FastAPI
from pydantic import BaseModel
from app.main import invoke_agent