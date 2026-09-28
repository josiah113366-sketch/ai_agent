'''
구동 환경 체크 
'''
import platform
import sys

print(f'Python : ', sys.version.split()[0])
print(f'Platform : ', platform.platform())
print('환경 준비 완료')