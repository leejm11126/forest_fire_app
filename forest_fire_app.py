# Updated app.py
# CSS fixed for dropdown menu text color

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="산불위험지수 예측 시스템", page_icon="🔥", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

st.markdown('''
<style>
.stApp{
    background: linear-gradient(135deg,#1a0a00,#2d1200);
    color:white !important;
}

html, body,
h1,h2,h3,h4,h5,h6,
p, label,
strong, b {
    color:white !important;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* dropdown selected */
.stSelectbox div[data-baseweb="select"] > div{
    background:#1a0a00 !important;
    color:white !important;
    border:2px solid #ff5a36 !important;
    border-radius:18px !important;
}

/* dropdown menu text */
div[role="listbox"] *{
    color:black !important;
}
</style>
''', unsafe_allow_html=True)

# 나머지 코드는 사용자가 올린 기존 코드 그대로 사용
