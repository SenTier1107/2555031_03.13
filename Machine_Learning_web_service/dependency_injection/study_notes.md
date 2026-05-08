# Dependency Injection (의존성 주입)

## 1. 의존성 주입이란?

> 객체가 필요한 것(의존성)을 **직접 만들지 않고, 외부에서 받아서** 쓰는 패턴

### DI 없이 — 반복 코드 문제

```python
@app.get("/users/")
def get_users():
    db = connect_db()     # ← 매번 반복
    auth_check()          # ← 매번 반복
    return db.query(User).all()

@app.get("/items/")
def get_items():
    db = connect_db()     # ← 또 반복
    auth_check()          # ← 또 반복
    return db.query(Item).all()
```

### DI 사용 — Depends로 주입

```python
from fastapi import Depends
from typing import Annotated

# 의존성 함수 한 번만 정의
def get_db():
    db = SessionLocal()
    try:
        yield db       # 요청 처리 중엔 db가 열려 있음
    finally:
        db.close()     # 응답이 나가면 자동으로 닫힘

# 각 함수에서 Depends로 주입받기만 하면 됨
@app.get("/users/")
def get_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()

@app.get("/items/")
def get_items(db: Annotated[Session, Depends(get_db)]):
    return db.query(Item).all()
```

---

## 2. yield를 쓰는 이유 — 제너레이터 패턴

`yield`는 함수 실행을 중간에 멈추고 값을 넘겨주는 문법이다.

```python
def get_db():
    db = SessionLocal()   # ① DB 연결 (요청 들어올 때)
    try:
        yield db          # ② 요청 처리 함수에 db 전달 후 대기
    finally:
        db.close()        # ③ 응답 후 자동 실행 (세션 닫기)
```

실행 흐름:
```
요청 들어옴
  → get_db() 시작 → DB 연결
  → yield → 라우터 함수 실행
  → 응답 반환
  → finally 블록 실행 → DB 닫힘
```

---

## 3. 공통 파라미터 재사용 예시

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

# 공통 쿼리 파라미터 묶기
async def common_params(
    q:     str | None = None,   # 검색어 (선택)
    skip:  int = 0,             # 건너뛸 개수
    limit: int = 100,           # 최대 반환 개수
):
    return {"q": q, "skip": skip, "limit": limit}

# /items?q=apple&skip=0&limit=10
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_params)]):
    return commons   # {"q": "apple", "skip": 0, "limit": 10}

# /users?skip=5
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_params)]):
    return commons   # {"q": null, "skip": 5, "limit": 100}
```

---

## 4. Streamlit + FastAPI Client-Server 구조

| 역할 | 담당 | 설명 |
|------|------|------|
| View (화면) | Streamlit | 사용자가 보는 UI |
| Control (로직) | FastAPI | 비즈니스 로직 처리 |
| Model (데이터) | DB + Depends | 데이터 저장/조회 |

```python
# Streamlit (frontend) — FastAPI를 requests로 호출
import streamlit as st
import requests

st.title("Iris 예측")
sl = st.slider("Sepal Length", 4.0, 8.0, 5.1)

if st.button("예측"):
    response = requests.post(
        "http://127.0.0.1:8000/predict/",
        json={"sepal_length": sl, ...}
    )
    result = response.json()
    st.success(result["species"])
```

---

## 5. DI를 써야 하는 상황 정리

| 상황 | DI 적용 |
|------|---------|
| DB 세션 (요청마다 열고 닫기) | `Depends(get_db)` |
| 인증 토큰 검증 | `Depends(verify_token)` |
| 공통 쿼리 파라미터 | `Depends(common_params)` |
| 설정 파일 로드 | `Depends(get_settings)` |
| 캐시 / 외부 API 클라이언트 | `Depends(get_client)` |

---

## 6. 핵심 정리

- `Depends()` — 의존성 함수를 주입받는 FastAPI 클래스
- `yield` 있는 의존성 함수 — 요청 전/후로 리소스 자동 관리 (DB, 파일 등)
- `Annotated[타입, Depends(함수)]` — 최신 FastAPI 권장 작성법
- 테스트할 때 의존성을 mock으로 교체하기 쉬워서 단위 테스트가 편해진다
