<<<<<<< HEAD
## ML Model Web Service Deployment

머신러닝 모델을 학습하고 FastAPI + Gradio로 웹 서비스로 배포하는 전체 과정을 정리한다.

---

## 폴더 구조

```
ml_web_service/
├── README.md                              ← 이 파일
│
├── decision_tree_ensemble/
│   ├── study_notes.md                     ← Decision Tree & Ensemble 이론 정리
│   └── train_model.py                     ← Random Forest 학습 + pkl 저장
│
├── fastapi_gradio_deployment/
│   ├── study_notes.md                     ← FastAPI + Gradio 배포 개념 정리
│   ├── api.py                             ← FastAPI 서버 (분리 방식)
│   ├── app_gradio.py                      ← Gradio 클라이언트 (분리 방식)
│   └── main_gradio_mount.py               ← FastAPI + Gradio 통합 서버
│
└── dependency_injection/
    ├── study_notes.md                     ← DI 개념 정리
    └── di_example.py                      ← DI 예제 (공통 파라미터, DB 세션, 인증)
```

---

## 실행 순서

### Part 1 — 모델 학습
```bash
cd decision_tree_ensemble
python train_model.py
# → iris_model.pkl 생성됨
```

### Part 2 — 웹 서비스 (통합 서버 방식)
```bash
cd fastapi_gradio_deployment
cp ../decision_tree_ensemble/iris_model.pkl .
python main_gradio_mount.py
# http://127.0.0.1:8000/gradio  → UI
# http://127.0.0.1:8000/docs    → API 문서
```

### Part 2 — 웹 서비스 (분리 서버 방식)
```bash
# 터미널 1
uvicorn api:app --reload --port 8000

# 터미널 2
python app_gradio.py
```

### Part 3 — DI 예제
```bash
cd dependency_injection
uvicorn di_example:app --reload --port 8001
# http://127.0.0.1:8001/docs 에서 테스트
```

---

## 핵심 개념 요약

| 파트 | 핵심 키워드 | 한 줄 요약 |
|------|------------|-----------|
| Part 1 | Random Forest, Ensemble | 약한 모델 여럿 → 강한 모델 하나보다 낫다 |
| Part 2 | FastAPI, Gradio, pickle | 모델을 저장하고 API로 감싸서 UI에서 호출 |
| Part 3 | Depends, yield | 공통 로직을 주입받아 코드 중복 제거 |

---

## 의존 패키지 설치

```bash
pip install scikit-learn fastapi uvicorn gradio requests sqlalchemy xgboost lightgbm
```
---

© 2026 Jiwon Lee. All rights reserved.

