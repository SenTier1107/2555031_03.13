"""
[Part 2 실습] FastAPI로 Iris 예측 API 서버 만들기
- Pydantic BaseModel로 입력 타입 정의
- pickle로 저장된 모델 불러와서 예측
- 실행: uvicorn api:app --reload --port 8000
- API 문서: http://127.0.0.1:8000/docs
"""

import pickle
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris

# ── 1. 모델 로드 ───────────────────────────────────────────
# 서버 시작 시 딱 한 번만 로드 (요청마다 로드하면 느려짐)
try:
    with open("iris_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ 모델 로드 완료")
except FileNotFoundError:
    print("❌ train_model.py를 먼저 실행하세요!")
    model = None

iris_names = load_iris().target_names   # ['setosa' 'versicolor' 'virginica']

# ── 2. FastAPI 인스턴스 생성 ───────────────────────────────
app = FastAPI(title="Iris Prediction API", version="1.0.0")

# ── 3. 입력 스펙 정의 (Pydantic BaseModel) ─────────────────
# 요청 body의 구조를 미리 선언
# 타입이 맞지 않으면 FastAPI가 자동으로 422 에러 반환
# /docs 페이지에서 이 모델을 기반으로 테스트 UI 자동 생성됨
class IrisFeatures(BaseModel):
    sepal_length: float   # 꽃받침 길이 (cm)
    sepal_width:  float   # 꽃받침 너비 (cm)
    petal_length: float   # 꽃잎 길이 (cm)
    petal_width:  float   # 꽃잎 너비 (cm)

# ── 4. 예측 엔드포인트 ─────────────────────────────────────
@app.post("/predict/")
def predict_iris(features: IrisFeatures):
    if model is None:
        return {"error": "모델 로드 실패. train_model.py를 먼저 실행하세요."}

    # 2D 배열 형태로 변환 (sklearn은 항상 2D 입력을 요구)
    data_in = [[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]]

    prediction = model.predict(data_in)[0]            # 예측 클래스 인덱스
    proba      = model.predict_proba(data_in)[0]      # 각 클래스 확률

    return {
        "species":    str(iris_names[prediction]),    # 품종 이름
        "confidence": float(np.max(proba)),           # 가장 높은 확률
        # ↑ numpy float32 → python float 변환 (JSON 직렬화 필수)
    }

# ── 5. 헬스 체크 엔드포인트 ───────────────────────────────
# 서버가 살아있는지 확인하는 용도
@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

# 실행: uvicorn api:app --reload --port 8000
