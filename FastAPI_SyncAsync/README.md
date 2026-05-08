# FastAPI 기초 및 동기/비동기 실습

> **환경**: Anaconda Base (Python 3.10+) + VSCode

---

## 파일 구성

| 파일 | 설명 |
|------|------|
| `sync_async_tutorial.ipynb` | 동기/비동기 개념 실습 — requests vs aiohttp, asyncio.gather, Semaphore |
| `FastAPI/server.py` | FastAPI CRUD 서버 — GET / POST / PUT / DELETE / CSV 다운로드 |
| `FastAPI/client.py` | FastAPI 클라이언트 — server.py에 실제 요청을 보내는 테스트 스크립트 |


---

## 학습 내용

### 1. 동기 vs 비동기 (Sync / Async)
- `requests` 동기 방식 vs `aiohttp` + `asyncio` 비동기 방식 파일 다운로드 성능 비교
- `async def`, `await`, `asyncio.gather()` 핵심 개념 이해
- `asyncio.Semaphore()`로 동시 요청 수 제한하기
- Jupyter/Colab 환경 vs 일반 .py 스크립트 실행 방법 차이

### 2. FastAPI 기초
- `@app.get()`, `@app.post()` 등 데코레이터로 엔드포인트 정의
- Path Parameter (`/items/{item_id}`) vs Query Parameter (`/items/?name=맥북`)
- Pydantic `BaseModel`을 이용한 Request Body 자동 유효성 검사
- `HTTPException`으로 404, 409 등 에러 응답 처리

### 3. CRUD API 구현
- **Create** — POST로 새 상품 생성
- **Read** — GET으로 전체/단일 상품 조회
- **Update** — PUT으로 상품 정보 수정
- **Delete** — DELETE로 상품 삭제
- **CSV 다운로드** — `StreamingResponse`로 데이터를 파일로 내보내기

### 4. HTTP 통신 클라이언트
- `requests` — 동기 방식 HTTP 클라이언트 (가장 일반적)
- `httpx` — 동기 + 비동기 모두 지원, FastAPI 공식 추천 라이브러리

---

## 실행 방법

### 환경 설정 (최초 1회)

```bash
pip install fastapi uvicorn httpx
```

### 서버 + 클라이언트 실행

VSCode에서 터미널을 **2개** 열고 실행하세요.

```bash
# 터미널 1 — 서버 실행
cd FastAPI
uvicorn server:app --reload

# 터미널 2 — 클라이언트 실행
cd FastAPI
python client.py
```

서버 실행 후 브라우저에서 **`http://localhost:8000/docs`** 를 열면 Swagger UI로 API를 직접 테스트할 수 있습니다.

---

## 실행 환경

```
Python      3.10+
fastapi
uvicorn
httpx
requests    (Anaconda base 기본 포함)
aiohttp
beautifulsoup4
```
