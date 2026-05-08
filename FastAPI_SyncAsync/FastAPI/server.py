"""
=============================================================
  FastAPI 실습 서버 — main_server.py
=============================================================

실행 방법 (터미널에서):
    uvicorn main_server:app --reload

접속 주소:
    API 서버  → http://localhost:8000
    Swagger UI → http://localhost:8000/docs   ← 여기서 직접 테스트 가능!
    ReDoc      → http://localhost:8000/redoc

-------------------------------------------------------------
[FastAPI 기본 구조 이해]

  클라이언트 (브라우저 / main_CRUD.py)
        ↓  HTTP 요청 (GET / POST / PUT / DELETE)
  FastAPI 서버 (main_server.py)
        ↓  데이터 처리
  인메모리 DB (items_db 딕셔너리)

-------------------------------------------------------------
[HTTP 메서드 정리]

  GET    → 데이터 조회  (Read)
  POST   → 데이터 생성  (Create)
  PUT    → 데이터 수정  (Update)
  DELETE → 데이터 삭제  (Delete)

=============================================================
"""

# ── 라이브러리 임포트 ──────────────────────────────────────
from typing import Union
from fastapi import FastAPI, HTTPException  # FastAPI 핵심
from fastapi.responses import StreamingResponse  # 파일 다운로드용
from pydantic import BaseModel  # 데이터 유효성 검사
import csv
import io


# ── FastAPI 앱 인스턴스 생성 ────────────────────────────────
# FastAPI()를 호출하여 앱 객체를 만듭니다.
# 이 app 객체에 라우터(엔드포인트)를 등록합니다.
app = FastAPI(
    title="상품 관리 API",
    description="FastAPI로 만든 간단한 상품 CRUD API 실습",
    version="1.0.0"
)


# ── 데이터 모델 정의 (Pydantic) ─────────────────────────────
# BaseModel을 상속받아 데이터 구조를 정의합니다.
# FastAPI는 이 모델을 기반으로 요청 데이터를 자동으로 검증합니다.
#
# 예) price에 "abc" 문자열을 보내면 → 자동으로 422 에러 반환
class Item(BaseModel):
    name: str                       # 필수 항목
    price: float                    # 필수 항목 (숫자만 허용)
    is_offer: Union[bool, None] = None  # 선택 항목 (기본값: None)


# ── 인메모리 데이터베이스 ────────────────────────────────────
# 실제 서비스에서는 PostgreSQL, MySQL 등 DB를 사용합니다.
# 지금은 학습용으로 딕셔너리를 DB처럼 사용합니다.
# 서버를 재시작하면 데이터가 초기화됩니다.
items_db = {
    1: {"name": "Laptop",   "price": 1200.0, "is_offer": True},
    2: {"name": "Mouse",    "price": 25.0,   "is_offer": False},
    3: {"name": "Keyboard", "price": 75.0,   "is_offer": True},
}


# ══════════════════════════════════════════════════════════
#  엔드포인트 정의
#  @app.메서드("경로") 데코레이터로 URL과 함수를 연결합니다.
# ══════════════════════════════════════════════════════════

# ── [GET] 루트 경로 ─────────────────────────────────────────
# GET http://localhost:8000/
@app.get("/")
def read_root():
    """서버 상태 확인용 루트 엔드포인트"""
    return {"message": "안녕하세요! FastAPI 상품 관리 서버입니다 🚀"}


# ── [GET] 전체 상품 조회 ─────────────────────────────────────
# GET http://localhost:8000/items/
@app.get("/items/")
def get_all_items():
    """모든 상품 목록을 반환합니다."""
    return items_db


# ── [GET] 특정 상품 조회 ─────────────────────────────────────
# GET http://localhost:8000/items/1
# {item_id}는 Path Parameter — URL의 일부로 전달되는 값
@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    특정 ID의 상품을 반환합니다.

    - item_id: URL 경로에서 추출한 상품 ID
    - 없는 ID를 요청하면 404 에러를 반환합니다.
    """
    if item_id not in items_db:
        # HTTPException으로 HTTP 에러 코드와 메시지를 함께 반환
        raise HTTPException(status_code=404, detail=f"ID {item_id} 상품을 찾을 수 없습니다.")
    return items_db[item_id]


# ── [POST] 새 상품 생성 ──────────────────────────────────────
# POST http://localhost:8000/items/4
# Request Body에 JSON 데이터를 포함해서 보냅니다.
# {"name": "Monitor", "price": 300.0, "is_offer": false}
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    """
    새로운 상품을 생성합니다.

    - item_id: URL에서 받는 새 상품의 ID
    - item: Request Body에서 받는 상품 데이터 (Pydantic 자동 검증)
    """
    if item_id in items_db:
        raise HTTPException(status_code=409, detail=f"ID {item_id}는 이미 존재합니다.")
    items_db[item_id] = item.model_dump()
    return {"message": "상품이 성공적으로 생성되었습니다!", "item": item}


# ── [PUT] 상품 수정 ──────────────────────────────────────────
# PUT http://localhost:8000/items/1
# Request Body: {"name": "Gaming Laptop", "price": 1500.0, "is_offer": true}
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    기존 상품 정보를 전체 수정합니다. (전체 덮어쓰기)

    - PUT은 리소스 전체를 새 데이터로 교체합니다.
    - 일부만 수정하려면 PATCH를 사용합니다.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"ID {item_id} 상품을 찾을 수 없습니다.")
    items_db[item_id] = item.model_dump()
    return {"message": "상품이 성공적으로 수정되었습니다!", "item": item}


# ── [DELETE] 상품 삭제 ───────────────────────────────────────
# DELETE http://localhost:8000/items/1
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """특정 ID의 상품을 삭제합니다."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"ID {item_id} 상품을 찾을 수 없습니다.")

    deleted_item = items_db.pop(item_id)  # 딕셔너리에서 꺼내면서 삭제

    return {
        "message": f"ID {item_id} 상품이 삭제되었습니다.",
        "deleted_item": deleted_item
    }


# ── [GET] CSV 파일 다운로드 ──────────────────────────────────
# GET http://localhost:8000/download-items-csv
# 브라우저에서 접속하면 CSV 파일이 자동으로 다운로드됩니다.
@app.get("/download-items-csv")
def download_items_csv():
    """
    현재 items_db의 데이터를 CSV 파일로 다운로드합니다.

    StreamingResponse: 파일을 메모리에서 스트리밍으로 전송하는 방식
    """
    # 메모리에 CSV 파일 생성 (실제 파일 저장 없이 메모리에서 처리)
    output = io.StringIO()
    writer = csv.writer(output)

    # 헤더 행 작성
    writer.writerow(["item_id", "name", "price", "is_offer"])

    # 데이터 행 작성
    for item_id, item in items_db.items():
        writer.writerow([item_id, item["name"], item["price"], item["is_offer"]])

    output.seek(0)  # 파일 포인터를 처음으로 되돌리기

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=items.csv"}
    )


# ── 직접 실행할 때 (uvicorn 없이) ───────────────────────────
# python main_server.py 로 실행하는 경우
if __name__ == "__main__":
    import uvicorn
    # host="0.0.0.0" → 같은 네트워크의 다른 기기에서도 접속 가능
    # reload=True → 코드 수정 시 서버 자동 재시작
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
