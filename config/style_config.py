"""
Streamlit 대시보드의 시각적 스타일을 정의합니다.
Deep Blue (#0047AB) 테마를 기반으로 카드 레이아웃을 적용합니다.
"""
import streamlit as st

def apply_custom_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .stApp {
            max-width: 100%;
        }
        .report-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
            border-top: 4px solid #0047AB;
        }
        .action-step {
            background-color: #F8F9FA;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #0047AB;
            margin-bottom: 12px;
        }
        .step-header {
            font-weight: bold;
            color: #0047AB;
            margin-bottom: 4px;
        }
        .stButton > button {
            background-color: #0047AB;
            color: white;
        }
        .stMetric > div > div {
            color: #0047AB !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
