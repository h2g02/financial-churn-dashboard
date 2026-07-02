import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# --- 한글 폰트 설정 (사용자 제공 코드 기반) ---
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# --- 페이지 및 스타일 설정 ---
st.set_page_config(page_title="금융 데이터 분석 센터", layout="wide")
st.markdown("""
    <style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 4px solid #0047AB; }
    .action-step { background-color: #F0F4F8; padding: 15px; border-radius: 10px; border-left: 5px solid #0047AB; margin-bottom: 10px; }
    .step-header { font-weight: bold; color: #0047AB; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 사이드바 ---
st.sidebar.title("📁 분석 리포트")
selection = st.sidebar.radio("보고서 유형", ["1. 기업 연체율 시차 분석", "2. 신용카드 고객 이탈 분석", "3. FDS 성능 개선 조치"])

# --- 섹션 1: 기업 연체율 ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 금리 지표와 기업 연체율 간의 시차 상관관계를 분석합니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("📊 지표별 통계 요약")
        st.table(pd.DataFrame({
            "Variable (항목)": ['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '회사채수익률', 'CD수익률'],
            "Mean (평균)": [2.46, 4.27, 4.17, 0.53, 3.61, 2.83],
            "Volatility (CV)": [0.44, 0.21, 0.20, 0.33, 0.24, 0.34],
            "Max (최고치)": [3.50, 5.31, 5.08, 0.90, 0.50, 5.49, 4.02]
        }))

    with col2:
        st.subheader("🌡️ 상관계수 디자인 수정")
        lag_data = pd.DataFrame({"상관계수": [1.0, 0.69, 0.64, 0.59, -0.35]}, 
                                index=["기업연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])
        
        # [1번 그래프 디자인 수정]
        fig, ax = plt.subplots(figsize=(4, 5))
        sns.heatmap(lag_data, annot=True, cmap='RdYlBu_r', ax=ax, cbar=False,
                    linewidths=1, linecolor='white', annot_kws={"size": 12, "weight": "bold"})
        ax.set_title("시차별 상관관계", fontsize=14, pad=15)
        plt.xticks(rotation=0)
        st.pyplot(fig)

    with col3:
        st.subheader("💡 Key Insight")
        st.success("기업대출금리는 **6개월의 시차**를 두고 연체율과 0.69의 높은 상관관계를 보입니다.")

# --- 섹션 2: 고객 이탈 ---
elif "2." in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 고객의 거래 빈도와 상담 연락 패턴을 분석합니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("🔍 집단 행동 비교")
        st.table(pd.DataFrame({
            "Segment (구분)": ["이탈 고객", "유지 고객"],
            "Trans. Ct (거래횟수)": [44.9, 68.7],
            "Contact (상담횟수)": [2.97, 2.35],
            "Utilization (이용률)": ["16.2%", "29.6%"]
        }))

    with col2:
        st.subheader("📊 상담 횟수 (한글 수정)")
        # [2번 그래프 한글 수정]
        fig, ax = plt.subplots(figsize=(5, 8))
        sns.barplot(x=["유지", "이탈"], y=[2.35, 2.97], palette="Blues_d", ax=ax)
        ax.set_title("고객 상태별 평균 상담 횟수")
        ax.set_xlabel("고객 구분")
        ax.set_ylabel("상담 횟수 (평균)")
        st.pyplot(fig)

    with col3:
        st.subheader("📢 대응 전략")
        st.warning("상담 연락 3회 초과 시 이탈 확률이 급증하므로 관리가 필요합니다.")

# --- 섹션 3: FDS 개선 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 성능 개선")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 모델 최적화 과정과 개선 조치를 설명합니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.subheader("🚀 성능 개선 지표")
        st.table(pd.DataFrame({
            "Metric (지표)": ["정밀도", "재현율", "오탐지 개선"],
            "기존 모델": ["9.0%", "82.0%", "-"],
            "개선 모델": ["33.0%", "82.0%", "3.6배 향상"]
        }))

    with col2:
        st.subheader("📊 변수 기여도 (한글 수정)")
        # [3번 그래프 한글 수정]
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 8))
        top_v.sort_values().plot(kind='barh', color='#0047AB', ax=ax)
        ax.set_title("FDS 모델 주요 변수 기여도")
        ax.set_xlabel("중요도 점수")
        ax.set_ylabel("변수 명칭")
        st.pyplot(fig)

    with col3:
        st.subheader("🛠️ 3단계 개선 조치")
        st.markdown("""
            <div class='action-step'><div class='step-header'>Step 1. 변수 제거</div>노이즈 변수를 제거하여 정밀도 확보.</div>
            <div class='action-step'><div class='step-header'>Step 2. 불균형 보정</div>SMOTE로 사기 비율 최적화.</div>
            <div class='action-step'><div class='step-header'>Step 3. 임계치 튜닝</div>임계치 조정으로 오탐지 감소.</div>
        """, unsafe_allow_html=True)
