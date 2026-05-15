# main_wine_gradio_mount.py
# 실행 순서:
#   1. python train_wine_model.py
#   2. python main_wine_gradio_mount.py
# 접속:
#   - Gradio UI : http://127.0.0.1:8000/gradio
#   - API Docs  : http://127.0.0.1:8000/docs

import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sklearn.datasets import load_wine
import gradio as gr
import uvicorn

# ── 1. 모델 & 데이터 로드 ─────────────────────────────
MODEL_FILENAME = "wine_model.pkl"
try:
    with open(MODEL_FILENAME, "rb") as f:
        model = pickle.load(f)
    print("모델 로드 완료")
except FileNotFoundError:
    print(f"'{MODEL_FILENAME}' 파일이 없습니다. train_wine_model.py를 먼저 실행하세요.")
    model = None

wine_data     = load_wine()
wine_names    = wine_data.target_names
feature_names = wine_data.feature_names

WINE_INFO = {
    "class_0": {"name": "Barolo (바롤로)",        "desc": "풀바디 고급 레드와인. 알코올과 프롤린 함량이 높고 색이 진함."},
    "class_1": {"name": "Grignolino (그리뇰리노)", "desc": "미디엄바디 레드와인. 페놀 함량이 중간이며 균형 잡힌 특성."},
    "class_2": {"name": "Barbera (바르베라)",       "desc": "산도 높은 레드와인. 말산과 색 강도가 높은 편."},
}

# ── 2. FastAPI ────────────────────────────────────────
app = FastAPI(title="Wine Classification API")

@app.get("/")
def root():
    return RedirectResponse(url="/gradio")

class WineTop6(BaseModel):
    flavanoids:      float
    color_intensity: float
    proline:         float
    alcohol:         float
    od280_od315:     float
    hue:             float

def get_prediction_top6(flavanoids, color_intensity, proline, alcohol, od280_od315, hue):
    if model is None:
        return {"error": "모델 로드 실패"}
    sample = wine_data.data.mean(axis=0).copy()
    sample[0]  = alcohol
    sample[6]  = flavanoids
    sample[9]  = color_intensity
    sample[10] = hue
    sample[11] = od280_od315
    sample[12] = proline
    prediction = model.predict([sample])[0]
    proba      = model.predict_proba([sample])[0]
    return {
        "class":         wine_names[prediction],
        "confidence":    float(np.max(proba)),
        "probabilities": {wine_names[i]: round(float(p), 4) for i, p in enumerate(proba)},
    }

@app.post("/api/predict")
def predict_api(features: WineTop6):
    return get_prediction_top6(
        features.flavanoids, features.color_intensity, features.proline,
        features.alcohol, features.od280_od315, features.hue
    )

# ── 3. 탭1: 전체 데이터 조회 ─────────────────────────
def load_dataset(class_filter):
    df = pd.DataFrame(wine_data.data, columns=feature_names)
    df.insert(0, "class", [wine_names[t] for t in wine_data.target])
    if class_filter != "전체":
        df = df[df["class"] == class_filter]
    df = df.round(2)
    summary = f"총 {len(df)}개 샘플  |  피처 {len(feature_names)}개"
    return df, summary

