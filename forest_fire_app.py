import streamlit as st
import pandas as pd
import joblib
import math

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
# CSS
# ==================================================
st.markdown("""
<style>
/* ── 전체 배경 ── */
.stApp {
    background: linear-gradient(135deg, #1a0a00, #2d1200);
    color: white !important;
}

html, body,
h1, h2, h3, h4, h5, h6,
p, span, label, div, li,
strong, b {
    color: white !important;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #160700, #0f0400);
    border-right: 1px solid rgba(255, 100, 30, 0.2);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ── 언어 셀렉트박스 ── */
/* 선택된 값 표시 영역 */
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2px solid #ff5a36 !important;
    border-radius: 18px !important;
    color: white !important;
}
/* 선택된 텍스트 */
.stSelectbox div[data-baseweb="select"] span {
    color: white !important;
}
/* 드롭다운 리스트 전체 */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background: #2d1200 !important;
    border: 1px solid rgba(255, 90, 54, 0.4) !important;
    border-radius: 12px !important;
}
/* 드롭다운 각 항목 */
li[role="option"],
div[role="option"] {
    background: transparent !important;
    color: white !important;
}
li[role="option"]:hover,
div[role="option"]:hover {
    background: rgba(255, 90, 54, 0.2) !important;
    color: white !important;
}
/* 선택된 항목 */
li[aria-selected="true"],
div[aria-selected="true"] {
    background: rgba(255, 90, 54, 0.3) !important;
    color: white !important;
}

/* ── 사이드바 버튼 너비 통일 ── */
section[data-testid="stSidebar"] .stButton {
    width: 100%;
}
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    min-width: 140px;
    height: 48px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(90deg, #f97316, #ef4444);
    color: white !important;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0.3px;
    transition: 0.25s;
    text-align: left;
    padding-left: 16px;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

/* ── 메인 영역 버튼 ── */
.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(90deg, #f97316, #ef4444);
    color: white !important;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 0.5px;
    transition: 0.25s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

/* ── 메인 카드 ── */
.main-card {
    background: rgba(255, 255, 255, 0.07);
    border-radius: 24px;
    padding: 32px 36px;
    border: 1px solid rgba(255, 150, 50, 0.2);
    margin-bottom: 20px;
}

/* ── 결과 카드 ── */
.result-card {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 20px;
    padding: 24px 28px;
    border: 1px solid rgba(255, 150, 50, 0.3);
    margin-top: 16px;
}

/* ── 인력 카드 ── */
.crew-card {
    background: rgba(99, 102, 241, 0.12);
    border-radius: 20px;
    padding: 24px 28px;
    border: 1px solid rgba(99, 102, 241, 0.3);
    margin-top: 16px;
}

/* ── 슬라이더 ── */
[data-testid="stSlider"] label {
    color: white !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
[data-testid="stSlider"] p {
    color: #ffb347 !important;
    font-weight: bold !important;
}

/* ── 메트릭 ── */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
[data-testid="metric-container"] * { color: white !important; }
[data-testid="stMetricValue"] { color: white !important; }

/* ── 알림 ── */
[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
}
[data-testid="stAlert"] * { color: white !important; }

/* ── 테이블 ── */
table { color: white !important; }
thead tr th { color: white !important; border-bottom: 1px solid rgba(255,255,255,0.2) !important; }
tbody tr td { color: white !important; border-bottom: 1px solid rgba(255,255,255,0.08) !important; }

/* ── 기타 ── */
.stMarkdown, .stMarkdown * { color: white !important; }
.footer { color: white !important; text-align: center; font-size: 13px; opacity: 0.5; }
hr { border-color: rgba(255, 255, 255, 0.12) !important; }

/* ── 프로그레스 바 ── */
[data-testid="stProgressBar"] > div {
    background: linear-gradient(90deg, #22c55e, #eab308, #f97316, #ef4444) !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 모델 로드
# ==================================================
model = joblib.load("forest_fire_model.pkl")

# ==================================================
# 인력 산정 함수
# ==================================================
def estimate_crew(fwi: float, area_ha: float = 10.0) -> dict:
    """
    FWI 및 예상 피해 면적(ha)을 기반으로 필요 인력을 산정합니다.
    기준: 산림청 산불 진화 인력 배치 지침 참고 (단계별 가중치 적용)
    """
    if fwi < 5.2:        # 낮음
        base, multiplier = 5,  1.0
    elif fwi < 11.2:     # 보통
        base, multiplier = 10, 1.2
    elif fwi < 21.3:     # 높음
        base, multiplier = 20, 1.5
    elif fwi < 38:       # 매우 높음
        base, multiplier = 35, 1.8
    else:                # 극위험
        base, multiplier = 60, 2.2

    area_factor = max(1.0, math.log10(area_ha + 1) * 1.5)
    total = math.ceil(base * multiplier * area_factor)

    crew = {
        "🚒 초동 진화대":   math.ceil(total * 0.42),
        "🪖 산림청 특수대": math.ceil(total * 0.26),
        "🚑 응급·구조대":   math.ceil(total * 0.18),
        "🎯 지휘·통제반":   math.ceil(total * 0.14),
    }
    crew["합계"] = sum(crew.values())
    return crew

# ==================================================
# 위험 단계 분류
# ==================================================
def classify_risk(fwi: float, lang: str) -> tuple:
    ko     = ["낮음", "보통", "높음", "매우 높음", "극도로 위험"]
    en     = ["Low", "Moderate", "High", "Very High", "Extreme"]
    colors = ["#22c55e", "#eab308", "#f97316", "#ef4444", "#991b1b"]
    if fwi < 5.2:    i = 0
    elif fwi < 11.2: i = 1
    elif fwi < 21.3: i = 2
    elif fwi < 38:   i = 3
    else:            i = 4
    label = ko[i] if lang == "한국어" else en[i]
    return label, colors[i]

# ==================================================
# 사이드바
# ==================================================
with st.sidebar:
    st.markdown("## 🌍 Language")
    language = st.selectbox("", ["한국어", "English"])
    st.divider()

    if language == "한국어":
        st.markdown("## 📌 메뉴")
        if st.button("🏠 홈"):           st.session_state.page = "home"
        if st.button("🔥 산불 예측"):   st.session_state.page = "predict"
        if st.button("ℹ️ 시스템 소개"): st.session_state.page = "about"
    else:
        st.markdown("## 📌 Menu")
        if st.button("🏠 Home"):         st.session_state.page = "home"
        if st.button("🔥 Prediction"):   st.session_state.page = "predict"
        if st.button("ℹ️ About"):        st.session_state.page = "about"

    st.divider()
    st.markdown(
        "<div style='font-size:11px;opacity:.4;text-align:center'>© 2026 ForestAI v1.0</div>",
        unsafe_allow_html=True
    )

# ==================================================
# 홈 화면
# ==================================================
if st.session_state.page == "home":
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":
        st.title("🔥 산불위험지수 예측 시스템")
        st.markdown("""
        ### 환영합니다

        이 시스템은 **AI 머신러닝 모델**을 활용해 기상 조건을 분석하고,
        **산불위험지수(FWI)** 및 **예상 필요 인력**을 실시간으로 예측합니다.

        #### 입력 변수
        - 🌡️ **기온** (°C)
        - 💧 **상대습도** (%)
        - 💨 **풍속** (km/h)
        - 🌧️ **강수량** (mm)

        #### 출력 결과
        - 📊 **FWI 예측값** — 산불 기상 위험 지수
        - 🚨 **위험 등급** — 낮음 / 보통 / 높음 / 매우 높음 / 극위험
        - 👥 **예상 필요 인력** — 역할별 인원 산정

        왼쪽 메뉴에서 **🔥 산불 예측**을 선택하세요.
        """)
    else:
        st.title("🔥 Forest Fire Risk Prediction System")
        st.markdown("""
        ### Welcome

        Thissystem analyzes weather conditions in real-time to predict
        the **Fire Weather Index (FWI)** and estimate the **required response crew**.

        #### Input Variables
        - 🌡️ **Temperature** (°C)
        - 💧 **Humidity** (%)
        - 💨 **Wind Speed** (km/h)
        - 🌧️ **Rainfall** (mm)

        #### Output
        - 📊 **Predicted FWI** — Fire Weather Index score
        - 🚨 **Risk Level** — Low / Moderate / High / Very High / Extreme
        - 👥 **Estimated Crew** — Personnel by role

        Select **🔥 Prediction** from the left menu.
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 예측 화면
# ==================================================
elif st.session_state.page == "predict":
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":
        st.title("🔥 산불위험지수 예측")
        st.caption("기상 데이터를 입력하고 예측 버튼을 누르세요.")
    else:
        st.title("🔥 Fire Risk Prediction")
        st.caption("Enter weather data and press the predict button.")

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider(
            "🌡️ 기온 (°C)" if language == "한국어" else "🌡️ Temperature (°C)",
            0.0, 50.0, 30.0, 0.5
        )
        wind = st.slider(
            "💨 풍속 (km/h)" if language == "한국어" else "💨 Wind Speed (km/h)",
            0.0, 50.0, 15.0, 0.5
        )
    with col2:
        humidity = st.slider(
            "💧 상대습도 (%)" if language == "한국어" else "💧 Humidity (%)",
            0.0, 100.0, 40.0, 1.0
        )
        rain = st.slider(
            "🌧️ 강수량 (mm)" if language == "한국어" else "🌧️ Rainfall (mm)",
            0.0, 10.0, 0.0, 0.1
        )

    st.divider()
    area_ha = st.slider(
        "🌲 예상 피해 면적 (ha)" if language == "한국어" else "🌲 Estimated Affected Area (ha)",
        1.0, 500.0, 10.0, 1.0
    )

    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("기온"   if language == "한국어" else "Temp",     f"{temperature}°C")
    m2.metric("습도"   if language == "한국어" else "Humidity", f"{humidity}%")
    m3.metric("풍속"   if language == "한국어" else "Wind",     f"{wind} km/h")
    m4.metric("강수량" if language == "한국어" else "Rain",     f"{rain} mm")

    st.markdown("</div>", unsafe_allow_html=True)

    predict_label = "🔍 산불위험지수 예측하기" if language == "한국어" else "🔍 Predict Fire Risk"
    if st.button(predict_label):

        input_df = pd.DataFrame(
            [[temperature, humidity, wind, rain]],
            columns=["기온", "상대습도", "풍속", "강수량"]
        )
        predicted_fwi = model.predict(input_df)[0]
        risk_label, risk_color = classify_risk(predicted_fwi, language)
        crew = estimate_crew(predicted_fwi, area_ha)

        # ── 예측 결과 카드 ──
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.subheader("📊 예측 결과" if language == "한국어" else "📊 Prediction Result")

        r1, r2 = st.columns(2)
        r1.metric("예측 FWI" if language == "한국어" else "Predicted FWI", f"{predicted_fwi:.2f}")
        r2.metric("위험도"   if language == "한국어" else "Risk Level",    risk_label)

        st.markdown(
            f"<p style='font-size:12px;opacity:.6;margin-bottom:4px'>"
            f"위험 단계: <strong style='color:{risk_color}'>{risk_label}</strong>"
            f" &nbsp;|&nbsp; FWI {predicted_fwi:.1f} / 38+</p>",
            unsafe_allow_html=True
        )
        st.progress(min(predicted_fwi / 38.0, 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

        # ── 인력 산정 카드 ──
        st.markdown("<div class='crew-card'>", unsafe_allow_html=True)

        if language == "한국어":
            st.subheader(f"👥 예상 필요 인력  —  총 {crew['합계']}명")
            st.caption(f"예상 피해 면적 {area_ha:.0f}ha · 위험도 '{risk_label}' 기준 산정")
        else:
            st.subheader(f"👥 Estimated Crew  —  Total {crew['합계']} personnel")
            st.caption(f"Based on {area_ha:.0f}ha affected area · Risk level '{risk_label}'")

        c1, c2, c3, c4 = st.columns(4)
        cols  = [c1, c2, c3, c4]
        roles = [k for k in crew if k != "합계"]
        for col, role in zip(cols, roles):
            col.metric(role, f"{crew[role]}명" if language == "한국어" else f"{crew[role]} ppl")

        st.divider()
        for role in roles:
            pct        = crew[role] / crew["합계"]
            bar_filled = int(pct * 30)
            bar        = "█" * bar_filled + "░" * (30 - bar_filled)
            st.markdown(
                f"<p style='font-size:13px;font-family:monospace'>"
                f"{role} &nbsp; <span style='color:#a78bfa'>{bar}</span>"
                f" &nbsp; {crew[role]}명 ({pct*100:.0f}%)</p>",
                unsafe_allow_html=True
            )

        if language == "한국어":
            st.info("ℹ️ 인력 산정은 산림청 산불 진화 지침 및 FWI·피해 면적 기반 추정치입니다. 실제 현장 상황에 따라 조정이 필요합니다.")
        else:
            st.info("ℹ️ Crew estimates are based on Korea Forest Service guidelines and FWI·area factors. Adjust according to actual site conditions.")

        st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 시스템 소개
# ==================================================
elif st.session_state.page == "about":
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if language == "한국어":
        st.title("ℹ️ 시스템 소개")
        st.markdown("""
        ### 산불위험지수(FWI) 예측 시스템

        기상 데이터를 기반으로 산불 발생 위험도를 예측하는 AI 시스템입니다.

        ---

        #### 🤖 모델 정보
        | 항목 | 내용 |
        |------|------|
        | 알고리즘 | 부스팅 회귀 (Gradient Boosting) |
        | R² 결정계수 | 0.654 (선형회귀 0.413 / 랜덤포레스트 0.617 대비 최고) |
        | 학습 데이터 | Algerian Forest Fires Dataset (2012.6 ~ 9월) |
        | 학습 지역 | 알제리 북부 2개 지역 |
        | 입력 변수 | 기온, 상대습도, 풍속, 강수량 |
        | 출력 | FWI 예측값, 위험 등급, 예상 인력 |

        ---

        #### 🚨 위험 등급 판단 기준 (FWI 구간)

        | 등급 | FWI 범위 | 설명 | 권고 조치 |
        |------|----------|------|-----------|
        | 🟢 낮음 | 0 ~ 5.2 | 산불 발생 가능성 낮음 | 일반 모니터링 |
        | 🟡 보통 | 5.2 ~ 11.2 | 건조 시 주의 필요 | 순찰 강화 |
        | 🟠 높음 | 11.2 ~ 21.3 | 산불 발생 위험 존재 | 진화 대기 |
        | 🔴 매우 높음 | 21.3 ~ 38 | 빠른 확산 가능 | 즉각 대응 |
        | 🔴 극위험 | 38 이상 | 대형 산불 위험 | 비상 대응 체계 가동 |

        ---

        #### 👥 예상 인력 산정 기준

        | 역할 | 비율 | 임무 |
        |------|------|------|
        | 🚒 초동 진화대 | 42% | 현장 직접 진화 |
        | 🪖 산림청 특수대 | 26% | 고위험 구역 투입 |
        | 🚑 응급·구조대 | 18% | 인명 구조 및 응급 처치 |
        | 🎯 지휘·통제반 | 14% | 현장 지휘 및 자원 조율 |

        > 총 인력 = (FWI 단계별 기준 인원) × (피해 면적 가중치)  
        > 피해 면적 가중치 = log₁₀(면적 + 1) × 1.5 (최솟값 1.0)

        ---

        #### 📊 주요 상관관계 (학습 데이터 기준)
        | 변수 | 산불 발생과의 상관계수 | 방향 |
        |------|----------------------|------|
        | 기온 | 0.52 | 기온 높을수록 위험 ↑ |
        | 가뭄지수 | 0.51 | 건조할수록 위험 ↑ |
        | 상대습도 | -0.43 | 습도 높을수록 위험 ↓ |
        | 강수량 | -0.38 | 강수 많을수록 위험 ↓ |
        | 풍속 | -0.07 | 상관 미미 |
        """)
    else:
        st.title("ℹ️ About System")
        st.markdown("""
        ### Forest Fire Risk Prediction System

        AI system that predicts forest fire risk based on weather data.

        ---

        #### 🤖 Model Info
        | Item | Detail |
        |------|--------|
        | Algorithm | Gradient Boosting Regression |
        | R² Score | 0.654 (best vs Linear 0.413 / RF 0.617) |
        | Training Data | Algerian Forest Fires Dataset (Jun–Sep 2012) |
        | Region | 2 regions in northern Algeria |
        | Input Variables | Temp, Humidity, Wind, Rainfall |
        | Output | FWI score, Risk level, Crew estimate |

        ---

        #### 🚨 Risk Level Criteria (FWI Range)

        | Level | FWI Range | Description | Action |
        |-------|-----------|-------------|--------|
        | 🟢 Low | 0 ~ 5.2 | Low fire risk | Routine monitoring |
        | 🟡 Moderate | 5.2 ~ 11.2 | Caution in dry conditions | Increase patrol |
        | 🟠 High | 11.2 ~ 21.3 | Fire risk present | Standby crews |
        | 🔴 Very High | 21.3 ~ 38 | Rapid spread possible | Immediate response |
        | 🔴 Extreme | 38+ | Large-scale fire risk | Emergency response |

        ---

        #### 👥 Crew Estimation Criteria

        | Role | Ratio | Duty |
        |------|-------|------|
        | 🚒 Initial Attack Crew | 42% | Direct firefighting |
        | 🪖 Forest Service Special Unit | 26% | High-risk zones |
        | 🚑 Emergency & Rescue | 18% | Life safety & first aid |
        | 🎯 Command & Control | 14% | On-site coordination |

        > Total crew = (FWI-based base) × (area weight factor)  
        > Area weight = log₁₀(area + 1) × 1.5 (minimum 1.0)

        ---

        #### 📊 Key Correlations (from training data)
        | Variable | Correlation with Fire | Direction |
        |----------|-----------------------|-----------|
        | Temperature | 0.52 | Higher temp → higher risk ↑ |
        | Drought Index | 0.51 | Drier → higher risk ↑ |
        | Humidity | -0.43 | Higher humidity → lower risk ↓ |
        | Rainfall | -0.38 | More rain → lower risk ↓ |
        | Wind Speed | -0.07 | Minimal correlation |
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 푸터
# ==================================================
st.divider()
st.markdown(
    '<div class="footer">© 2026 Forest Fire Prediction System</div>',
    unsafe_allow_html=True
)
