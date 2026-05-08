"""
[Part 1 실습] Random Forest로 Iris 모델 학습 후 저장
- sklearn의 RandomForestClassifier 사용
- pickle로 모델 직렬화(Serialization)해서 .pkl 파일로 저장
- 이 파일을 먼저 실행해야 api 서버가 동작한다
"""

import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# ── 1. 데이터 로드 ──────────────────────────────────────────
iris = load_iris()
X, y = iris.data, iris.target

# feature: sepal_length, sepal_width, petal_length, petal_width
# target : 0=setosa, 1=versicolor, 2=virginica
print("데이터 shape:", X.shape)  # (150, 4)

# ── 2. 훈련 / 테스트 분리 ──────────────────────────────────
# test_size=0.25 → 75% 훈련, 25% 테스트
# stratify=y     → 각 클래스 비율 유지
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

# ── 3. 모델 학습 ───────────────────────────────────────────
# n_estimators=100 : 트리 100개를 만들어서 다수결
# random_state     : 재현성을 위해 고정
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ── 4. 성능 확인 ───────────────────────────────────────────
y_pred = model.predict(X_test)
print("\n--- 모델 성능 ---")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# feature 중요도 출력 (Random Forest의 장점: 해석 가능)
print("--- Feature 중요도 ---")
for name, importance in zip(iris.feature_names, model.feature_importances_):
    print(f"  {name:20s}: {importance:.4f}")

# ── 5. 모델 저장 (Serialization) ──────────────────────────
# pickle: 파이썬 객체를 바이트(binary)로 변환해서 파일 저장
# wb = write binary (텍스트 모드로 저장하면 모델이 깨짐)
MODEL_PATH = "iris_model.pkl"
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print(f"\n✅ 모델 저장 완료: {os.path.abspath(MODEL_PATH)}")

# ── [참고] 불러오기 테스트 ──────────────────────────────────
with open(MODEL_PATH, "rb") as f:        # rb = read binary
    loaded_model = pickle.load(f)

sample = [[5.1, 3.5, 1.4, 0.2]]         # setosa 샘플
pred = loaded_model.predict(sample)[0]
print(f"로드 후 예측 테스트: {iris.target_names[pred]}")  # → setosa
