# my_module.py

# 1. 변수 (데이터 저장)
module_name = "기초 모듈 1호"
version = 1.0

# 2. 함수 (특정 동작 수행)
def print_hello():
    return "안녕하세요! 모듈 내 함수가 실행되었습니다."

# 3. 클래스 (데이터와 기능을 묶은 틀)
class SimpleCalculator:
    def __init__(self):
        self.count = 0  # 계산 횟수를 저장할 변수

    def add(self, a, b):
        self.count += 1
        return a + b