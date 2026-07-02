import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from matplotlib import font_manager, rc

# --- 1. 한글/영문 통합 가독성 및 깨짐 방지 설정 ---
@st.cache_resource
def setup_environment():
    # 운영체제별 폰트 자동 설정
    system_os = platform.system()
    font_candidates = [
        "Malgun Gothic", "AppleGothic", "NanumGothic", 
        "Noto Sans CJK KR", "Arial"
    ]
    
    selected_font = "sans-serif"
    for f in font_candidates:
        if f in [font.name for font in font_manager.fontManager.ttflist]:
            selected_font = f
            break
            
    # Matplotlib 전역 설정
    plt.rcParams['font.family'] = selected_font
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
    plt.rcParams['font.size'] = 10
    
    # Seaborn 테마 강제 적용
    sns.set_theme(style="whitegrid", font=selected_font)

    # 전문적인 대시보드 스타일링
    st.markdown("""
        <style>
        .main { background-color: #F8F9FA; }
        .report-box {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #E9ECEF;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 25px;
        }
        .metric-card {
            background-color: #E3F2FD;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border-left: 5px solid #1565C0;
        }
        .step-title {
            color: #1565C0;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

setup_environment()

# --- 사이드바 ---
st.sidebar.title("📊 Financial Report")
st.sidebar.info("분석할 리포트 유형을 선택하십시오.")
selection = st.sidebar.radio("", [
    "1. 기업 연체율 시차 분석 (Macro)",
    "2. 고객 이탈 세그먼트 (Retail)",
    "3. FDS 모델 개선 리포트 (Risk)"
])

# --- 섹션 1: 기업 연체율 ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-box'>금리 변화가 기업 건전성에 미치는 영향력을 시차별로 분석하여 조기 경보 지표를 도출합니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("📊 데이터 기초 통계 요약")
        summary_df = pd.DataFrame({
            "항목 (Variable)": ['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '회사채수익률', 'CD수익률'],
            "평균 (Mean)": [2.46, 4.27, 4.17, 0.53, 3.61, 2.83],
            "변동계수 (CV)": [0.44, 0.21, 0.20, 0.33, 0.24, 0.34],
            "최고치 (Max)": [3.50, 5.31, 5.08, 0.90, 5.49, 4.02]
        })
        st.table(summary_df)

    with col2:
        st.subheader("🌡️ 선행 지표 상관도")
        lag_corr = pd.DataFrame({"상관계수": [1.0, 0.69, 0.64, 0.59, -0.35]}, 
                                index=["연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])
        fig, ax = plt.subplots(figsize=(4, 6))
        sns.heatmap(lag_corr, annot=True, cmap='RdYlBu_r', ax=ax, cbar=False)
        ax.set_title("Time-Lag Corr", fontsize=12)
        st.pyplot(fig)

    with col3:
        st.subheader("💡 분석 결과")
        st.info("**6개월의 시차 확인**")
        st.write("금리 인상 후 기업의 이자 부담이 임계치에 도달하여 연체로 이어지는 기간은 평균 6개월로 분석되었습니다.")

# --- 섹션 2: 고객 이탈 ---
elif "2." in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-box'>이탈 고객의 행동적 특징을 분석하여 이탈 방지를 위한 핵심 비즈니스 룰을 수립합니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("🔍 주요 집단 지표 비교")
        df_comp = pd.DataFrame({
            "구분 (Segment)": ["이탈 (Attrited)", "유지 (Existing)"],
            "거래 횟수 (Trans.)": [44.9, 68.7],
            "상담 횟수 (Contact)": [2.97, 2.35],
            "한도 소진 (Util.)": ["16.2%", "29.6%"]
        })
        st.table(df_comp)
        st.error("**핵심 규칙:** 거래 55회 미만 & 한도소진 2.7% 이하 고객 → 타사 카드 주사용자로 분류 (이탈률 72%)")

    with col2:
        st.subheader("📊 상담 횟수 분포")
        fig, ax = plt.subplots(figsize=(5, 8))
        sns.barplot(x=["유지", "이탈"], y=[2.35, 2.97], palette="coolwarm", ax=ax)
        ax.set_title("평균 상담 연락 횟수", fontsize=12)
        st.pyplot(fig)

    with col3:
        st.subheader("📢 대응 전략")
        st.warning("**이탈 징후 감지**")
        st.write("연락 횟수가 3회를 넘어서는 시점에서 소비 변화율을 감지하여 VIP 케어 프로모션을 즉시 실행해야 합니다.")

# --- 섹션 3: FDS 개선 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 성능 개선 리포트")
    st.markdown("<div class='report-box'>데이터 불균형 해결과 변수 정제를 통해 탐지 시스템의 효율성을 극대화하였습니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("🚀 모델 최적화 성과")
        perf_df = pd.DataFrame({
            "성능 지표 (Metric)": ["정밀도 (Precision)", "재현율 (Recall)", "F1-Score", "오탐지율 (FAR)"],
            "초기 모델": ["9.0%", "82.0%", "0.16", "High"],
            "최종 개선": ["33.0%", "82.0%", "0.47", "Reduced (1/3.6)"]
        })
        st.table(perf_df)

    with col2:
        st.subheader("📊 변수 기여도 (Top 5)")
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 8))
        top_v.sort_values().plot(kind='barh', color='#0D47A1', ax=ax)
        ax.set_title("모델 기여도 점수", fontsize=12)
        st.pyplot(fig)

    with col3:
        st.subheader("🛠️ 3단계 개선 조치")
        
        st.markdown("""
        <div class='metric-card'>
            <div class='step-title'>Step 1. 변수 다이어트 (Feature Selection)</div>
            중요도가 낮은 V20, V21 등 노이즈 변수 5종을 제거하여 모델 혼선을 방어함.
        </div>
        <br>
        <div class='metric-card'>
            <div class='step-title'>Step 2. 데이터 불균형 해결 (SMOTE)</div>
            0.17%에 불과한 사기 데이터를 합성하여 정상 데이터와 1:1 비율로 학습.
        </div>
        <br>
        <div class='metric-card'>
            <div class='step-title'>Step 3. 임계치 튜닝 (Threshold)</div>
            탐지 임계치를 0.9로 상향하여 고객 불편(오탐지)을 최소화하고 탐지력 유지.
        </div>
        """, unsafe_allow_html=True)
