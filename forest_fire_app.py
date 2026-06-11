```python
import streamlit as st
import pandas as pd
import joblib

# ==========================
# 페이지 설정
# ==========================
st.set_page_config(
    page_title="Forest Fire Prediction System",
    page_icon="🔥",
    layout="wide"
)

# ==========================
# 세션 상태
# ==========================
if "lang" not in st.session_state:
    st.session_state.lang = "한국어"

if "page" not in st.session_state:
    st.session_state.page = "홈"

# ==========================
# CSS
# ==========================
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background: linear-gradient(135deg, #1a0a00, #2d1200);
    color: #f5f5f5;
}

/* 카드 */
.main-card {
    background: rgba(255,255,255,0.07);
    padding: 2rem;
    border-radius: 24px;
    border: 1px solid rgba(255,150,50,0.2);
    margin-top: 1rem;
}

/* 제목 */
h1,h2,h3{
    color:white !important;
}

/* 버튼 */
.stButton > button{
    width:100%;
    border-radius:15px;
    background:linear-gradient(90deg,#f97316,#ef4444);
    color:white;
    border:none;
    font-weight:bold;
    height:3rem;
}

/* 메트릭 */
[data-testid="metric-container"]{
    background:rgba(255,255,255,0.08);
    border-radius:18px;
    padding:15px;
}

/* 사이드바 */
section[data-testid="stSidebar"]{
    background:#140800;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# 모델 로드
# ==========================
model = joblib.load("forest_fire_model.pkl")

# ==========================
# 사이드바
# ==========================
with st.sidebar:

    st.title("🔥 MENU")

    language = st.selectbox(
        "🌍 Language",
        ["한국어", "English"]
    )

    st.session_state.lang = language

    st.divider()

    if language == "한국어":

        page = st.radio(
            "📌 메뉴",
            ["홈", "산불 예측", "시스템 소개"]
        )

    else:

        page = st.radio(
            "📌 Menu",
            ["Home", "Prediction", "About"]
        )

# ==========================
# 홈
# ==========================
if page in ["홈", "Home"]:

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":

        st.title("🔥 산불위험지수 예측 시스템")

        st.markdown("""
        ## 환영합니다.

        이 시스템은 기상 데이터를 기반으로
        AI가 산불 위험도(FWI)를 예측합니다.

        ### 제공 기능

        - 🔥 산불 위험도 예측
        - 📊 실시간 위험도 계산
        - 🌍 다국어 지원

        왼쪽 메뉴에서 시작하세요.
        """)

    else:

        st.title("🔥 Forest Fire Risk Prediction System")

        st.markdown("""
        ## Welcome

        This system predicts
        Forest Fire Risk (FWI)
        using weather data.

        ### Features

        - 🔥 Fire Risk Prediction
        - 📊 Real-time Risk Analysis
        - 🌍 Multi-language Support

        Start from the left menu.
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# 예측 페이지
# ==========================
elif page in ["산불 예측", "Prediction"]:

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":
        st.title("🔥 산불위험지수 예측")
        st.caption("기상 데이터를 입력하면 AI가 FWI를 예측합니다.")
    else:
        st.title("🔥 Fire Risk Prediction")
        st.caption("Enter weather data to predict FWI.")

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if language == "한국어":
            temperature = st.slider("🌡️ 기온 (°C)", 0.0, 50.0, 30.0, 0.5)
            wind = st.slider("💨 풍속 (km/h)", 0.0, 50.0, 15.0, 0.5)
        else:
            temperature = st.slider("🌡️ Temperature (°C)", 0.0, 50.0, 30.0, 0.5)
            wind = st.slider("💨 Wind Speed (km/h)", 0.0, 50.0, 15.0, 0.5)

    with col2:

        if language == "한국어":
            humidity = st.slider("💧 상대습도 (%)", 0.0, 100.0, 40.0, 1.0)
            rain = st.slider("🌧️ 강수량 (mm)", 0.0, 10.0, 0.0, 0.1)
        else:
            humidity = st.slider("💧 Humidity (%)", 0.0, 100.0, 40.0, 1.0)
            rain = st.slider("🌧️ Rainfall (mm)", 0.0, 10.0, 0.0, 0.1)

    st.write("")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Temperature" if language=="English" else "기온",
                  f"{temperature}°C")

    with m2:
        st.metric("Humidity" if language=="English" else "상대습도",
                  f"{humidity}%")

    with m3:
        st.metric("Wind" if language=="English" else "풍속",
                  f"{wind}km/h")

    with m4:
        st.metric("Rainfall" if language=="English" else "강수량",
                  f"{rain}mm")

    st.write("")

    button_text = (
        "🔍 Predict Fire Risk"
        if language == "English"
        else "🔍 산불위험지수 예측"
    )

    if st.button(button_text):

        input_data = pd.DataFrame(
            [[temperature, humidity, wind, rain]],
            columns=['기온', '상대습도', '풍속', '강수량']
        )

        predicted_fwi = model.predict(input_data)[0]

        if predicted_fwi < 0:
            risk = "Safe"
            desc = "Very low probability of fire."
        elif predicted_fwi < 5.2:
            risk = "Low"
            desc = "Low fire risk."
        elif predicted_fwi < 11.2:
            risk = "Moderate"
            desc = "Possible fire occurrence."
        elif predicted_fwi < 21.3:
            risk = "High"
            desc = "High probability of fire."
        elif predicted_fwi < 38:
            risk = "Very High"
            desc = "Very dangerous condition."
        else:
            risk = "Extreme"
            desc = "Immediate response required."

        if language == "한국어":

            if predicted_fwi < 0:
                risk="안전"
                desc="산불 발생 가능성이 거의 없습니다."
            elif predicted_fwi < 5.2:
                risk="낮음"
                desc="산불 발생 가능성이 낮습니다."
            elif predicted_fwi < 11.2:
                risk="보통"
                desc="주의가 필요합니다."
            elif predicted_fwi < 21.3:
                risk="높음"
                desc="산불 발생 위험이 높습니다."
            elif predicted_fwi < 38:
                risk="매우 높음"
                desc="산불 위험이 매우 높습니다."
            else:
                risk="극도로 위험"
                desc="즉시 대비가 필요합니다."

        st.subheader(
            "📊 Prediction Result"
            if language=="English"
            else "📊 예측 결과"
        )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Predicted FWI"
                if language=="English"
                else "예측 산불위험지수",
                f"{predicted_fwi:.1f}"
            )

        with c2:
            st.metric(
                "Risk Level"
                if language=="English"
                else "위험도",
                risk
            )

        st.info(desc)

        progress = min(predicted_fwi / 38.0, 1.0)
        st.progress(progress)

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# 소개 페이지
# ==========================
else:

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":

        st.title("ℹ️ 시스템 소개")

        st.markdown("""
        ### 산불위험지수(FWI) 예측 시스템

        본 시스템은 기상 데이터를 이용하여
        산불 발생 위험도를 예측합니다.

        #### 사용 변수

        - 기온
        - 상대습도
        - 풍속
        - 강수량

        #### AI 모델

        머신러닝 회귀모델 기반

        #### 데이터

        Algerian Forest Fires Dataset
        """)

    else:

        st.title("ℹ️ About System")

        st.markdown("""
        ### Forest Fire Prediction System

        This system predicts forest fire risk
        using meteorological data.

        #### Variables

        - Temperature
        - Humidity
        - Wind Speed
        - Rainfall

        #### AI Model

        Machine Learning Regression Model

        #### Dataset

        Algerian Forest Fires Dataset
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# Footer
# ==========================
st.divider()

st.markdown("""
<center>
© 2026 Forest Fire Prediction System
</center>
""", unsafe_allow_html=True)
```
