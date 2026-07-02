import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# --- 1. 사용자 제공 한글 폰트 설정 적용 ---
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# --- 2. 디자인 및 가독성 개선 (CSS) ---
st.set_page_config(page_title="금융 데이터 분석 센터", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F9FAFB; }
    .report-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-top: 4px solid #0047AB;
    }
    .action-step {
        background-color: #F0F4F8;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0047AB;
        margin-bottom: 10px;
    }
    .step-header {
        font-weight: bold;
        color: #0047AB;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 사이드바 ---
st.sidebar.title("📁 분석 리포트")
selection = st.sidebar.radio("보고서 유형", [
    "1. 기업 연체율 시차 분석",
    "2. 신용카드 고객 이탈 분석",
    "3. FDS 성능 개선 조치"
])

# --- 섹션 1: 기업 연체율 ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 거시경제 지표인 금리와 기업의 건전성 사이의 상관관계를 시차별(Time-Lag)로 분석합니다.</div>", unsafe_allow_html=True)

    # 레이아웃: 표(2/4) : 그래프(1/4) : 인사이트(1/4)
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("📊 지표별 통계 요약")
        summary_df = pd.DataFrame({
            "Variable (항목)": ['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '회사채수익률', 'CD수익률'],
            "Mean (평균)": [2.46, 4.27, 4.17, 0.53, 3.61, 2.83],
            "Volatility (CV)": [0.44, 0.21, 0.20, 0.33, 0.24, 0.34],
            "Max (최고치)": [3.50, 5.31, 5.08, 0.90, 5.49, 4.02]
        })
        st.table(summary_df)

    with col2:
        st.subheader("🌡️ 상관계수")
        lag_data = pd.DataFrame({"상관계수": [1.0, 0.69, 0.64, 0.59, -0.35]}, 
                                index=["연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])
        fig, ax = plt.subplots(figsize=(4, 5))
        sns.heatmap(lag_data, annot=True, cmap='coolwarm', ax=ax, cbar=False)
        st.pyplot(fig)

    with col3:
        st.subheader("💡 Key Insight")
        st.success("기업대출금리는 **6개월의 시차**를 두고 연체율과 0.69의 높은 상관관계를 보입니다. 이는 리스크 관리의 골든타임을 의미합니다.")

# --- 섹션 2: 고객 이탈 ---
elif "2." in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 고객의 거래 빈도와 상담 연락 패턴을 분석하여 이탈 징후를 사전 포착합니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🔍 집단 행동 비교")
        df_comp = pd.DataFrame({
            "Segment (구분)": ["이탈 고객 (Attrited)", "유지 고객 (Existing)"],
            "Trans. Ct (거래횟수)": [44.9, 68.7],
            "Contact (상담횟수)": [2.97, 2.35],
            "Utilization (이용률)": ["16.2%", "29.6%"]
        })
        st.table(df_comp)
        st.error("**Rule:** 거래 55회 미만 & 이용률 2.7% 이하 → 이탈률 72%")

    with col2:
        st.subheader("📊 상담 횟수 분포")
        fig, ax = plt.subplots(figsize=(5, 8))
        sns.barplot(x=["유지", "이탈"], y=[2.35, 2.97], palette="Blues", ax=ax)
        ax.set_title("평균 상담 횟수 비교")
        st.pyplot(fig)

    with col3:
        st.subheader("📢 대응 전략")
        st.warning("상담 연락 3회 초과 시, 해당 고객의 이탈 확률이 급증하므로 전담 상담원 배정이 필요합니다.")

# --- 섹션 3: FDS 개선 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 모델 개선")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 정밀도(Precision)를 3.6배 향상시킨 모델 최적화 과정과 개선 조치를 설명합니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🚀 성능 개선 지표")
        perf_df = pd.DataFrame({
            "Metric (지표)": ["Precision (정밀도)", "Recall (재현율)", "오탐지 개선"],
            "기존 모델": ["9.0%", "82.0%", "-"],
            "개선 모델": ["33.0%", "82.0%", "3.6배 향상"]
        })
        st.table(perf_df)

    with col2:
        st.subheader("📊 변수 기여도")
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 8))
        top_v.sort_values().plot(kind='barh', color='#0047AB', ax=ax)
        ax.set_title("핵심 변수 점수")
        st.pyplot(fig)

    with col3:
        st.subheader("🛠️ 3단계 개선 조치")
        st.markdown("""
            <div class='action-step'>
                <div class='step-header'>Step 1. 변수 제거 (Diet)</div>
                중요도가 낮은 V20, V21 등 노이즈 변수를 제거하여 모델 정밀도 확보.
            </div>
            <div class='action-step'>
                <div class='step-header'>Step 2. 불균형 보정 (SMOTE)</div>
                0.17%의 희소 데이터를 합성하여 정상/사기 비율을 최적화함.
            </div>
            <div class='action-step'>
                <div class='step-header'>Step 3. 임계치 튜닝</div>
                탐지 임계치를 0.9로 조정하여 고객 불편(오탐지)을 획기적으로 낮춤.
            </div>
        """, unsafe_allow_html=True)
