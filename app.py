import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from matplotlib import font_manager, rc

# --- 1. 한글 폰트 설정 (환경별 자동 감지) ---
def set_korean_font():
    system_os = platform.system()
    try:
        if system_os == "Windows":
            font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
            rc('font', family=font_name)
        elif system_os == "Darwin": # Mac
            rc('font', family='AppleGothic')
        else: # Linux (Streamlit Cloud 등)
            rc('font', family='NanumGothic')
    except:
        # 폰트가 없을 경우 기본 고딕 계열 설정
        rc('font', family='sans-serif')
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# --- 페이지 설정 ---
st.set_page_config(page_title="금융 데이터 분석 포트폴리오", layout="wide")

# --- 사이드바: 섹션 분리 ---
st.sidebar.title("📁 분석 리포트 선택")
selection = st.sidebar.radio("보고서를 선택하세요:", [
    "1. 기업 대출 연체율 시차 분석",
    "2. 신용카드 고객 이탈 세분화",
    "3. 이상거래 탐지(FDS) 성능 리포트"
])

# 데이터 로드 함수
@st.cache_data
def get_data(path):
    try:
        return pd.read_csv(path)
    except:
        return None

# --- 섹션 1: 기업 대출 연체율 ---
if selection == "1. 기업 대출 연체율 시차 분석":
    st.title("📈 기업 대출 연체율 및 금리 시차(Lead-Lag) 분석")
    
    st.subheader("📊 1단계: 변수별 기초 통계 및 변동성 요약")
    summary_data = {
        "평균(mean)": [2.45, 4.27, 4.17, 0.53, 0.33, 3.61, 2.83],
        "표준편차(std)": [1.08, 0.89, 0.83, 0.18, 0.10, 0.87, 0.97],
        "최솟값(min)": [0.50, 2.79, 2.74, 0.30, 0.20, 1.83, 0.66],
        "최댓값(max)": [3.50, 5.31, 5.08, 0.90, 0.50, 5.48, 4.02]
    }
    df_summary = pd.DataFrame(summary_data, index=['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '가계연체율', '회사채수익률', 'CD수익률'])
    
    col1, col2 = st.columns([2, 2]) # 표 1/2 사이즈
    with col1:
        st.write("**[데이터 요약 및 위험도 분석 테이블]**")
        st.table(df_summary)

    st.divider()
    st.subheader("🎯 2단계: 미래 기업연체율 선행 지표 탐색")
    
    lag_corr = pd.DataFrame({
        "상관계수": [1.000, 0.692, 0.640, 0.638, 0.588, -0.350]
    }, index=["기업연체율", "기업대출금리_6M전", "CD수익률_6M전", "기업대출금리_5M전", "CD수익률_5M전", "회사채수익률_1M전"])

    # 표 1/2 (비중 2), 그래프 1/4 (비중 1.5) 레이아웃
    col_tbl, col_spacer, col_img = st.columns([2, 0.5, 1.5]) 
    
    with col_tbl:
        st.write("**[선행 시차 상관계수 테이블]**")
        st.dataframe(lag_corr, use_container_width=True)
        
    with col_img:
        st.write("**[시차 상관관계 히트맵]**")
        fig, ax = plt.subplots(figsize=(3, 5)) # 그래프 크기 최적화
        sns.heatmap(lag_corr, annot=True, cmap='coolwarm', fmt=".3f", ax=ax)
        st.pyplot(fig)

# --- 섹션 2: 고객 이탈 분석 ---
elif selection == "2. 신용카드 고객 이탈 세분화":
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    
    df_card = get_data('Include/포폴2_Data/credit_card_customer.csv')
    
    if df_card is not None:
        st.subheader("🔍 1단계: 집단별 주요 지표 비교")
        comparison = df_card.groupby('Attrition_Flag')[['Total_Trans_Ct', 'Contacts_Count_12_mon', 'Avg_Utilization_Ratio']].mean()
        comparison.index = ['이탈 고객', '유지 고객']
        comparison.columns = ['총 거래 횟수', '상담 연락 횟수', '평균 한도 소진율']
        
        col_t1, col_spacer2, col_i1 = st.columns([2, 0.5, 1.5])
        with col_t1:
            st.write("**[집단별 평균 수치]**")
            st.table(comparison)
        with col_i1:
            st.write("**[연락 횟수별 이탈 분포]**")
            fig, ax = plt.subplots(figsize=(4, 3))
            sns.boxplot(x='Attrition_Flag', y='Contacts_Count_12_mon', data=df_card, ax=ax)
            ax.set_xticklabels(['유지', '이탈'])
            st.pyplot(fig)

        st.divider()
        st.subheader("📊 2단계: 전략적 고객 세분화(Segmentation)")
        
        segments = pd.DataFrame({
            "그룹명": ["Group A", "Group B", "Group C", "Group D", "Group E"],
            "상태": ["초고위험", "체리피커", "이용저조", "민원폭발", "우량유지"],
            "고객 수": [998, 35, 2425, 16, 6653],
            "이탈률 예측": ["72.0%", "15.4%", "10.2%", "100.0%", "2.1%"]
        })

        col_t2, col_spacer3, col_i2 = st.columns([2, 0.5, 1.5])
        with col_t2:
            st.write("**[세그먼트별 분류 통계]**")
            st.dataframe(segments, hide_index=True, use_container_width=True)
        with col_i2:
            st.write("**[고객군 비중]**")
            fig2, ax2 = plt.subplots(figsize=(4, 4))
            ax2.pie(segments["고객 수"], labels=segments["그룹명"], autopct='%1.1f%%', startangle=140)
            st.pyplot(fig2)

# --- 섹션 3: 이상거래 탐지 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 모델 리포트")
    
    col_t3, col_spacer4, col_i3 = st.columns([2, 0.5, 1.5])
    with col_t3:
        st.write("**[모델 개선 성과 요약]**")
        perf_report = pd.DataFrame({
            "평가 지표": ["정밀도 (Precision)", "재현율 (Recall)", "오탐지율(False Alarm)"],
            "개선 전": ["9.0%", "82.0%", "높음"],
            "개선 후": ["33.0%", "82.0%", "낮음 (3.6배 개선)"]
        })
        st.table(perf_report)
        
        st.write("**[제거된 노이즈 변수 점수]**")
        low_imp = pd.DataFrame({"변수": ["V20", "V21", "V22"], "중요도": [330, 334, 377]})
        st.dataframe(low_imp, use_container_width=True)

    with col_i3:
        st.write("**[핵심 변수 중요도 Top 5]**")
        top_features = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig3, ax3 = plt.subplots(figsize=(4, 6))
        top_features.sort_values().plot(kind='barh', ax=ax3, color='orange')
        ax3.set_title("모델 기여도 점수")
        st.pyplot(fig3)
