import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from matplotlib import font_manager, rc

# --- 1. 한글 및 영문 가독성 폰트 설정 ---
@st.cache_resource
def setup_design():
    # 운영체제별 폰트 설정
    curr_os = platform.system()
    if curr_os == "Windows":
        font_path = "c:/Windows/Fonts/malgun.ttf"
    elif curr_os == "Darwin":
        font_path = "/Library/Fonts/AppleGothic.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    
    try:
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font_name)
    except:
        rc('font', family='sans-serif')
        
    plt.rcParams['axes.unicode_minus'] = False
    # 디자인 개선을 위한 스타일 시트
    st.markdown("""
        <style>
        .report-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 5px solid #1E88E5;
        }
        .stTitle { color: #0E1117; font-weight: 800; }
        .stSubheader { color: #1E88E5; font-weight: 600; }
        </style>
    """, unsafe_allow_html=True)

setup_design()

# --- 데이터 로드 함수 ---
def load_csv(path):
    try: return pd.read_csv(path)
    except: return None

# --- 사이드바 ---
st.sidebar.markdown("# 🚀 금융 분석 센터")
selection = st.sidebar.selectbox("분석 리포트 변경", [
    "📈 기업 연체율 시차 분석",
    "💳 카드 고객 이탈 세분화",
    "🛡️ FDS 모델 성능 진단"
])

# --- 섹션 1: 기업 연체율 ---
if "기업" in selection:
    st.title("📈 기업 대출 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>분석 요약:</b> 금리 인상이 실제 기업 부실로 이어지는 6개월의 골든타임을 정량적으로 증명합니다.</div>", unsafe_allow_html=True)

    summary_df = pd.DataFrame({
        "Variable (항목)": ['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '가계연체율', '회사채수익률', 'CD수익률'],
        "Mean (평균)": [2.46, 4.27, 4.17, 0.53, 0.33, 3.61, 2.83],
        "Volatility (변동성)": ["Medium", "High", "Low", "Critical", "Stable", "High", "Very High"],
        "Max (최고치)": [3.50, 5.31, 5.08, 0.90, 0.50, 5.49, 4.02]
    })

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("📊 지표별 기초 통계 요약")
        st.table(summary_df)
    with col2:
        st.subheader("🌡️ 시차 상관계수")
        lag_data = pd.DataFrame({"Corr": [1.0, 0.69, 0.64, 0.59, -0.35]}, 
                                index=["연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])
        fig, ax = plt.subplots(figsize=(4, 5))
        sns.heatmap(lag_data, annot=True, cmap='coolwarm', ax=ax, cbar=False, annot_kws={"size": 13})
        st.pyplot(fig)
    with col3:
        st.subheader("💡 인사이트")
        st.success("기업대출금리는 **6개월 전** 수치가 현재 연체율을 69%의 확률로 설명합니다. 선행 지표로서의 가치가 매우 높습니다.")

# --- 섹션 2: 고객 이탈 ---
elif "카드" in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-card'><b>분석 요약:</b> 거래 빈도와 한도 소진율의 결합 패턴을 통해 이탈 고위험군을 식별합니다.</div>", unsafe_allow_html=True)

    df_comp = pd.DataFrame({
        "Segment (구분)": ["이탈 고객 (Attrited)", "유지 고객 (Existing)"],
        "Trans. Count (거래 횟수)": [44.9, 68.7],
        "Contacts (상담 횟수)": [2.97, 2.35],
        "Utilization (한도소진율)": ["16.2%", "29.6%"]
    })

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("🔍 집단별 행동 패턴 비교")
        st.table(df_comp)
        st.info("**Decision Tree Rule:** 거래 55회 미만 & 이용률 2.7% 이하 → 이탈률 72% (초고위험군)")
    with col2:
        st.subheader("📉 연락 빈도 분포")
        # 더 세련된 색상 적용
        fig, ax = plt.subplots(figsize=(5, 7))
        sns.barplot(x=["유지", "이탈"], y=[2.35, 2.97], palette="Blues_d", ax=ax)
        ax.set_ylabel("평균 상담 횟수")
        st.pyplot(fig)
    with col3:
        st.subheader("📢 마케팅 제언")
        st.warning("상담 연락이 **4회 이상**인 고객에게는 즉시 해피콜 또는 전용 바우처를 발송하여 이탈을 방어해야 합니다.")

# --- 섹션 3: FDS 성능 ---
else:
    st.title("🛡️ 이상거래 탐지(FDS) 성능 개선")
    st.markdown("<div class='report-card'><b>분석 요약:</b> 노이즈 변수 제거를 통해 정밀도를 3.6배 향상시킨 모델 다이어트 결과입니다.</div>", unsafe_allow_html=True)

    perf_df = pd.DataFrame({
        "Metric (지표)": ["Precision (정밀도)", "Recall (재현율)", "False Alarm (오탐지)"],
        "Base Model": ["9.0%", "82.0%", "Very High"],
        "Optimized (개선)": ["33.0%", "82.0%", "Low (Improved)"]
    })

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("🚀 성능 개선 성과")
        st.table(perf_df)
    with col2:
        st.subheader("📊 변수 중요도")
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 8))
        top_v.sort_values().plot(kind='barh', color='#1E88E5', ax=ax)
        st.pyplot(fig)
    with col3:
        st.subheader("🛠 개선 조치")
        st.help("중요도가 낮은 V20, V21 등의 변수를 제거하여 모델의 복잡도를 낮추고 실제 사기 탐지 정확도를 높였습니다.")
