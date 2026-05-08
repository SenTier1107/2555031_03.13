## Decision Tree & Ensemble Learning _ ( STUDY_NOTES )

## 1. Decision Tree

의사결정 트리는 데이터를 **조건(질문)** 으로 계속 나눠서 분류하는 모델이다.

```
꽃잎 길이 > 2.5?
├── Yes → 꽃잎 너비 > 1.8?
│         ├── Yes → Virginica
│         └── No  → Versicolor
└── No  → Setosa
```

### Pruning (가지치기)

트리가 너무 깊어지면 훈련 데이터에만 딱 맞는 **과적합(Overfitting)** 이 발생한다.  
`max_depth`로 깊이를 제한하는 것이 해결책이다.

| depth | 상태 |
|-------|------|
| 1 (Stump) | Underfitting — 너무 단순 |
| 4~5 | 적당 |
| None (제한 없음) | Overfitting — 훈련 데이터 암기 |

```python
from sklearn.tree import DecisionTreeClassifier

dt_under = DecisionTreeClassifier(max_depth=1)   # Underfitting
dt_good  = DecisionTreeClassifier(max_depth=4)   # 적당
dt_over  = DecisionTreeClassifier()               # Overfitting (제한 없음)
```

---

## 2. 앙상블 (Ensemble) — 왜 여러 모델을 합치나?

### 콩도르세 배심원 정리 (Condorcet's Jury Theorem)

> 각자 55% 정확도를 가진 배심원이 101명이면, 다수결의 정확도는 97%를 넘는다.

→ **약한 모델 여럿 > 강한 모델 하나**

```python
from scipy.stats import binom

p = 0.55
for n in [1, 5, 11, 51, 101]:
    prob = sum(binom.pmf(k, n, p) for k in range(n // 2 + 1, n + 1))
    print(f"배심원 {n:3d}명 → 다수결 정확도: {prob:.4f}")
```

---

## 3. 앙상블 3종 비교

### Bagging
- 훈련 데이터를 무작위로 **복원 샘플링**해서 여러 트리 생성
- 결과는 다수결(분류) 또는 평균(회귀)
- 트리들이 서로 독립적이라 분산이 줄어든다

```python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bag = BaggingClassifier(
    estimator=DecisionTreeClassifier(),
    n_estimators=30,
    max_samples=0.8,   # 데이터의 80%만 샘플링
    random_state=42
)
bag.fit(X_train, y_train)
```

### Random Forest  (이번 실습 모델)
- Bagging + **변수(Feature)도 무작위 선택**
- 트리 간 상관관계가 더 낮아져서 Bagging보다 성능이 좋다
- `n_estimators`: 트리 수 (많을수록 안정적, 느려짐)

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,   # 트리 100개
    random_state=42
)
rf.fit(X_train, y_train)
print(rf.score(X_test, y_test))
```

### Boosting
- 이전 모델이 **틀린 샘플에 더 높은 가중치**를 주고 순차 학습
- 성능이 높지만 과적합 위험도 있어서 파라미터 튜닝 필요
- 대표 모델: AdaBoost, GradientBoosting, XGBoost, LightGBM

```python
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

gb  = GradientBoostingClassifier(n_estimators=100)
xgb = XGBClassifier(n_estimators=100)
lgb = LGBMClassifier(n_estimators=100)
```

---

## 4. 세 가지 한눈에 비교

| | Bagging | Random Forest | Boosting |
|---|---|---|---|
| 학습 순서 | 병렬 | 병렬 | 순차 |
| 샘플링 | 데이터 무작위 | 데이터 + 변수 무작위 | 오답에 가중치 |
| 속도 | 빠름 | 빠름 | 느림 |
| 과적합 위험 | 낮음 | 낮음 | 있음 (튜닝 필요) |
| 대표 모델 | BaggingClassifier | RandomForestClassifier | XGBoost, LightGBM |

---

## 5. 모델 성능 평가 지표

```python
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

# Confusion Matrix
ConfusionMatrixDisplay.from_estimator(rf, X_test, y_test)

# 정밀도(Precision), 재현율(Recall), F1
print(classification_report(y_test, rf.predict(X_test)))
```

- **Precision (정밀도)**: 양성이라 예측한 것 중 실제 양성 비율 → 판사 관점
- **Recall (재현율)**: 실제 양성 중 양성으로 예측한 비율 → 검사 관점
- **F1 Score**: Precision과 Recall의 조화 평균
