# main.py
from my_package import module_a, module_b

print("=== 패키지 사용 실습 시작 ===\n")

# 1. A 모듈의 변수 사용
print(module_a.a_variable)

# 2. A 모듈의 함수 사용
print(module_a.a_function())

# 3. B 모듈의 클래스 사용
# 클래스는 '객체'를 먼저 만들어야 합니다.
my_instance = module_b.BClass()

print(my_instance.info)     # 클래스 내부의 변수 출력
print(my_instance.display()) # 클래스 내부의 함수 출력

print("\n=== 모든 요소 사용 완료 ===")