# 목표
- 앞 전 단계에서 프롬프트 -> 업무 수행(llm 호출)를 하나의 에이전트로 가정
- 에이전트를 여러 개 만들어서 협업 -> A2A 표현
- 랭체인의 체인 단위 구성을 n개 구성하여 서로 상호 다른 작업 진행토록 구성
- 순차적 협업 패턴 진행
  - 랭체인 완결되는 단위 -> 에이전트로 표현
  - 구성 (회차 제한)
    - 신입 개발자 에이전트 
    - 전문 리뷰어 에이전트 
    - 피드백 반영 에이전트 
  - 완성된 코드를 개발

# 구조
```
/
L steps
  L step5_a2a_basic.py
```

# 실행 (응답 토큰은 1200으로 제한됨)
```
python -m steps.step5_a2a_basic
---
목표 사용자 비밀번호를 입력받아 DB에 저장하는 간단한 함수 (보안 고려)
==================================================

[신입 개발자] 코드 작성 중...
---
 # 비밀번호 저장 함수 (bcrypt 해싱 적용)

```python
import bcrypt
import sqlite3

def hash_password(plain_password: str) -> bytes:
    """평문 비밀번호를 salt 포함하여 해싱"""
    salt = bcrypt.gensalt()  # 매번 랜덤 salt 생성
    h ... 
 (코드 생략) 
 ---

[전문 개발자] 코드 검토 중...
---
 # 코드 리뷰

전반적으로 bcrypt 사용법은 올바르지만, 실무에 배포하기엔 몇 가지 중요한 문제가 있습니다.

## 🔴 보안 문제

### 1. `username` 입력값 검증 부재
```python
if not plain_password or len(plain_password) < 8:
    raise ValueError(...)
```
비밀번호만 검증하고 `username`은 검증하지 않습니다. `None`, 빈 문자열, 과도하게 긴 문자열 등이 그대로 DB에 들어갈 수 있습니다.

**수정 제안:**
```python
if not username or not username.strip():
    raise ValueError("사용자명은 필수입니다.")
if len(username) > 50:
    raise ValueError("사용자명이 너무 깁니다.")
```

### 2. bcrypt 72바이트 제한 미처리
bcrypt는 **72바이트를 초과하는 비밀번호는 잘라서 처리**합니다. 긴 비밀번호를 입력해도 뒷부분이 무시되어 사용자가 인지하지 못한 보안 약화가 발생할 수 있습니다.

```python
if len(plain_password.encode('utf-8')) > 72:
    raise ValueError("비밀번호는 72바이트를 초과할 수 없습니다.")
```

### 3. 타이밍 사이드채널 — 사용자 존재 여부 노출
`verify_password`에서 사용자가 없으면 즉시 `return False`, 있으면 `checkpw` 연산(느림)을 수행합니다. 응답 시간 차이로 **사용자명 존재 여부를 추측(user enumeration)** 할 수 있습니다.

**수정 제안:**
```python
DUMMY_HASH = bcrypt.hashpw(b"dummy", bcrypt.gensalt())

def verify_password(username, input_password, db_path="users.db") -> bool:
    ...
    stored_hash = result[0] if result else DUMMY_HASH
    is_valid = bcrypt.checkpw(input_password.encode('utf-8'), stored_hash)
    return is_valid if result else False
```

### 4. 예외 정보 노출 위험
`print`로 성공/실패 메시지를 직접 출력하고 있는데, 이는 라이브러리 함수가 아니라 **로깅 시스템(logging 모듈)** 을 사용해야 합니다. 운영 환경에서 `print`는 로그 레벨 관리, 파일 기록 등이 불가능합니다.

## 🟡 비효율/구조 문제

### 5. `CREATE TABLE`을 매 저장마다 실행
`save_user_password` 호출마다 `CREATE TABLE IF NOT EXISTS`를 실행하는 것은 비효율적입니다. 스키마 초기화는 별도의 `init_db()` 함수로 분리해야 합니다.

### 6. DB 커넥션 관리 비효율
매 함수 호출마다 `sqlite3.connect`/`close`를 반복합니다. 트래픽이 많다면 커넥션 풀 또는 `with` 문 기반 컨텍스트 매니저 사용을 권장합니다.

```python
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    ...
```

### 7. `save_user_password`가 성공 여부를 반환하지 않음
현재 `None`을 반환하고  ... 


[신입 개발자] 피드백 반영하여 수정 중...
최종 결과물
```python
# 비밀번호 저장 함수 (bcrypt 해싱 적용) - 개선 버전

import bcrypt
import sqlite3
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 사용자 미존재 시에도 동일한 연산 시간을 유지하기 위한 더미 해시
_DUMMY_HASH = bcrypt.hashpw(b"dummy_password_for_timing_safety", bcrypt.gensalt())

MAX_USERNAME_LENGTH = 50
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_BYTES = 72  # bcrypt 제한


def init_db(db_path: str = "users.db") -> None:
    """DB 스키마 초기화 (앱 시작 시 한 번만 호출)"""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            )
        """)
        conn.commit()
    logger.info("DB 초기화 완료: %s", db_path)


def _validate_username(username: str) -> None:
    if not username or not username.strip():
        raise ValueError("사용자명은 필수입니다.")
    if len(username) > MAX_USERNAME_LENGTH:
        raise ValueError(f"사용자명은 {MAX_USERNAME_LENGTH}자를 초과할 수 없습니다.")


def _validate_password(plain_password: str) -> None:
    if not plain_password or len(plain_password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"비밀번호는 {MIN_PASSWORD_LENGTH}자 이상이어야 합니다.")
    if len(plain_password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValueError(f"비밀번호는 {MAX_PASSWORD_BYTES}바이트를 초과할 수 없습니다.")


def hash_password(plain_password: str) -> bytes:
    """평문 비밀번호를 salt 포함하여 해싱"""
    salt = bcrypt.gensalt()  # 매번 랜덤 salt 생성
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed


def save_user_password(username: str, plain_password: str, db_path: str = "users.db") -> bool:
    """
    사용자 이름과 비밀번호를 받아 해싱 후 DB에 저장

    - 평문 비밀번호는 절대 저장하지 않음
    - bcrypt는 자체적으로 salt를 포함하여 저장됨
    - 성공 시 True, 실패(중복 사용자 등) 시 