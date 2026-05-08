# FastAPI + Gradio 웹 서비스 배포

## 1. 전체 구조

학습된 `.pkl` 모델을 실제 웹에서 쓸 수 있게 만드는 과정이다.

```
[사용자]
   ↓ 슬라이더 조작
[Gradio UI]  →  requests.post()  →  [FastAPI]  →  model.predict()
                                         ↓
                                   { species, confidence }
```

---

## 2. FastAPI 핵심 개념

### Pydantic BaseModel — 입출력 타입 정의

FastAPI는 `BaseModel`로 요청/응답의 구조를 미리 정의한다.  
타입이 맞지 않으면 자동으로 422 에러를 돌려주고, `/docs`에 문서도 자동 생성된다.

```python
from pydantic import BaseModel

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
```

### 엔드포인트 정의

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict/")
def predict(features: IrisFeatures):
    data = [[features.sepal_length, features.sepal_width,
             features.petal_length, features.petal_width]]

    pred  = model.predict(data)[0]
    proba = model.predict_proba(data)[0]

    return {
        "species":    iris_names[pred],
        "confidence": float(max(proba))   # ← 반드시 float() 변환!
        # numpy의 float32는 JSON 직렬화 불가 → python float으로 변환
    }
```

### 실행 명령어
```bash
uvicorn api:app --reload --port 8000
# api     : 파일명 (api.py)
# app     : FastAPI 인스턴스 변수명
# --reload: 코드 변경 시 자동 재시작 (개발용)
```

---

## 3. Gradio UI 핵심 개념

Gradio는 슬라이더, 버튼, 텍스트박스 같은 UI를 코드 몇 줄로 만들어준다.

```python
import gradio as gr

def predict_species(sl, sw, pl, pw):
    # FastAPI 호출
    payload = {"sepal_length": sl, "sepal_width": sw,
               "petal_length": pl, "petal_width": pw}
    response = requests.post("http://127.0.0.1:8000/predict/", json=payload)
    result = response.json()
    return f"{result['species']} ({result['confidence']*100:.1f}%)"

iface = gr.Interface(
    fn=predict_species,                  # 실행할 함수
    inputs=[
        gr.Slider(4.0, 8.0, label="Sepal Length"),
        gr.Slider(2.0, 4.5, label="Sepal Width"),
        gr.Slider(1.0, 7.0, label="Petal Length"),
        gr.Slider(0.1, 2.5, label="Petal Width"),
    ],
    outputs=gr.Textbox(label="예측 결과"),
)
iface.launch()
```

---

## 4. 배포 방식 2가지 비교

### 방식 A — 분리 서버 (api.py + app_gradio.py)

```
터미널 1: uvicorn api:app --reload --port 8000
터미널 2: python app_gradio.py
```

- FastAPI: 백엔드 전용 (포트 8000)
- Gradio: 프론트엔드 전용 (포트 7860), requests로 API 호출
- 장점: 역할 분리 명확, 프론트를 Streamlit 등으로 교체하기 쉬움
- 단점: 서버 2개 관리 필요

### 방식 B — 단일 서버 (main_gradio_mount.py) 

```
터미널 1개: python main_gradio_mount.py
```

```python
app = gr.mount_gradio_app(app, demo, path="/gradio")
# http://localhost:8000/gradio     → Gradio UI
# http://localhost:8000/docs       → API 자동 문서 (Swagger)
# http://localhost:8000/api/predict → REST API
```

- 장점: 서버 1개, 배포 간단
- 단점: UI와 API 코드가 한 파일에 섞임

---

## 5. 실행 순서 (방식 B 기준)

```bash
# 1. 모델 학습 (최초 1회)
python train_model.py       # iris_model.pkl 생성

# 2. 통합 서버 실행
python main_gradio_mount.py

# 3. 브라우저에서 확인
# http://127.0.0.1:8000/gradio  → UI
# http://127.0.0.1:8000/docs    → API 문서
```

---

## 6. 자주 하는 실수

| 실수 | 원인 | 해결 |
|------|------|------|
| `iris_model.pkl not found` | train_model.py 미실행 | 먼저 train_model.py 실행 |
| JSON 직렬화 에러 | numpy float 반환 | `float()` 로 변환 |
| 연결 거부 에러 | FastAPI 서버 미실행 | uvicorn 먼저 실행 |
| 422 에러 | 요청 key 이름 불일치 | Pydantic 모델 필드명 확인 |
