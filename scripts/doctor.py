'''
개발 환경 체크용 
- 추후 필요 시 계속 추가될 수 있음 
'''
import shutil
import sys

commands = ['git','docker','aws']

# 체크 
print(f'파이썬 : {sys.version.split()[0]}') 
for cmd in commands: 
  print(f'{cmd:10s}', shutil.which(cmd) or 'not found') 