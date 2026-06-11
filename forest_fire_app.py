# app.py
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="산불위험지수 예측 시스템",
    page_icon="🔥",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "home"

st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#1a0a00,#2d1200);
    color:white !important;
}
html, body, h1,h2,h3,h4,h5,h6,p,span,label,div,li,strong,b {
    color:white !important;
}
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#160700,#0f0400);
}
section[data-testid="stSidebar"] *{
    color:white !important;
}
.stSelectbox *{color:white !important;}
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
}
.main-card{
    background:rgba(255,255,255,0.07);
    border-radius:24px;
    padding:30px;
}
[data-testid="metric-container"],
[data-testid="metric-container"] *{
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

# 이하 사용자 기존 코드 계속 사용
