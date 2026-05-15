---
title: Wine FastAPI Gradio Dashboard
emoji: 🍷
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
---

# 🍷 Wine Classification Dashboard

FastAPI와 Gradio를 결합한 이탈리아 와인 품종 분류 웹 서비스입니다.  
scikit-learn의 `load_wine` 데이터셋을 기반으로 RandomForest 모델을 학습하고,  
화학적 성분 입력만으로 와인 품종을 예측합니다.

---

## 📌 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 데이터셋 | scikit-learn `load_wine` (178개 샘플, 13개 피처) |
| 분류 대상 | Barolo (class_0) / Grignolino (class_1) / Barbera (class_2) |
| 모델 | RandomForestClassifier (n_estimators=100) |
| 테스트 정확도 | 100% |
| 예측 방식 | 상위 6개 피처 입력 → 나머지 7개는 평균값 자동 대체 |

---

## 🚀 실행 방법

### 로컬 실행

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 모델 학습 및 저장
python train_wine_model.py

# 3. 서버 실행
python app.py
```

### 접속 주소

| 경로 | 설명 |
|------|------|
| `http://localhost:7860/gradio` | Gradio UI |
| `http://localhost:7860/docs` | FastAPI Swagger 문서 |
| `http://localhost:7860/api/predict` | 예측 API 엔드포인트 |

### Docker 실행

```bash
docker build -t wine-dashboard .
docker run -p 7860:7860 wine-dashboard
```

---

## 🗂️ 탭 기능 소개

### 탭 1 — 데이터 조회
- 178개 전체 샘플을 테이블로 조회
- class_0 / class_1 / class_2 클래스별 필터링 가능

### 탭 2 — 피처 중요도
- RandomForest 기반 변수 중요도 시각화 (다크 테마 차트)
- 개별 중요도 막대 + 누적 중요도 꺾은선 동시 표시
- 상위 6개 변수 기준선 (누적 80.7%) 표시
- 요약 카드: 전체 변수 수 / 예측 사용 변수 수 / 누적 설명력

### 탭 3 — 품종 예측
- 중요도 상위 6개 변수 슬라이더 입력으로 품종 예측
- 예측 품종 + 확신도 + 품종 설명 출력
- 클래스별 확률 텍스트 바 시각화
- 예시 데이터 클릭으로 자동 입력 가능

---

## 📊 피처 중요도 분석 결과

| 순위 | 피처 | 중요도 | 누적 |
|------|------|--------|------|
| 1 | flavanoids | 20.2% | 20.2% |
| 2 | color_intensity | 17.1% | 37.3% |
| 3 | proline | 13.9% | 51.3% |
| 4 | alcohol | 11.2% | 62.5% |
| 5 | od280/od315_of_diluted_wines | 11.2% | 73.7% |
| 6 | hue | 7.1% | **80.7%** ← 예측에 사용 |
| 7~13 | 나머지 7개 | 19.3% | 100% |

> 상위 6개 변수만으로 전체 설명력의 **80.7%** 를 커버합니다.

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| ML | scikit-learn (RandomForestClassifier) |
| Backend | FastAPI, Uvicorn |
| Frontend | Gradio (FastAPI에 마운트) |
| 데이터 처리 | NumPy, Pandas |
| 시각화 | Matplotlib, Pillow |
| 컨테이너 | Docker |

---

## 📁 파일 구조

```
├── app.py                 # FastAPI + Gradio 통합 서버
├── train_wine_model.py    # 모델 학습 및 저장
├── wine_model.pkl         # 학습된 모델 (train 후 생성)
├── requirements.txt       # 패키지 목록
├── Dockerfile             # Docker 설정
└── README.md
```

---

## 🍷 와인 클래스 설명

| 클래스 | 품종 | 특징 |
|--------|------|------|
| class_0 | **Barolo (바롤로)** | 풀바디 고급 레드와인. 알코올과 프롤린 함량이 높고 색이 진함. |
| class_1 | **Grignolino (그리뇰리노)** | 미디엄바디 레드와인. 페놀 함량이 중간이며 균형 잡힌 특성. |
| class_2 | **Barbera (바르베라)** | 산도 높은 레드와인. 말산과 색 강도가 높은 편. |

> 📌 데이터 출처: UCI ML Repository — 이탈리아 동일 지역의 세 품종 와인 178개 샘플
