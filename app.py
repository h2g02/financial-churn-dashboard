import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from matplotlib import font_manager, rc

# --- 1. 한글 폰트 및 마이너스 깨짐 완벽 방지 설정 ---
def apply_korean_font():
    system_os = platform.system()
    if system_os == "Windows":
        font_path = "c:/Windows/Fonts/malgun.ttf"
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font_name)
    elif system_os == "Darwin": # Mac
        rc('font', family='AppleGothic')
    else: # Streamlit Cloud / Linux
        # 나눔고딕이 설치되어 있지 않을 경우를 대비해 폰트 경로를 직접 지정하거나 기본 고딕 설정
        try:
            rc('font', family='NanumGothic')
        except:
            rc('font', family='sans-serif')
            
    # 그래프 내 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    # Seaborn 폰트 설정 동기화
    sns.set(font=plt.rcParams['font.family'], rc={'axes.unicode_minus': False})

apply_korean_font()

# --- 페이지 설정 ---
st.set_page_config(page_title="금융 데이터 분석 대시보드", layout="wide")

# 사이드바 레이아웃
st.sidebar.title("📊 분석 프로젝트")
selection = st.sidebar.radio("보고서 선택:", [
    "1. 기업 대출 연체율 분석",
    "2. 신용카드 고객 이탈 분석",
    "3. 이상거래 탐지 성능 리포트"
])

# 데이터 로드 (캐시 사용)
@st.cache_data
def get_data(path):
    try:
        return pd.read_csv(path)
    except:
        return None

# --- 섹션 1: 기업 대출 연체율 ---
if selection == "1. 기업 대출 연체율 분석":
    st.title("📈 기업 대출 연체율 및 금리 시차 분석")
    
    st.subheader("📝 변수별 기초 통계 및 위험도 요약")
    summary_data = {
        "평균": [2.456, 4.272, 4.174, 0.533, 0.331, 3.614, 2.831],
        "표준편차": [1.080, 0.894, 0.839, 0.185, 0.107, 0.871, 0.974],
        "중윗값(IQR)": [1.875, 1.700, 1.520, 0.300, 0.200, 1.180, 1.122],
        "최댓값": [3.500, 5.310, 5.080, 0.900, 0.500, 5.487, 4.020]
    }
    df_summary = pd.DataFrame(summary_data, index=['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '가계연체율', '회사채수익률', 'CD수익률'])
    
    # 레이아웃: 표 1/2(50%), 공백, 그래프 1/4(25%)
    col1, col_space, col2 = st.columns([2, 0.5, 1.5]) 
    
    with col1:
        st.write("### [전체 지표 통계 요약]")
        st.dataframe(df_summary, use_container_width=True) # 화면의 1/2 수준 가독성

    st.divider()
    
    st.subheader("🎯 기업연체율 선행 시차 상관계수")
    lag_corr = pd.DataFrame({
        "상관계수": [1.000, 0.692, 0.640, 0.638, 0.588, -0.350]
    }, index=["기업연체율", "기업대출금리(6M전)", "CD수익률(6M전)", "기업대출금리(5M전)", "CD수익률(5M전)", "회사채수익률(1M전)"])

    col_tbl, col_space2, col_img = st.columns([2, 0.5, 1.5])
    
    with col_tbl:
        st.write("### [선행 시차 상관성 테이블]")
        st.table(lag_corr) # 화면의 1/2 수준
        
    with col_img:
        st.write("### [시차 상관계수 히트맵]")
        fig, ax = plt.subplots(figsize=(4, 6))
        sns.heatmap(lag_corr, annot=True, cmap='coolwarm', fmt=".3f", ax=ax, cbar=False)
        ax.set_title("시차별 상관도", fontsize=10)
        st.pyplot(fig) # 화면의 1/4 수준

# --- 섹션 2: 고객 이탈 분석 ---
elif selection == "2. 신용카드 고객 이탈 분석":
    st.title("💳 신용카드 고객 이탈 패턴 및 세분화")
    
    df_card = get_data('Include/포폴2_Data/credit_card_customer.csv')
    
    if df_card is not None:
        st.subheader("🔍 이탈/유지 집단간 주요 수치 비교")
        comparison = df_card.groupby('Attrition_Flag')[['Total_Trans_Ct', 'Contacts_Count_12_mon', 'Avg_Utilization_Ratio']].mean()
        comparison.index = ['이탈 고객', '유지 고객']
        comparison.columns = ['평균 거래 횟수', '상담 연락 횟수', '평균 한도 소진율']
        
        col_t1, col_space3, col_i1 = st.columns([2, 0.5, 1.5])
        with col_t1:
            st.write("### [집단별 지표 평균 표]")
            st.table(comparison)
        with col_i1:
            st.write("### [이탈여부별 상담횟수]")
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.boxplot(x='Attrition_Flag', y='Contacts_Count_12_mon', data=df_card, ax=ax)
            ax.set_xticklabels(['이탈', '유지'])
            ax.set_xlabel('고객 상태')
            ax.set_ylabel('연락 횟수')
            st.pyplot(fig)

        st.divider()
        st.subheader("📊 의사결정나무 기반 타겟 고객군")
        
        segments = pd.DataFrame({
            "세그먼트 그룹": ["Group A (초고위험)", "Group B (체리피커)", "Group C (이용저조)", "Group D (불만폭발)", "Group E (우량유지)"],
            "고객 수": [998, 35, 2425, 16, 6653],
            "이탈 방어 전략": ["바우처 발송", "미션형 이벤트", "자동이체 유도", "긴급 케어 서비스", "등급 업그레이드"]
        })

        col_t2, col_space4, col_i2 = st.columns([2, 0.5, 1.5])
        with col_t2:
            st.write("### [전략적 세그먼트 분류 데이터]")
            st.dataframe(segments, use_container_width=True, hide_index=True)
        with col_i2:
            st.write("### [세그먼트별 분포]")
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            ax2.pie(segments["고객 수"], labels=segments["세그먼트 그룹"], autopct='%1.1f%%', startangle=90)
            st.pyplot(fig2)

# --- 섹션 3: 이상거래 탐지 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 모델 개선 분석")
    
    col_t3, col_space5, col_i3 = st.columns([2, 0.5, 1.5])
    with col_t3:
        st.write("### [모델 성능 개선 데이터]")
        perf_data = {
            "평가 지표": ["정밀도 (Precision)", "재현율 (Recall)", "F1-Score"],
            "기존 모델": ["9.0%", "82.0%", "0.16"],
            "개선 모델(V20,V21 제거)": ["33.0%", "82.0%", "0.47"]
        }
        st.table(pd.DataFrame(perf_data))
        
        st.write("### [하위 중요도 변수 점수 (제거 대상)]")
        low_importance = pd.DataFrame({
            "변수명": ["V20", "V21", "V22", "V23", "V5"],
            "중요도 점수": [330, 334, 377, 426, 428]
        })
        st.dataframe(low_importance, use_container_width=True, hide_index=True)

    with col_i3:
        st.write("### [핵심 변수 중요도 Top 5]")
        # 가상의 중요도 데이터
        top_f = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig3, ax3 = plt.subplots(figsize=(5, 7))
        top_f.sort_values().plot(kind='barh', ax=ax3, color='royalblue')
        ax3.set_title("변수별 기여도")
        st.pyplot(fig3)