# ── 4. 탭2: 피처 중요도 차트 (차트 내부만 영문) ──────
def show_importance():
    if model is None:
        return None, "모델 없음"

    df = pd.DataFrame({'feature': feature_names, 'importance': model.feature_importances_})
    df = df.sort_values('importance', ascending=False).reset_index(drop=True)
    df['cumsum'] = df['importance'].cumsum() * 100
    df_plot = df.iloc[::-1].reset_index(drop=True)
    top6 = set(df.head(6)['feature'])

    fig, ax1 = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor('#1a1a2e')
    ax1.set_facecolor('#16213e')

    bar_colors = ['#e05a2b' if f in top6 else '#3a3a5c' for f in df_plot['feature']]
    bars = ax1.barh(df_plot['feature'], df_plot['importance'], color=bar_colors, height=0.65, zorder=3)

    for bar, val, feat in zip(bars, df_plot['importance'], df_plot['feature']):
        color = 'white' if feat in top6 else '#9090b0'
        ax1.text(val + 0.001, bar.get_y() + bar.get_height()/2,
                 f'{val*100:.1f}%', va='center', fontsize=9,
                 color=color, fontweight='bold' if feat in top6 else 'normal')

    ax2 = ax1.twinx()
    ax2.set_facecolor('#16213e')
    ax2.plot(df_plot['cumsum'].values, list(range(len(df_plot))),
             color='#00d4ff', linewidth=2, marker='o', markersize=5, zorder=4, alpha=0.9)

    hue_y  = df_plot[df_plot['feature'] == 'hue'].index[0]
    line_y = hue_y - 0.5
    ax2.axhline(y=line_y, color='#ffd700', linewidth=1.3, linestyle='--', alpha=0.9, zorder=5)

    x_max = df['importance'].max() * 1.28
    ax1.text(x_max * 0.98, line_y + 0.05,
             'Up to hue: 80.7% explained',
             fontsize=8.5, color='#ffd700', va='bottom', ha='right', zorder=6)

    ax2.set_ylim(-0.5, len(df_plot) - 0.5)
    ax2.set_xlim(0, 115)
    ax2.set_ylabel('Cumulative Importance (%)', fontsize=10, color='#00d4ff', labelpad=8)
    ax2.tick_params(axis='y', colors='#00d4ff', labelsize=9)
    ax2.spines[['top','right','bottom','left']].set_visible(False)

    ax1.set_xlim(0, x_max)
    ax1.set_xlabel('Individual Importance', fontsize=10, color='#9090b0', labelpad=8)
    ax1.tick_params(axis='y', labelsize=10, colors='white')
    ax1.tick_params(axis='x', colors='#9090b0', labelsize=9)
    ax1.spines[['top','right','bottom','left']].set_visible(False)
    ax1.xaxis.grid(True, color='#2a2a4a', linewidth=0.7, zorder=0)
    ax1.set_axisbelow(True)
    ax1.set_title('Wine Classification — Feature Importance Analysis',
                  fontsize=14, fontweight='bold', color='white', pad=16, loc='left')

    legend_patches = [
        mpatches.Patch(color='#e05a2b', label='Top 6 features (used in prediction)'),
        mpatches.Patch(color='#3a3a5c', label='Other features'),
        plt.Line2D([0],[0], color='#00d4ff', linewidth=2, marker='o', markersize=5, label='Cumulative importance'),
        plt.Line2D([0],[0], color='#ffd700', linewidth=1.5, linestyle='--', label='Top 6 threshold (80.7%)'),
    ]
    ax1.legend(handles=legend_patches, loc='lower right', fontsize=9,
               facecolor='#1a1a2e', edgecolor='#3a3a5c', labelcolor='white')

    plt.subplots_adjust(left=0.2, right=0.88, top=0.92, bottom=0.1)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches=None, facecolor='#1a1a2e')
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)

    cumsum = 0
    rank_text = f"{'순위':<4} {'피처':<35} {'중요도':>7}  {'누적'}\n"
    rank_text += "-" * 58 + "\n"
    for i, row in df.iterrows():
        cumsum += row['importance']
        marker = " << 예측 사용" if i < 6 else ""
        rank_text += f"{i+1:<4} {row['feature']:<35} {row['importance']:.4f}   {cumsum*100:.1f}%{marker}\n"

    return img, rank_text

# ── 5. 탭3: 예측 함수 ─────────────────────────────────
def predict_ui(flavanoids, color_intensity, proline, alcohol, od280_od315, hue):
    result = get_prediction_top6(flavanoids, color_intensity, proline, alcohol, od280_od315, hue)
    if "error" in result:
        return f"오류: {result['error']}", ""

    cls        = result["class"]
    confidence = result["confidence"] * 100
    info       = WINE_INFO[cls]
    probs      = result["probabilities"]

    prob_bars = ""
    for k, v in probs.items():
        bar = "█" * int(v * 20) + "░" * (20 - int(v * 20))
        prob_bars += f"{WINE_INFO[k]['name']}\n  [{bar}] {v*100:.1f}%\n\n"

    result_text = (
        f"예측 결과: {info['name']}\n"
        f"확신도: {confidence:.1f}%\n"
        f"특징: {info['desc']}"
    )
    return result_text, prob_bars

