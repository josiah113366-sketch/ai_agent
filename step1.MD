# 목표
- 프로젝트 구조 기초 완성 (뼈대 구성)

# 구조
/
L app/              : 모듈 파일, 실제 코드 
  L __init__.py
L steps/            : 각 단계별 테스트 코드, 추가 코드 
  L step1_check.py  : 1단계 점검용 
L scripts/          : 환경 설정, 관리, 실행 등 보조 도구 
  L doctor.py       : git, docker, aws cli 진단 도구 
L step1.MD          : step1 설명

# 테스트 
- doctor.py
```
파이썬 : 3.12.10
git        C:\Program Files\Git\cmd\git.EXE
docker     C:\Program Files\Docker\Docker\resources\bin\docker.EXE
aws        C:\Program Files\Amazon\AWSCLIV2\aws.EXE
```