# FastAPI 입문을 위한 파이썬 핵심 개념

> **환경**: Google Colab (Python 3.10+)

---

##  파일 구성

| 파일 | 설명 |
|------|------|
| `Python_Backend_Essentials_for_FastAPI.ipynb` | 개념 정리 보고서 — 데코레이터, 타입 힌트, Pydantic, SQLite3, Async, Gradio |
| `04_17_실습과제.ipynb` | 04/17 실습과제 정리 — SQLite3 CRUD, 모듈화 리팩토링, Pydantic 변환 |
| `gradio_crud.ipynb` | 추가 실습과제 1 Gradio CRUD 대시보드 |

---

##  학습 내용

### 1. 데코레이터 (Decorator)
- 함수를 인자로 받아 기능을 추가하거나 변형하는 함수
- `@register` 문법으로 함수 정의 시점에 자동 등록
- FastAPI, Flask의 `@app.get("/")` 라우팅에 동일하게 활용

### 2. 타입 힌트 (Type Hints)
- 변수·함수 인자·반환값에 타입을 명시하는 Python 3.5+ 문법
- `list[T]`, `dict[K, V]`, `Optional`, `Union` 등 컬렉션 타입
- FastAPI 코드의 80%를 차지하는 핵심 개념

### 3. Pydantic
- `BaseModel`을 통한 런타임 데이터 유효성 검사 및 자동 타입 변환
- `dataclass`와의 차이점 비교 — 런타임 검증 여부
- FastAPI 요청/응답 스키마 정의에 직접 활용

### 4. SQLite3 CRUD
- 별도 서버 없이 파일 하나로 동작하는 경량 DB
- `connect` → `cursor` → `execute` → `commit` 흐름
- Create / Read / Update / Delete 전체 실습

### 5. SQLite3 + Pydantic 연동
- `row_factory = sqlite3.Row`로 dict처럼 접근
- `model_validate(dict(row))`로 DB Row → Pydantic 모델 변환
- 도트 연산자(`user.name`)로 안전한 데이터 접근

### 6. 동기 vs 비동기 (Sync / Async)
- `requests` 동기 방식 vs `aiohttp` + `asyncio` 비동기 방식 다운로드 성능 비교
- `async/await`, `asyncio.gather()` 핵심 개념
- 33개 파일 순차 처리 vs 동시 처리 소요 시간 비교

### 7. Gradio UI
- 파이썬 함수를 단 몇 줄로 웹 UI로 변환
- 텍스트 입출력, 이미지 흑백 변환, 대문자 변환 예제
- ngrok을 통한 외부 공개 URL 생성 및 모바일 접속

---

##  실습과제

### 실습과제 1 — CSV → SQLite3 CRUD
`customers.csv`를 읽어와 DB를 만들고 `customers` 테이블에 CRUD 구현

### 실습과제 2 — 모듈화 리팩토링
실습과제 1 코드를 `init.py`, `create.py`, `read.py`, `update.py`, `delete.py`로 모듈화

### 실습과제 3 — CSV → Pydantic 저장
`customers.csv`를 읽어와 Pydantic 모델로 변환 및 저장

---

## Gradio CRUD Dashboard (`gradio_crud.py`)

`customers.csv` 기반 SQLite3 DB를 Gradio UI로 조작하는 대시보드

**탭 구성**

| 탭 | 기능 |
|----|------|
| ➕ Create | 고객ID 자동 배정, 드롭다운 선택, Pydantic 유효성 검사 |
| 🔍 Read | 고객ID · 거주지 · 회원등급 · 성별 검색 및 전체 조회 |
| ✏️ Update | 고객ID 입력 → 불러오기 → 수정 |
| 👋 Greet | 고객ID 입력 → `Hello, CUST_XXXX!` 인사말 출력 |
| 🗑️ Delete | 고객ID 입력 → 삭제 |

**유효성 검사 (Pydantic)**
- 텍스트 항목(성별·결제수단·거주지·회원등급)에 숫자 입력 시 오류 메시지 출력
- 만족도 1~5 범위 초과 시 안내 메시지 출력
- 빈값 입력 시 오류 메시지 출력

**실행 방법**
```bash
# 패키지 설치
pip install gradio pydantic pandas

# 실행
python gradio_crud.py
```

---

##  실행 환경

```
Python      3.10+
gradio
pydantic    v2
pandas
aiohttp
sqlite3     (Python 표준 라이브러리)
```
