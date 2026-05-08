"""
[Part 2 실습 - 심화] FastAPI + Gradio 단일 서버
- gr.mount_gradio_app()으로 Gradio를 FastAPI 안에 합친다
- 서버 1개로 UI + API + 문서를 모두 제공
- 실행: python main_gradio_mount.py

접속 주소:
  http://127.0.0.1:8000/gradio      → Gradio UI
  http://127.0.0.1:8000/docs        → Swagger API 문서
  http://127.0.0.1:8000/api/predict → REST API
"""

import pickle
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
import gradio as gr
import uvicorn

# ── 1. 모델 로드 ───────────────────────────────────────────
MODEL_PATH = "iris_model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ 모델 로드 완료")
except FileNotFoundError:
    print(f"❌ '{MODEL_PATH}' 없음. train_model.py를 먼저 실행하세요.")
    model = None

iris_names = load_iris().target_names

# ── 2. FastAPI 앱 생성 ─────────────────────────────────────
app = FastAPI(title="Iris Service (통합 서버)")

class IrisFeatures(BaseModel):
    sl: float   # sepal_length
    sw: float   # sepal_width
    pl: float   # petal_length
    pw: float   # petal_width

# ── 3. 예측 로직 (API와 Gradio가 함께 사용) ────────────────
# 하나의 함수를 두 곳에서 재사용 → 코드 중복 제거
def get_prediction(sl, sw, pl, pw):
    if model is None:
        return {"error": "모델 없음"}
    data_in    = [[sl, sw, pl, pw]]
    prediction = model.predict(data_in)[0]
    proba      = model.predict_proba(data_in)[0]
    return {
        "species":    str(iris_names[prediction]),
        "confidence": float(np.max(proba)),
    }

# ── 4. REST API 엔드포인트 ─────────────────────────────────
@app.post("/api/predict")
def predict_api(features: IrisFeatures):
    return get_prediction(features.sl, features.sw, features.pl, features.pw)

# ── 5. Gradio UI 함수 ──────────────────────────────────────
def predict_ui(sl, sw, pl, pw):
    result = get_prediction(sl, sw, pl, pw)
    if "error" in result:
        return f"❌ {result['error']}"
    species    = result["species"].capitalize()
    confidence = result["confidence"] * 100
    return f"예측 품종: {species}\n확신도: {confidence:.2f}%"

# ── 6. Gradio 인터페이스 정의 (gr.Blocks 방식) ─────────────
# gr.Blocks: gr.Interface보다 레이아웃 자유도가 높다
with gr.Blocks(title="붓꽃 예측 서비스") as demo:
    gr.Markdown("# 🌸 붓꽃 품종 예측 서비스")

    with gr.Row():
        with gr.Column():
            sl  = gr.Slider(4.0, 8.0, step=0.1, value=5.1, label="꽃받침 길이 (cm)")
            sw  = gr.Slider(2.0, 4.5, step=0.1, value=3.5, label="꽃받침 너비 (cm)")
            pl  = gr.Slider(1.0, 7.0, step=0.1, value=1.4, label="꽃잎 길이 (cm)")
            pw  = gr.Slider(0.1, 2.5, step=0.1, value=0.2, label="꽃잎 너비 (cm)")
            btn = gr.Button("예측하기", variant="primary")
        with gr.Column():
            output = gr.Textbox(label="예측 결과", lines=3)

    gr.Examples(
        examples=[[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3], [5.9, 3.0, 4.2, 1.5]],
        inputs=[sl, sw, pl, pw],
    )

    btn.click(fn=predict_ui, inputs=[sl, sw, pl, pw], outputs=output)

# ── 7. Gradio를 FastAPI에 마운트 ──────────────────────────
# /gradio 경로 아래에 Gradio 앱을 붙인다
# 이 줄 이후로 app 변수가 Gradio가 감싼 새 FastAPI 인스턴스가 됨
app = gr.mount_gradio_app(app, demo, path="/gradio")

# ── 8. 서버 실행 ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 서버 시작!")
    print("  Gradio UI : http://127.0.0.1:8000/gradio")
    print("  API 문서  : http://127.0.0.1:8000/docs")
    print("  API       : http://127.0.0.1:8000/api/predict")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)
