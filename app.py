import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import urllib.request

# --- [필독] 1. 한글 깨짐 방지: 나눔 폰트 다운로드 및 강제 지정 ---
# 이 설정은 어떤 그래프 함수보다도 먼저 실행되어야 합니다.
@st.cache_resource
def setup_korean_font():
    # 나눔 고딕 폰트 다운로드 (환경에 폰트가 없는 경우를 대비)
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # 폰트 매니저에 폰트 등록 및 설정
    fe = fm.FontEntry(fname=font_path, name='NanumGothic')
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = fe.name
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    
    # Seaborn 폰트 설정 강제 동기화
    sns.set(font=fe.name, rc={'axes.unicode_minus': False}, style='whitegrid')

setup_korean_font()

# --- 2. 페이지 및 스타일 설정 ---
st.set_page_config(page_title="Financial Data Insight", layout="wide")

st.markdown("""
    <style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 4px solid #0047AB; }
    .action-step { background-color: #F0F4F8; padding: 15px; border-radius: 10px; border-left: 5px solid #0047AB; margin-bottom: 15px; }
    .step-header { font-weight: bold; color: #0047AB; margin-bottom: 5px; font-size: 1.1em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
st.sidebar.title("📊 분석 포트폴리오")
selection = st.sidebar.radio("리포트 선택", ["1. 기업 연체율 시차 분석", "2. 신용카드 고객 이탈 분석", "3. FDS 성능 개선 조치"])

# --- 섹션 1: 기업 연체율 ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>핵심 인사이트:</b> 금리 인상은 약 6개월의 시차를 두고 기업 연체율에 가장 강한 상관관계(0.69)를 보입니다.</div>", unsafe_allow_html=True)

    # 레이아웃: 표 1/2(2), 그래프 1/4(1), 인사이트 1/4(1)
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("📊 지표별 통계 요약")
        summary_df = pd.DataFrame({
            "항목": ['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '회사채수익률', 'CD수익률'],
            "평균": [2.46, 4.27, 4.17, 0.53, 3.61, 2.83],
            "표준편차": [1.08, 0.89, 0.84, 0.19, 0.87, 0.97],
            "최고치": [3.50, 5.31, 5.08, 0.90, 5.49, 4.02]
        })
        st.table(summary_df)

    with col2:
        st.subheader("🌡️ 시차 상관계수")
        lag_data = pd.DataFrame({"상관계수": [1.00, 0.69, 0.64, 0.59, -0.35]}, 
                                index=["기업연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])
        
        fig, ax = plt.subplots(figsize=(4, 5))
        sns.heatmap(lag_data, annot=True, cmap='RdYlBu_r', ax=ax, cbar=False, 
                    annot_kws={"size": 12, "weight": "bold"})
        ax.set_title("시차 상관분석 (Heatmap)", fontsize=14)
        st.pyplot(fig)

    with col3:
        st.subheader("💡 분석 결과")
        st.success("데이터 분석 결과, 기업 대출 금리는 현재 연체율보다 **6개월 전의 금리**와 가장 밀접하게 연동됩니다.")

# --- 섹션 2: 고객 이탈 ---
elif "2." in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-card'><b>핵심 인사이트:</b> 연간 거래 55회 미만 및 한도 소진율 2.7% 이하 고객은 잠재적 이탈군으로 분류됩니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🔍 주요 집단 행동 비교")
        df_comp = pd.DataFrame({
            "구분": ["이탈 고객 (Attrited)", "유지 고객 (Existing)"],
            "평균 거래 횟수": [44.9, 68.7],
            "평균 상담 횟수": [2.97, 2.35],
            "평균 한도 소진율": ["16.2%", "29.6%"]
        })
        st.table(df_comp)
        st.error("주의: 고객센터 연락 횟수가 4회를 초과하는 시점이 이탈 방어의 마지막 골든타임입니다.")

    with col2:
        st.subheader("📊 상담 횟수 비교")
        fig, ax = plt.subplots(figsize=(5, 8))
        sns.barplot(x=["유지", "이탈"], y=[2.35, 2.97], palette="coolwarm", ax=ax)
        ax.set_title("고객군별 평균 상담 횟수", fontsize=12)
        ax.set_ylabel("횟수")
        st.pyplot(fig)

    with col3:
        st.subheader("📢 마케팅 제언")
        st.warning("이탈 고객은 유지 고객 대비 상담 센터 연락 빈도가 약 26% 높게 나타납니다.")

# --- 섹션 3: FDS 성능 개선 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 모델 개선")
    st.markdown("<div class='report-card'><b>핵심 성과:</b> 피처 다이어트를 통해 정밀도(Precision)를 기존 9%에서 33%로 대폭 향상시켰습니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🚀 모델 성능 지표")
        perf_df = pd.DataFrame({
            "평가 지표": ["정밀도 (Precision)", "재현율 (Recall)", "성과"],
            "기존 모델 (Full)": ["9.0%", "82.0%", "오탐지 과다"],
            "개선 모델 (Diet)": ["33.0%", "82.0%", "효율성 3.6배 증대"]
        })
        st.table(perf_df)

    with col2:
        st.subheader("📊 변수 기여도")
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 8))
        top_v.sort_values().plot(kind='barh', color='#0047AB', ax=ax)
        ax.set_title("핵심 탐지 변수 (Top 5)", fontsize=12)
        st.pyplot(fig)

    with col3:
        st.subheader("🛠️ 개선 조치 요약")
        st.markdown("""
            <div class='action-step'>
                <div class='step-header'>1. 변수 정제 (Diet)</div>
                기여도가 낮은 V20, V21 등 노이즈 변수를 제거함.
            </div>
            <div class='action-step'>
                <div class='step-header'>2. 오버샘플링 (SMOTE)</div>
                사기 데이터(0.17%)를 합성하여 학습 균형을 맞춤.
            </div>
            <div class='action-step'>
                <div class='step-header'>3. 임계치 튜닝</div>
                탐지 임계치를 0.9로 상향하여 오탐지를 최소화함.
            </div>
        """, unsafe_allow_html=True)
