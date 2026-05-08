"""
[Part 2 실습] Gradio UI — FastAPI를 호출하는 프론트엔드
- FastAPI 서버(8000)가 먼저 실행 중이어야 한다
- requests.post()로 API를 호출하고 결과를 화면에 표시
- 실행: python app_gradio.py
"""

import gradio as gr
import requests

FASTAPI_URL = "http://127.0.0.1:8000/predict/"

def predict_species(sl, sw, pl, pw):
    """
    슬라이더 값을 받아 FastAPI에 POST 요청을 보내고 결과를 반환한다.

    Args:
        sl: sepal_length (꽃받침 길이)
        sw: sepal_width  (꽃받침 너비)
        pl: petal_length (꽃잎 길이)
        pw: petal_width  (꽃잎 너비)
    """
    # Pydantic 모델의 필드명과 key가 정확히 일치해야 함
    payload = {
        "sepal_length": sl,
        "sepal_width":  sw,
        "petal_length": pl,
        "petal_width":  pw,
    }

    try:
        response = requests.post(FASTAPI_URL, json=payload, timeout=5)
        response.raise_for_status()   # 4xx, 5xx 에러를 예외로 변환

        result     = response.json()
        species    = result["species"].capitalize()
        confidence = result["confidence"] * 100

        return f"예측 품종: {species}\n확신도: {confidence:.2f}%"

    except requests.exceptions.ConnectionError:
        return "❌ FastAPI 서버에 연결할 수 없습니다.\nuvicorn api:app --reload 로 먼저 서버를 실행하세요."
    except requests.exceptions.HTTPError as e:
        return f"❌ HTTP {e.response.status_code} 에러: {e.response.text}"
    except Exception as e:
        return f"❌ 오류: {e}"


# ── Gradio Interface 정의 ──────────────────────────────────
# gr.Interface: 함수 하나를 UI로 감싸는 가장 간단한 방법
iface = gr.Interface(
    fn=predict_species,
    inputs=[
        gr.Slider(minimum=4.0, maximum=8.0, step=0.1, value=5.1,
                  label="꽃받침 길이 (Sepal Length, cm)"),
        gr.Slider(minimum=2.0, maximum=4.5, step=0.1, value=3.5,
                  label="꽃받침 너비 (Sepal Width, cm)"),
        gr.Slider(minimum=1.0, maximum=7.0, step=0.1, value=1.4,
                  label="꽃잎 길이 (Petal Length, cm)"),
        gr.Slider(minimum=0.1, maximum=2.5, step=0.1, value=0.2,
                  label="꽃잎 너비 (Petal Width, cm)"),
    ],
    outputs=gr.Textbox(label="예측 결과", lines=3),
    title="🌸 붓꽃(Iris) 품종 예측",
    description="슬라이더를 조절해 붓꽃 크기를 입력하면 품종을 예측합니다.",
)

if __name__ == "__main__":
    # share=True → 외부에서 접근 가능한 임시 URL 생성 (ngrok 사용)
    iface.launch(share=False)

# 실행: python app_gradio.py
