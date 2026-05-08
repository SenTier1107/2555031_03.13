"""
[Part 3 실습] FastAPI 의존성 주입 (Dependency Injection) 예제

주요 패턴:
1. 공통 쿼리 파라미터 재사용
2. DB 세션 자동 관리 (yield 패턴)
3. 인증 토큰 검증

실행: uvicorn di_example:app --reload --port 8001
테스트: http://127.0.0.1:8001/docs
"""

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

app = FastAPI(title="DI 예제")

# ── 예제 1. 공통 쿼리 파라미터 재사용 ─────────────────────
async def common_params(
    q:     str | None = None,
    skip:  int = 0,
    limit: int = 100,
):
    """여러 엔드포인트에서 공통으로 쓰는 파라미터를 묶은 의존성 함수"""
    return {"q": q, "skip": skip, "limit": limit}

# Annotated[타입, Depends(함수)] — 최신 FastAPI 권장 방식
CommonDep = Annotated[dict, Depends(common_params)]

@app.get("/items/")
async def read_items(commons: CommonDep):
    # GET /items?q=apple&skip=0&limit=10
    return {"endpoint": "items", **commons}

@app.get("/users/")
async def read_users(commons: CommonDep):
    # GET /users?skip=5
    return {"endpoint": "users", **commons}


# ── 예제 2. DB 세션 자동 관리 (yield 패턴) ─────────────────
DATABASE_URL = "sqlite:///./test.db"
engine       = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)   # 테이블 생성

def get_db():
    """
    요청마다 DB 세션을 열고, 응답 후 자동으로 닫는 의존성 함수.

    yield를 쓰는 이유:
    - yield 이전: 요청 시작 시 실행 (DB 연결)
    - yield:      라우터 함수에 db 객체 전달
    - finally:    응답 후 항상 실행 (DB 닫기)
    """
    db = SessionLocal()
    try:
        yield db           # ← 여기서 라우터 함수 실행됨
    finally:
        db.close()         # ← 응답 후 항상 실행

DbDep = Annotated[Session, Depends(get_db)]

@app.get("/db-items/")
def read_db_items(db: DbDep):
    return db.query(Item).all()

@app.post("/db-items/")
def create_item(name: str, db: DbDep):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# ── 예제 3. 인증 토큰 검증 ────────────────────────────────
VALID_TOKEN = "secret-token-1234"

def verify_token(x_token: Annotated[str, Header()]):
    """
    요청 헤더의 X-Token 값을 검증하는 의존성 함수.
    Header()로 헤더 값을 자동으로 파라미터에 바인딩한다.
    """
    if x_token != VALID_TOKEN:
        raise HTTPException(status_code=403, detail="유효하지 않은 토큰")
    return x_token

@app.get("/secure/")
def secure_endpoint(token: Annotated[str, Depends(verify_token)]):
    # curl -H "x-token: secret-token-1234" http://127.0.0.1:8001/secure/
    return {"message": "인증 성공!", "token": token}


# ── 실행 ───────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
