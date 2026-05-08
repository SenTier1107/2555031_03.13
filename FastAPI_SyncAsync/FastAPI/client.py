"""
=============================================================
  FastAPI 클라이언트 실습 — client.py
=============================================================

이 파일은 server.py 서버에 실제로 요청을 보내는 클라이언트입니다.

실행 순서:
    1. 터미널 1: uvicorn server:app --reload  (서버 먼저 실행!)
    2. 터미널 2: python client.py              (클라이언트 실행)

사용 라이브러리:
    - requests : 동기 방식 HTTP 클라이언트 (가장 일반적)
    - httpx    : requests와 유사하지만 비동기도 지원 (최신 트렌드)

-------------------------------------------------------------
[requests vs httpx 비교]

  requests  → 동기 전용, 오래된 라이브러리, 사용법 단순
  httpx     → 동기 + 비동기 모두 지원, FastAPI 공식 추천

=============================================================
"""

import requests
import httpx
import json

# 서버 주소를 상수로 관리합니다.
# 나중에 서버 주소가 바뀌어도 여기 한 곳만 수정하면 됩니다.
BASE_URL = "http://localhost:8000"


def print_response(label: str, response):
    """응답 결과를 보기 좋게 출력하는 헬퍼 함수"""
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    print(f"  상태 코드: {response.status_code}")
    print(f"  응답 데이터: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")


# ══════════════════════════════════════════════════════════
#  1. GET 요청 — 데이터 조회
# ══════════════════════════════════════════════════════════

print("\n" + "★"*50)
print("  1. GET 요청 실습")
print("★"*50)

# [GET] 루트 경로 — httpx 사용
# httpx.get()은 requests.get()과 사용법이 동일합니다.
r = httpx.get(f"{BASE_URL}/")
print_response("GET / — 서버 상태 확인 (httpx 사용)", r)

# [GET] 전체 상품 목록 조회
r = requests.get(f"{BASE_URL}/items/")
print_response("GET /items/ — 전체 상품 조회", r)

# [GET] 특정 상품 조회 (Path Parameter)
# URL 경로에 ID를 포함해서 보냅니다: /items/1
r = requests.get(f"{BASE_URL}/items/1")
print_response("GET /items/1 — ID=1 상품 조회", r)

# [GET] 존재하지 않는 상품 조회 → 404 에러
r = requests.get(f"{BASE_URL}/items/999")
print_response("GET /items/999 — 없는 상품 조회 (404 에러 확인)", r)


# ══════════════════════════════════════════════════════════
#  2. POST 요청 — 새 데이터 생성
# ══════════════════════════════════════════════════════════

print("\n" + "★"*50)
print("  2. POST 요청 실습")
print("★"*50)

# [POST] 새 상품 생성
# json= 파라미터로 딕셔너리를 넘기면 자동으로 JSON으로 변환됩니다.
# Content-Type: application/json 헤더도 자동으로 설정됩니다.
new_item = {
    "name": "Monitor",
    "price": 350.0,
    "is_offer": False
}
r = requests.post(f"{BASE_URL}/items/4", json=new_item)
print_response("POST /items/4 — 새 상품(Monitor) 생성", r)

# 생성 확인: 전체 목록 다시 조회
r = requests.get(f"{BASE_URL}/items/")
print_response("GET /items/ — 생성 후 전체 조회 (ID=4 추가됨 확인)", r)


# ══════════════════════════════════════════════════════════
#  3. PUT 요청 — 데이터 수정
# ══════════════════════════════════════════════════════════

print("\n" + "★"*50)
print("  3. PUT 요청 실습")
print("★"*50)

# [PUT] ID=2 상품 수정 (Mouse → Wireless Mouse, 가격 변경)
# PUT은 리소스 전체를 새 데이터로 교체합니다.
updated_item = {
    "name": "Wireless Mouse",
    "price": 45.0,
    "is_offer": True
}
r = requests.put(f"{BASE_URL}/items/2", json=updated_item)
print_response("PUT /items/2 — ID=2 상품 수정 (Mouse → Wireless Mouse)", r)

# 수정 확인
r = requests.get(f"{BASE_URL}/items/2")
print_response("GET /items/2 — 수정 후 확인", r)


# ══════════════════════════════════════════════════════════
#  4. DELETE 요청 — 데이터 삭제
# ══════════════════════════════════════════════════════════

print("\n" + "★"*50)
print("  4. DELETE 요청 실습")
print("★"*50)

# [DELETE] ID=3 상품 삭제
r = requests.delete(f"{BASE_URL}/items/3")
print_response("DELETE /items/3 — ID=3 상품(Keyboard) 삭제", r)

# 삭제 확인: 전체 목록 다시 조회
r = requests.get(f"{BASE_URL}/items/")
print_response("GET /items/ — 삭제 후 전체 조회 (ID=3 사라짐 확인)", r)

# [DELETE] 이미 삭제된 상품 다시 삭제 시도 → 404 에러
r = requests.delete(f"{BASE_URL}/items/3")
print_response("DELETE /items/3 — 이미 삭제된 상품 삭제 시도 (404 에러 확인)", r)


# ══════════════════════════════════════════════════════════
#  5. CSV 다운로드 확인
# ══════════════════════════════════════════════════════════

print("\n" + "★"*50)
print("  5. CSV 다운로드")
print("★"*50)

r = requests.get(f"{BASE_URL}/download-items-csv")
print(f"\n{'='*50}")
print("  GET /download-items-csv — CSV 파일 내용 확인")
print(f"{'='*50}")
print(f"  상태 코드: {r.status_code}")
print(f"  Content-Type: {r.headers.get('content-type')}")
print(f"  CSV 내용:\n")
print(r.text)

print("\n✅ 모든 CRUD 요청 완료!")
print("브라우저에서 http://localhost:8000/docs 를 열면 Swagger UI로 직접 테스트할 수 있습니다.")
