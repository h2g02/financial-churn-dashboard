import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from matplotlib import font_manager, rc

# --- 1. 한글 폰트 문제 완전 해결 (시스템 내 가용한 폰트 검색) ---
@st.cache_resource
def init_korean_font():
    # 운영체제별 폰트 후보군
    font_candidates = [
        "Malgun Gothic", "AppleGothic", "NanumGothic", 
        "Gulim", "Dotum", "Noto Sans CJK KR"
    ]
    
    found = False
    for font_name in font_candidates:
        # 시스템에 해당 폰트가 있는지 확인
        if font_name in [f.name for f in font_manager.fontManager.ttflist]:
            rc('font', family=font_name)
            found = True
            break
            
    if not found:
        # 리눅스/서버 환경을 위해 범용 폰트 설정
        rc('font', family='sans-serif')
        
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
    # Seaborn 테마 설정 (한글 폰트 강제 주입)
    sns.set(font=plt.rcParams['font.family'], rc={'axes.unicode_minus': False}, style='whitegrid')

init_korean_font()

# --- 페이지 설정 ---
st.set_page_config(page_title="금융 데이터 리포트", layout="wide")

# 사이드바 설정
st.sidebar.header("📁 분석 메뉴")
selection = st.sidebar.radio("원하는 보고서를 선택하세요", [
    "1. 기업 연체율 시차 분석",
    "2. 카드 고객 이탈 분석",
    "3. FDS 모델 개선 결과"
])

# 데이터 로드 함수
def load_data(path):
    try:
        return pd.read_csv(path)
    except:
        return None

# --- 섹션 1: 기업 대출 연체율 ---
if selection == "1. 기업 연체율 시차 분석":
    st.title("📈 기업 대출 연체율 및 금리 시차 분석")
    st.markdown("---")

    # [가독성 테이블 데이터]
    summary_data = {
        "항목": ['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '가계연체율', '회사채수익률', 'CD수익률'],
        "평균": [2.46, 4.27, 4.17, 0.53, 0.33, 3.61, 2.83],
        "표준편차": [1.08, 0.89, 0.84, 0.19, 0.11, 0.87, 0.97],
        "최댓값": [3.50, 5.31, 5.08, 0.90, 0.50, 5.49, 4.02]
    }
    df_sum = pd.DataFrame(summary_data)

    # 레이아웃 구성: 표 2(50%), 그래프 1(25%), 여백 1(25%)
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("📊 변수별 통계 요약")
        st.table(df_sum) # 고정형 표로 가독성 확보

    with col2:
        st.subheader("🌡️ 상관계수")
        lag_data = pd.DataFrame({
            "상관도": [1.00, 0.69, 0.64, 0.59, -0.35]
        }, index=["기업연체율", "금리(6M전)", "CD(6M전)", "금리(5M전)", "회사채(1M)"])
        
        fig, ax = plt.subplots(figsize=(4, 5))
        sns.heatmap(lag_data, annot=True, cmap='RdYlBu_r', ax=ax, cbar=False)
        plt.title("시차별 상관성")
        st.pyplot(fig)

# --- 섹션 2: 고객 이탈 분석 ---
elif selection == "2. 카드 고객 이탈 분석":
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("---")

    df_card = load_data('Include/포폴2_Data/credit_card_customer.csv')
    
    # [집단 비교 테이블]
    comparison_data = {
        "집단": ["이탈 고객 (Attrited)", "유지 고객 (Existing)"],
        "평균 거래 횟수": [44.9, 68.7],
        "평균 연락 횟수": [2.97, 2.35],
        "평균 한도 소진율": ["16.2%", "29.6%"]
    }
    df_comp = pd.DataFrame(comparison_data)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🔍 주요 지표 비교")
        st.table(df_comp)
        
        st.subheader("📌 핵심 이탈 규칙 (Decision Tree)")
        st.info("거래 횟수 55회 미만이면서 한도 소진율이 2.7% 이하인 경우 이탈 확률 72%")

    with col2:
        st.subheader("📉 연락 횟수 분포")
        if df_card is not None:
            fig, ax = plt.subplots(figsize=(5, 6))
            sns.boxplot(x='Attrition_Flag', y='Contacts_Count_12_mon', data=df_card, ax=ax)
            ax.set_title("이탈 여부별 고객센터 연락")
            st.pyplot(fig)
        else:
            st.write("차트용 데이터가 없습니다.")

# --- 섹션 3: 이상거래 탐지 ---
else:
    st.title("🛡️ 이상거래 탐지(FDS) 성능 개선")
    st.markdown("---")

    # [성능 개선 테이블]
    perf_data = {
        "모델 구분": ["개선 전 (전체 변수)", "개선 후 (변수 제거)"],
        "정밀도 (Precision)": ["9.0%", "33.0%"],
        "재현율 (Recall)": ["82.0%", "82.0%"],
        "성과": ["오탐지 과다", "정밀도 3.6배 향상"]
    }
    df_perf = pd.DataFrame(perf_data)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🚀 모델 성능 지표")
        st.table(df_perf)
        
        st.subheader("🗑️ 제거된 하위 변수")
        st.write("V20, V21, V22, V23, V5 (노이즈 제거)")

    with col2:
        st.subheader("📊 변수 기여도 (Top 5)")
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 7))
        top_v.sort_values().plot(kind='barh', color='seagreen', ax=ax)
        ax.set_title("모델 중요도")
        st.pyplot(fig)
