import streamlit as st
import pandas as pd
import joblib

# ---------------- 페이지 설정 ----------------
st.set_page_config(
    page_title="산불위험지수 예측 시스템",
    page_icon="🔥",
    layout="wide"
)

# ---------------- CSS 스타일 ----------------
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background: linear-gradient(135deg, #1a0a00, #2d1200);
    color: #f5f5f5;
}

/* 메인 카드 */
.main-card {
    background: rgba(255,255,255,0.07);
    padding: 2rem;
    border-radius: 24px;
    border: 1px solid rgba(255,150,50,0.2);
    margin-top: 2rem;
    margin-bottom: 2rem;
}

/* 제목 */
h1, h2, h3 {
    color: #ffffff !important;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

/* 일반 텍스트 */
p, label, .stMarkdown, caption {
    color: #f0e6d3 !important;
    font-size: 1rem !important;
}

/* 슬라이더 레이블 */
[data-testid="stSlider"] label {
    color: #ffd9b3 !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
}

/* 슬라이더 숫자 */
[data-testid="stSlider"] p {
    color: #ffb347 !important;
    font-size: 1.1rem !important;
    font-weight: bold !important;
}

/* metric 제목 */
[data-testid="metric-container"] label {
    color: #ffd9b3 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

/* metric 값 */
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.8rem !important;
    font-weight: bold !important;
}

/* metric 카드 */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1rem;
    border: 1px solid rgba(255,150,50,0.2);
}

/* 버튼 */
.stButton > button {
    width: 100%;
    height: 3.2rem;
    border-radius: 16px;
    border: none;
    background: linear-gradient(90deg, #f97316, #ef4444);
    color: white !important;
    font-size: 1.1rem !important;
    font-weight: bold !important;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(249,115,22,0.4);
}

/* info 박스 */
[data-testid="stAlert"] {
    background: rgba(255,200,100,0.1) !important;
    border: 1px solid rgba(255,150,50,0.3) !important;
    color: #ffe0b2 !important;
    font-size: 1.05rem !important;
}

/* caption */
[data-testid="stCaptionContainer"] p {
    color: #ffcc88 !important;
    font-size: 0.95rem !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- 모델 로드 ----------------
model = joblib.load("forest_fire_model.pkl")

# ---------------- 메인 ----------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.title("🔥 산불위험지수 예측 시스템")
st.caption("기상 데이터를 입력하면 AI가 산불위험지수(FWI)를 예측합니다.")

st.write("")

# ---------------- 슬라이더 입력 ----------------
st.subheader("📌 기상 데이터 입력")

col1, col2 = st.columns(2)

with col1:
    temperature = st.slider("🌡️ 기온 (°C)", min_value=0.0, max_value=50.0, value=30.0, step=0.5)
    wind = st.slider("💨 풍속 (km/h)", min_value=0.0, max_value=50.0, value=15.0, step=0.5)

with col2:
    humidity = st.slider("💧 상대습도 (%)", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
    rain = st.slider("🌧️ 강수량 (mm)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)

st.write("")

# ---------------- 현재 입력값 표시 ----------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("기온", f"{temperature}°C")
with m2:
    st.metric("상대습도", f"{humidity}%")
with m3:
    st.metric("풍속", f"{wind}km/h")
with m4:
    st.metric("강수량", f"{rain}mm")

st.write("")

# ---------------- 예측 버튼 ----------------
if st.button("🔍 산불위험지수 예측"):

    input_data = pd.DataFrame([[temperature, humidity, wind, rain]],
                               columns=['기온', '상대습도', '풍속', '강수량'])

    predicted_fwi = model.predict(input_data)[0]

    if predicted_fwi < 0:
        risk_level, description, color = "안전", "산불 발생 가능성이 거의 없습니다.", "green"
    elif predicted_fwi < 5.2:
        risk_level, description, color = "낮음", "산불 발생 가능성이 낮습니다.", "blue"
    elif predicted_fwi < 11.2:
        risk_level, description, color = "보통", "산불 발생 가능성이 있습니다. 주의하세요.", "yellow"
    elif predicted_fwi < 21.3:
        risk_level, description, color = "높음", "산불 발생 가능성이 높습니다! 각별히 주의하세요.", "orange"
    elif predicted_fwi < 38.0:
        risk_level, description, color = "매우 높음", "산불 발생 위험이 매우 높습니다! 즉각 대비하세요.", "red"
    else:
        risk_level, description, color = "극도로 위험", "산불 발생 위험이 극도로 높습니다! 즉시 대피하세요.", "red"

    st.write("")
    st.subheader("📊 예측 결과")

    r1, r2 = st.columns(2)
    with r1:
        st.metric(label="예측 산불위험지수 (FWI)", value=f"{predicted_fwi:.1f}")
    with r2:
        st.metric(label="위험도", value=risk_level)

    st.write("")
    st.markdown(f"### :{color}[{risk_level}]")
    st.info(f"💬 {description}")

    progress_value = min(predicted_fwi / 38.0, 1.0) if predicted_fwi > 0 else 0.0
    st.progress(progress_value)
    st.caption(f"FWI 기준 위험도: {progress_value * 100:.1f}%")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------- 푸터 ----------------
st.write("")
st.divider()
st.markdown("""
<p style='text-align: center; color: #a07850; font-size: 0.8rem;'>
    © 2026 산불위험지수 예측 시스템 | 
    Data: <a href='https://www.kaggle.com/datasets/nitinchoudhary012/algerian-forest-fires-dataset' target='_blank' style='color: #f97316;'>Kaggle - Algerian Forest Fires Dataset</a> | 
    FWI 기준: Canadian Forest Fire Weather Index System
</p>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)