# ── 6. Gradio 인터페이스 ──────────────────────────────
with gr.Blocks(title="Wine 품종 분류", theme=gr.themes.Soft()) as demo:

    gr.Markdown("# Wine 품종 분류 서비스\n이탈리아 와인 3종(Barolo / Grignolino / Barbera)을 분석합니다.")

    with gr.Tabs():

        # ── 탭 1: 데이터 조회 ──
        with gr.Tab("데이터 조회"):
            gr.Markdown("### 전체 데이터셋 (178개 샘플, 13개 피처)")
            with gr.Row():
                class_filter = gr.Dropdown(
                    choices=["전체", "class_0", "class_1", "class_2"],
                    value="전체", label="클래스 필터", scale=1
                )
                summary_box = gr.Textbox(label="요약", scale=3, interactive=False)
            load_btn   = gr.Button("데이터 불러오기", variant="primary")
            data_table = gr.Dataframe(label="와인 데이터", interactive=False, wrap=False)

            load_btn.click(fn=load_dataset, inputs=class_filter, outputs=[data_table, summary_box])
            demo.load(fn=load_dataset, inputs=class_filter, outputs=[data_table, summary_box])

        # ── 탭 2: 피처 중요도 ──
        with gr.Tab("피처 중요도"):
            gr.Markdown("### 각 변수가 품종 분류에 기여하는 정도 (Random Forest)")

            with gr.Row():
                gr.Textbox(value="13개",         label="전체 변수 수",         interactive=False)
                gr.Textbox(value="6개  (1~6위)", label="예측에 사용하는 변수", interactive=False)
                gr.Textbox(value="80.7%",         label="상위 6개 누적 설명력", interactive=False)

            gr.Markdown(
                "> 변수가 많을수록 UI가 복잡해지지만 정확도 향상은 점점 줄어듭니다.  \n"
                "> 상위 6개만으로 전체의 **80.7%** 를 설명할 수 있어,  \n"
                "> 나머지 7개(19.3%)는 예측에서 제외하고 평균값으로 대체했습니다."
            )

            importance_btn = gr.Button("중요도 차트 보기", variant="primary")
            with gr.Row():
                importance_img  = gr.Image(label="중요도 차트", type="pil")
                importance_text = gr.Textbox(label="순위 목록 (누적 중요도)", lines=15, interactive=False)
            importance_btn.click(fn=show_importance, inputs=[], outputs=[importance_img, importance_text])

        # ── 탭 3: 품종 예측 ──
        with gr.Tab("품종 예측"):
            gr.Markdown("### 상위 기여도 6개 변수로 품종 예측 (누적 설명력 80.7%)")
            gr.Markdown("> 나머지 7개 변수는 **평균값**으로 자동 처리됩니다.")

            with gr.Row():
                with gr.Column():
                    gr.Markdown("**페놀 & 색상**")
                    flavanoids      = gr.Slider(0.3,  5.1,  step=0.01, value=2.03, label="Flavanoids (플라보노이드) — 1위 20.2%")
                    color_intensity = gr.Slider(1.2,  13.1, step=0.01, value=5.06, label="Color Intensity (색 강도) — 2위 17.1%")
                    hue             = gr.Slider(0.4,  1.8,  step=0.01, value=0.96, label="Hue (색조) — 6위 7.1%")

                with gr.Column():
                    gr.Markdown("**기본 성분**")
                    proline     = gr.Slider(278,  1680, step=1.0,  value=747,  label="Proline (프롤린) — 3위 13.9%")
                    alcohol     = gr.Slider(11.0, 15.0, step=0.01, value=13.0, label="Alcohol (알코올) — 4위 11.2%")
                    od280_od315 = gr.Slider(1.2,  4.1,  step=0.01, value=2.61, label="OD280/OD315 (희석 와인) — 5위 11.2%")

            pred_btn = gr.Button("품종 예측하기", variant="primary", size="lg")

            with gr.Row():
                pred_result = gr.Textbox(label="예측 결과", lines=5)
                pred_probs  = gr.Textbox(label="클래스별 확률", lines=7)

            

            pred_btn.click(
                fn=predict_ui,
                inputs=[flavanoids, color_intensity, proline, alcohol, od280_od315, hue],
                outputs=[pred_result, pred_probs]
            )

# ── 7. 마운트 & 실행 ──────────────────────────────────
app = gr.mount_gradio_app(app, demo, path="/gradio")

if __name__ == "__main__":
    print("\n" + "="*55)
    print("서버 시작!")
    print("="*55)
    print("Gradio UI   : /gradio")
    print("API Docs    : /docs")
    print("API Endpoint: /api/predict")
    print("="*55 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=7860)