import pickle
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

# 1. 데이터 로드
print("Wine 모델 학습을 시작합니다...")
wine = load_wine()
X, y = wine.data, wine.target

# 2. 훈련/테스트 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. 정확도 출력
score = model.score(X_test, y_test)
print(f"테스트 정확도: {score:.4f} ({score*100:.2f}%)")

# 5. 모델 저장
MODEL_FILENAME = "wine_model.pkl"
with open(MODEL_FILENAME, "wb") as f:
    pickle.dump(model, f)

print(f"Wine 모델이 '{MODEL_FILENAME}'으로 저장되었습니다.")
print(f"저장 경로: {os.path.abspath(MODEL_FILENAME)}")