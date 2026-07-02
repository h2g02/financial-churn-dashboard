import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor

# --- 페이지 설정 ---
st.set_page_config(page_title="금융 데이터 분석 포트폴리오", layout="wide")

# 한글 폰트 설정 (Matplotlib)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# --- 사이드바: 섹션 분리 ---
st.sidebar.title("📁 분석 리포트 선택")
selection = st.sidebar.radio("보고서를 선택하세요:", [
    "1. 기업 대출 연체율 시차 분석",
    "2. 신용카드 고객 이탈 세분화",
    "3. 이상거래 탐지(FDS) 성능 리포트"
])

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def get_data(path):
    try:
        return pd.read_csv(path)
    except:
        return None

# --- 섹션 1: 기업 대출 연체율 ---
if selection == "1. 기업 대출 연체율 시차 분석":
    st.title("📈 기업 대출 연체율 및 금리 시차(Lead-Lag) 분석")
    
    df_base = get_data('Include/포폴1_Data/한국은행기준금리.csv')
    df_loan = get_data('Include/포폴1_Data/예금은행대출금리.csv')
    df_delin = get_data('Include/포폴1_Data/은행대출금연체율.csv')
    df_market = get_data('Include/포폴1_Data/회사채_CD수익률.csv')

    if df_base is not None:
        # [데이터 처리 로직]
        def melt_to_long(df, val_name, acc=None, code=None):
            date_cols = [c for c in df.columns if '/' in str(c)]
            mask = pd.Series([True] * len(df))
            if acc: mask &= df['계정항목'].str.strip() == acc
            if code and '구분코드' in df.columns: mask &= df['구분코드'].str.strip() == code
            return df[mask][date_cols].melt(var_name='날짜', value_name=val_name).reset_index(drop=True)

        # 요약 통계량 계산
        st.subheader("📊 1단계: 변수별 기초 통계 및 변동성 요약")
        # 예시 데이터 통합 로직 (노트북 결과 재현)
        summary_data = {
            "mean": [2.45, 4.27, 4.17, 0.53, 0.33, 3.61, 2.83],
            "std": [1.08, 0.89, 0.83, 0.18, 0.10, 0.87, 0.97],
            "min": [0.50, 2.79, 2.74, 0.30, 0.20, 1.83, 0.66],
            "max": [3.50, 5.31, 5.08, 0.90, 0.50, 5.48, 4.02]
        }
        df_summary = pd.DataFrame(summary_data, index=['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '가계연체율', '회사채수익률', 'CD수익률'])
        
        col1, col2 = st.columns([2, 2]) # 테이블 1/2 사이즈
        with col1:
            st.write("**[데이터 요약 및 위험도 분석]**")
            st.table(df_summary) # 가독성을 위해 st.table 사용

        st.divider()

        st.subheader("🎯 2단계: 미래 기업연체율 선행 지표 탐색")
        
        # 상관관계 데이터 (노트북 결과값 기준)
        lag_corr = pd.DataFrame({
            "상관계수": [1.000, 0.692, 0.640, 0.638, 0.588, -0.350]
        }, index=["기업연체율", "기업대출금리_6M전", "CD수익률_6M전", "기업대출금리_5M전", "CD수익률_5M전", "회사채수익률_1M전"])

        col_tbl, col_spacer, col_img = st.columns([2, 0.5, 1.5]) # 테이블 1/2, 이미지 1/4 수준
        
        with col_tbl:
            st.write("**[미래 기업연체율 선행 시차 테이블]**")
            st.dataframe(lag_corr, use_container_width=True)
            
        with col_img:
            st.write("**[시차 상관계수 히트맵]**")
            fig, ax = plt.subplots(figsize=(4, 6))
            sns.heatmap(lag_corr, annot=True, cmap='coolwarm', fmt=".3f", ax=ax)
            st.pyplot(fig)

# --- 섹션 2: 고객 이탈 분석 ---
elif selection == "2. 신용카드 고객 이탈 세분화":
    st.title("💳 신용카드 고객 이탈 패턴 및 세그먼트 분석")
    
    df_card = get_data('Include/포폴2_Data/credit_card_customer.csv')
    
    if df_card is not None:
        df_card = df_card.drop(columns=[c for c in df_card.columns if 'Naive_Bayes' in c])
        
        st.subheader("🔍 1단계: 이탈 집단 vs 유지 집단 주요 지표 비교")
        comparison = df_card.groupby('Attrition_Flag')[['Total_Amt_Chng_Q4_Q1', 'Total_Trans_Ct', 'Contacts_Count_12_mon', 'Avg_Utilization_Ratio']].mean()
        
        col_t1, col_spacer2, col_i1 = st.columns([2, 0.5, 1.5])
        with col_t1:
            st.write("**[집단별 주요 수치 평균]**")
            st.table(comparison)
        with col_i1:
            st.write("**[연락 횟수와 이탈 관계]**")
            fig, ax = plt.subplots(figsize=(4, 3))
            sns.boxplot(x='Attrition_Flag', y='Contacts_Count_12_mon', data=df_card, ax=ax)
            st.pyplot(fig)

        st.divider()

        st.subheader("📊 2단계: 의사결정나무 기반 고객 세분화 결과")
        
        segments = pd.DataFrame({
            "세그먼트": ["Group A (초고위험)", "Group B (잠재적 체리피커)", "Group C (거개저조 유지)", "Group D (불만 폭발)", "Group E (우량 유지)"],
            "핵심 조건": ["거래 < 54회 & 이용률 < 2.7%", "거래 < 54회 & 이용률 < 2.7% & 소비증가", "거래 < 54회 & 이용률 > 2.7%", "거래 > 54회 & 민원 > 5회", "거래 > 54회 & 민원 < 5회"],
            "고객 수": [998, 35, 2425, 16, 6653]
        })

        col_t2, col_spacer3, col_i2 = st.columns([2, 0.5, 1.5])
        with col_t2:
            st.write("**[전략적 고객 분류 테이블]**")
            st.dataframe(segments, hide_index=True, use_container_width=True)
        with col_i2:
            st.write("**[이탈 세그먼트 비중]**")
            fig2, ax2 = plt.subplots(figsize=(4, 4))
            ax2.pie(segments["고객 수"], labels=segments["세그먼트"], autopct='%1.1f%%', startangle=140)
            st.pyplot(fig2)

# --- 섹션 3: 이상거래 탐지 ---
else:
    st.title("🛡️ FDS(이상거래 탐지) 모델 개선 리포트")
    
    st.subheader("🚀 Feature Selection을 통한 오탐지율 개선 성과")
    
    # 성능 비교 테이블
    perf_report = pd.DataFrame({
        "구분": ["개선 전 (Full Features)", "개선 후 (Feature Diet)"],
        "정밀도 (Precision)": ["9.0%", "33.0%"],
        "재현율 (Recall)": ["82.0%", "82.0%"],
        "개선 효과": ["-", "오탐지율 약 3.6배 감소"]
    })

    col_t3, col_spacer4, col_i3 = st.columns([2, 0.5, 1.5])
    with col_t3:
        st.write("**[모델 성능 변화 요약]**")
        st.table(perf_report)
        
        st.write("**[하위 중요도 변수 리스트 (제거 대상)]**")
        low_importance = pd.DataFrame({
            "변수명": ["V20", "V21", "V22", "V23", "V5"],
            "중요도 점수": [330, 334, 377, 426, 428]
        })
        st.dataframe(low_importance, hide_index=True)

    with col_i3:
        st.write("**[최종 모델 변수 중요도 (Top 5)]**")
        # 가상의 중요도 차트
        top_features = pd.DataFrame({
            "Score": [803, 669, 661, 643, 639]
        }, index=["V4", "V27", "V18", "V8", "V1"])
        fig3, ax3 = plt.subplots(figsize=(4, 6))
        top_features.plot(kind='barh', ax=ax3, color='skyblue', legend=False)
        st.pyplot(fig3)
