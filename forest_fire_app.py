
import streamlit as st
import pandas as pd
import joblib

# ==================================================
# 페이지 설정
# ==================================================
st.set_page_config(
    page_title="산불위험지수 예측 시스템",
    page_icon="🔥",
    layout="wide"
)

# ==================================================
# 세션 상태
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ==================================================
# CSS (모든 글씨 흰색 버전)
# ==================================================
st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#1a0a00,#2d1200);
    color:white !important;
}

html, body,
h1,h2,h3,h4,h5,h6,
p, span, label, div, li,
strong, b {
    color:white !important;
}

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#160700,#0f0400);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

.stSelectbox *{
    color:white !important;
}

.stSelectbox div[data-baseweb="select"] > div{
    background: rgba(255,255,255,0.08) !important;
    border:2px solid #ff5a36 !important;
    border-radius:18px !important;
}

.stButton > button{
    width:100%;
    height:60px;
    border:none;
    border-radius:18px;
    background:linear-gradient(90deg,#f97316,#ef4444);
    color:white !important;
    font-size:18px;
    font-weight:bold;
    transition:0.3s;
}

.stButton > button:hover{
    transform:translateY(-2px);
}

.main-card{
    background:rgba(255,255,255,0.07);
    border-radius:24px;
    padding:30px;
    border:1px solid rgba(255,150,50,0.2);
}

[data-testid="stSlider"] label{
    color:white !important;
    font-size:16px !important;
    font-weight:600 !important;
}

[data-testid="stSlider"] p{
    color:#ffb347 !important;
    font-weight:bold !important;
}

[data-testid="metric-container"]{
    background:rgba(255,255,255,0.08);
    border-radius:20px;
    padding:15px;
    border:1px solid rgba(255,255,255,0.1);
}

[data-testid="metric-container"] *{
    color:white !important;
}

[data-testid="stMetricValue"]{
    color:white !important;
}

[data-testid="stAlert"]{
    background:rgba(255,255,255,0.08) !important;
}

[data-testid="stAlert"] *{
    color:white !important;
}

.stMarkdown,
.stMarkdown *{
    color:white !important;
}

.footer{
    color:white !important;
    text-align:center;
}

hr{
    border-color:rgba(255,255,255,0.15) !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 모델 로드
# ==================================================
model = joblib.load("forest_fire_model.pkl")

# ==================================================
# 사이드바
# ==================================================
with st.sidebar:

    st.markdown("## 🌍 Language")

    language = st.selectbox(
        "",
        ["한국어", "English"]
    )

    st.divider()

    if language == "한국어":
        st.markdown("## 📌 메뉴")
    else:
        st.markdown("## 📌 Menu")

    if language == "한국어":

        if st.button("🏠 홈"):
            st.session_state.page = "home"

        if st.button("🔥 산불 예측"):
            st.session_state.page = "predict"

        if st.button("ℹ️ 시스템 소개"):
            st.session_state.page = "about"

    else:

        if st.button("🏠 Home"):
            st.session_state.page = "home"

        if st.button("🔥 Prediction"):
            st.session_state.page = "predict"

        if st.button("ℹ️ About"):
            st.session_state.page = "about"

# ==================================================
# 홈 화면
# ==================================================
if st.session_state.page == "home":

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":

        st.title("🔥 산불위험지수 예측 시스템")

        st.markdown("""
        ### 환영합니다

        이 시스템은 AI를 이용하여

        - 🌡️ 기온
        - 💧 상대습도
        - 💨 풍속
        - 🌧️ 강수량

        데이터를 분석하여 산불위험지수(FWI)를 예측합니다.

        왼쪽 메뉴에서 시작하세요.
        """)

    else:

        st.title("🔥 Forest Fire Risk Prediction System")

        st.markdown("""
        ### Welcome

        This system predicts the Fire Weather Index (FWI)
        using:

        - Temperature
        - Humidity
        - Wind Speed
        - Rainfall

        Start from the left menu.
        """)

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "predict":

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    st.title("🔥 산불위험지수 예측" if language=="한국어" else "🔥 Fire Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        temperature = st.slider("🌡️ 기온 (°C)" if language=="한국어" else "🌡️ Temperature (°C)",0.0,50.0,30.0,0.5)
        wind = st.slider("💨 풍속 (km/h)" if language=="한국어" else "💨 Wind Speed (km/h)",0.0,50.0,15.0,0.5)

    with col2:
        humidity = st.slider("💧 상대습도 (%)" if language=="한국어" else "💧 Humidity (%)",0.0,100.0,40.0,1.0)
        rain = st.slider("🌧️ 강수량 (mm)" if language=="한국어" else "🌧️ Rainfall (mm)",0.0,10.0,0.0,0.1)

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("기온" if language=="한국어" else "Temp", f"{temperature}°C")
    m2.metric("습도" if language=="한국어" else "Humidity", f"{humidity}%")
    m3.metric("풍속" if language=="한국어" else "Wind", f"{wind} km/h")
    m4.metric("강수량" if language=="한국어" else "Rain", f"{rain} mm")

    if st.button("🔍 산불위험지수 예측" if language=="한국어" else "🔍 Predict"):

        input_df = pd.DataFrame(
            [[temperature, humidity, wind, rain]],
            columns=["기온","상대습도","풍속","강수량"]
        )

        predicted_fwi = model.predict(input_df)[0]

        if predicted_fwi < 5.2:
            risk = "낮음" if language=="한국어" else "Low"
        elif predicted_fwi < 11.2:
            risk = "보통" if language=="한국어" else "Moderate"
        elif predicted_fwi < 21.3:
            risk = "높음" if language=="한국어" else "High"
        elif predicted_fwi < 38:
            risk = "매우 높음" if language=="한국어" else "Very High"
        else:
            risk = "극도로 위험" if language=="한국어" else "Extreme"

        st.subheader("📊 예측 결과" if language=="한국어" else "📊 Prediction Result")

        c1,c2 = st.columns(2)
        c1.metric("예측 FWI" if language=="한국어" else "Predicted FWI", f"{predicted_fwi:.2f}")
        c2.metric("위험도" if language=="한국어" else "Risk Level", risk)

        st.progress(min(predicted_fwi/38.0,1.0))

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "about":

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":
        st.title("ℹ️ 시스템 소개")
        st.markdown("""
        ### 산불위험지수(FWI) 예측 시스템

        기상 데이터를 기반으로 산불 발생 위험도를 예측하는 AI 시스템입니다.
        """)
    else:
        st.title("ℹ️ About System")
        st.markdown("""
        ### Forest Fire Prediction System

        AI system that predicts forest fire risk.
        """)

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.markdown(
    """
    <div class="footer">
        © 2026 Forest Fire Prediction System
    </div>
    """,
    unsafe_allow_html=True
)
