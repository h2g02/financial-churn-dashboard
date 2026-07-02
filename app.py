import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# --- 1. [점검] 한글 폰트 설정 (사용자 제공 코드 최우선 적용) ---
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False
# Seaborn에도 폰트 적용
sns.set(font=plt.rcParams['font.family'], style="whitegrid")

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="금융 데이터 분석 포트폴리오", layout="wide")

# 가독성을 위한 카드 스타일 CSS
st.markdown("""
    <style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 4px solid #0047AB; }
    .action-step { background-color: #F0F4F8; padding: 15px; border-radius: 10px; border-left: 5px solid #0047AB; margin-bottom: 10px; }
    .step-header { font-weight: bold; color: #0047AB; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 내비게이션 ---
st.sidebar.title("📁 분석 리포트")
selection = st.sidebar.radio("보고서 유형", ["1. 기업 연체율 시차 분석", "2. 신용카드 고객 이탈 분석", "3. FDS 성능 개선 조치"])

# 데이터 로드 함수
@st.cache_data
def load_csv(path):
    try: return pd.read_csv(path)
    except: return None

# --- 섹션 1: 기업 연체율 (에러 수정 완료) ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 금리 인상이 실제 기업 부실로 이어지는 시차(Time-Lag)를 분석합니다.</div>", unsafe_allow_html=True)

    # 데이터 요약 (노트북 수치 반영)
    summary_df = pd.DataFrame({
        "항목": ['기준금리', '기업대출금리', '가계대출금리', '기업연체율', '가계연체율', '회사채수익률', 'CD수익률'],
        "평균(Mean)": [2.46, 4.27, 4.17, 0.53, 0.33, 3.61, 2.83],
        "표준편차(Std)": [1.08, 0.89, 0.84, 0.19, 0.11, 0.87, 0.97],
        "최고치(Max)": [3.50, 5.31, 5.08, 0.90, 0.50, 5.49, 4.02]
    })

    # 레이아웃: 표 1/2(2/4), 그래프 1/4(1/4), 인사이트 1/4(1/4)
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("📊 지표별 통계 요약")
        st.table(summary_df) # 화면의 50% 차지

    with col2:
        st.subheader("🌡️ 상관계수")
        lag_data = pd.DataFrame({"상관계수": [1.0, 0.69, 0.64, 0.59, -0.35]}, 
                                index=["기업연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])
        # 그래프 디자인 수정
        fig, ax = plt.subplots(figsize=(4, 6))
        sns.heatmap(lag_data, annot=True, cmap='RdYlBu_r', ax=ax, cbar=False, linewidths=1, annot_kws={"weight": "bold"})
        ax.set_title("시차별 상관관계")
        st.pyplot(fig) # 화면의 25% 차지

    with col3:
        st.subheader("💡 분석 결과")
        st.info("금리 인상 후 약 **6개월의 시차**를 두고 기업 연체율이 가장 민감하게 반응함이 확인되었습니다.")

# --- 섹션 2: 고객 이탈 분석 ---
elif "2." in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 거래 빈도와 상담 연락 패턴을 분석하여 이탈 징후를 사전 포착합니다.</div>", unsafe_allow_html=True)

    df_comp = pd.DataFrame({
        "구분": ["이탈 고객 (Attrited)", "유지 고객 (Existing)"],
        "평균 거래 횟수": [44.9, 68.7],
        "평균 상담 횟수": [2.97, 2.35],
        "평균 한도 소진율": ["16.2%", "29.6%"]
    })

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🔍 집단 행동 비교")
        st.table(df_comp)
        st.error("**핵심 규칙:** 거래 55회 미만 & 이용률 2.7% 이하 → 이탈률 72%")

    with col2:
        st.subheader("📊 상담 횟수 분포")
        fig, ax = plt.subplots(figsize=(5, 8))
        sns.barplot(x=["유지", "이탈"], y=[2.35, 2.97], palette="coolwarm", ax=ax)
        ax.set_title("평균 상담 연락 횟수")
        ax.set_xlabel("고객 구분")
        ax.set_ylabel("상담 횟수")
        st.pyplot(fig)

    with col3:
        st.subheader("📢 마케팅 제언")
        st.warning("상담 연락이 **4회 이상**인 고객은 이탈 임계치에 도달한 것으로 판단됩니다.")

# --- 섹션 3: FDS 개선 조치 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 모델 개선")
    st.markdown("<div class='report-card'><b>보고서 개요:</b> 노이즈 제거와 샘플링을 통해 정밀도를 3.6배 향상시킨 개선 조치 리포트입니다.</div>", unsafe_allow_html=True)

    perf_df = pd.DataFrame({
        "평가 지표": ["정밀도 (Precision)", "재현율 (Recall)", "오탐지 개선"],
        "기존 모델": ["9.0%", "82.0%", "-"],
        "개선 모델": ["33.0%", "82.0%", "3.6배 향상"]
    })

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🚀 성능 개선 지표")
        st.table(perf_df)

    with col2:
        st.subheader("📊 변수 기여도")
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 8))
        top_v.sort_values().plot(kind='barh', color='#0047AB', ax=ax)
        ax.set_title("모델 중요 변수 Top 5")
        st.pyplot(fig)

    with col3:
        st.subheader("🛠️ 3단계 개선 조치")
        st.markdown("""
            <div class='action-step'>
                <div class='step-header'>Step 1. 변수 제거</div>
                V20, V21 등 노이즈 변수 제거로 정밀도 확보.
            </div>
            <div class='action-step'>
                <div class='step-header'>Step 2. 불균형 보정</div>
                SMOTE 기법을 통한 사기 데이터 합성 및 학습.
            </div>
            <div class='action-step'>
                <div class='step-header'>Step 3. 임계치 튜닝</div>
                탐지 임계치 0.9 상향으로 오탐지율 획기적 개선.
            </div>
        """, unsafe_allow_html=True)
