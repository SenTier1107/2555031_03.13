# main.py
import my_module1

# [1] 변수 사용하기
print(f"사용 중인 모듈: {my_module1.module_name}")
print(f"버전 정보: {my_module1.version}")

# [2] 함수 호출하기
result_msg = my_module1.print_hello()
print(result_msg)

# [3] 클래스 사용하기
# 클래스는 '설계도'이므로, 먼저 객체(도구)를 만들어야 합니다.
calc = my_module1.SimpleCalculator()

sum_result = calc.add(10, 5)
print(f"더하기 결과: {sum_result}")
print(f"계산기 사용 횟수: {calc.count}")