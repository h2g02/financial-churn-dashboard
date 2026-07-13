"""
Streamlit Financial Analytics Dashboard
사이드바 내비게이션으로 3개의 금융 분석 포트폴리오를 전환합니다.
"""
import streamlit as st
from config import font_config, style_config
from portfolios import portfolio1_report, portfolio2_report, portfolio3_report

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Financial Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- 커스텀 CSS 주입 ---
style_config.apply_custom_css()

# --- 헤더 ---
with st.container():
    st.title("📊 Financial Analytics Dashboard")
    st.markdown("### Macro · Retail · ML — 통합 금융 데이터 분석 포트폴리오")

# --- 사이드바 ---
st.sidebar.title("📁 분석 리포트")
selection = st.sidebar.radio(
    "보고서를 선택하세요:",
    [
        "1. 기업 연체율 시차 분석",
        "2. 신용카드 고객 이탈 분석",
        "3. FDS 성능 개선 조치",
    ],
)

st.sidebar.divider()
st.sidebar.caption(
    "© 2025 Financial Analytics Dashboard\n\n"
    "Built with Streamlit · Pandas · Matplotlib · Seaborn"
)

# --- 라우팅 ---
if "1." in selection:
    portfolio1_report()
elif "2." in selection:
    portfolio2_report()
else:
    portfolio3_report()
