#  FastAPI 실습 가이드 

## 파일 구성

```
FastAPI
├── server.py          ← FastAPI 서버 (API 엔드포인트 정의)
├── CRUD.py            ← 클라이언트 (서버에 요청 보내기)
└── README.md               
```

---

##  환경 설정 (최초 1회)

아나콘다 base 환경 기준. VSCode 터미널에서 실행하세요.

```bash
pip install fastapi uvicorn httpx
```

> `requests`는 아나콘다 base에 이미 포함되어 있습니다.

---

##  실행 방법

**터미널을 2개** 열어야 합니다. VSCode에서 터미널 탭을 하나 더 추가하세요.

### 터미널 1 — 서버 실행

```bash
# fastapi 폴더로 이동 후 실행
cd fastapi
uvicorn server:app --reload
```

아래 메시지가 뜨면 서버가 정상 실행된 것입니다:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

> `--reload` 옵션: 코드를 수정하면 서버가 자동으로 재시작됩니다.

### 터미널 2 — 클라이언트 실행

```bash
# fastapi 폴더 안에서 실행
cd fastapi
python main_CRUD.py
```

---

##  접속 주소

| 주소 | 설명 |
|------|------|
| `http://localhost:8000` | API 서버 루트 |
| `http://localhost:8000/docs` | **Swagger UI** — 브라우저에서 직접 API 테스트 가능 |
| `http://localhost:8000/redoc` | ReDoc — 문서 형태로 보기 |
| `http://localhost:8000/items/` | 전체 상품 목록 |

>  **Swagger UI(`/docs`)를 꼭 열어보세요!** 코드 없이 브라우저에서 바로 API를 테스트할 수 있습니다.

---

## 📡 API 엔드포인트 목록

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 서버 상태 확인 |
| GET | `/items/` | 전체 상품 조회 |
| GET | `/items/{item_id}` | 특정 상품 조회 |
| POST | `/items/{item_id}` | 새 상품 생성 |
| PUT | `/items/{item_id}` | 상품 수정 |
| DELETE | `/items/{item_id}` | 상품 삭제 |
| GET | `/download-items-csv` | 상품 목록 CSV 다운로드 |

---

## 핵심 개념 요약

### Path Parameter vs Query Parameter

```python
# Path Parameter — URL 경로에 포함
GET /items/1          → item_id = 1

# Query Parameter — ? 뒤에 붙음
GET /items/?name=맥북  → name = "맥북"
```

### Pydantic 모델 (자동 데이터 검증)

```python
class Item(BaseModel):
    name: str        # 필수, 문자열만 허용
    price: float     # 필수, 숫자만 허용
    is_offer: bool | None = None  # 선택, 기본값 None
```

price에 `"abc"` 같은 문자열을 보내면 FastAPI가 자동으로 `422 Unprocessable Entity` 에러를 반환합니다.

### HTTP 상태 코드

| 코드 | 의미 |
|------|------|
| 200 | 성공 |
| 404 | 리소스를 찾을 수 없음 |
| 409 | 충돌 (이미 존재함) |
| 422 | 데이터 형식 오류 |
| 500 | 서버 내부 오류 |

---

##  서버 종료

터미널 1에서 `Ctrl + C`를 누르면 서버가 종료됩니다.

> ⚠️ 서버를 종료하면 추가/수정/삭제한 데이터가 모두 초기화됩니다.  
> (인메모리 DB이기 때문. 다음 시간에 실제 DB 연동을 배웁니다.)
