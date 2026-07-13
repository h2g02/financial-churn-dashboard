import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import urllib.request

# --- [점검] 1. 한글 깨짐 방지: 나눔 폰트 다운로드 및 글로벌 설정 ---
# @st.cache_resource
def setup_full_korean_env():
    # 1. Seaborn 테마 설정을 가장 먼저 수행 (폰트 설정을 덮어쓰지 않도록 함)
    sns.set_theme(style='whitegrid')
    
    # 2. 나눔 고딕 폰트 다운로드 (안전한 파일명 설정)
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
    
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # 3. 폰트 매니저에 안전하게 폰트 파일 경로 등록 (insert 대신 addfont 사용)
    fm.fontManager.addfont(font_path)
    
    # 4. 글로벌 rcParams 설정 (addfont로 등록했기 때문에 이름만 지정하면 됩니다)
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False
    
    # 5. 개별 위젯용 FontProperties 객체 생성 (축 라벨 강제 적용용)
    return fm.FontProperties(fname=font_path)

# 폰트 속성 객체 획득
nanum_prop = setup_full_korean_env()

# --- 2. 페이지 레이아웃 설정 ---
st.set_page_config(page_title="금융 데이터 리포트", layout="wide")

# CSS 스타일링 (예술성 보강)
st.markdown("""
    <style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 4px solid #0047AB; }
    .action-step { background-color: #F8F9FA; padding: 15px; border-radius: 8px; border-left: 5px solid #0047AB; margin-bottom: 12px; }
    .step-header { font-weight: bold; color: #0047AB; margin-bottom: 3px; font-size: 1.05em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
st.sidebar.title("📁 분석 포트폴리오")
selection = st.sidebar.radio("보고서 선택", ["1. 기업 연체율 시차 분석", "2. 신용카드 고객 이탈 분석", "3. FDS 성능 개선 조치"])

# --- 섹션 1: 기업 연체율 ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>분석 요약:</b> 금리 지표가 기업 부실에 미치는 영향을 시차별로 정량화하여 리스크 관리의 근거를 제시합니다.</div>", unsafe_allow_html=True)

    # 레이아웃 비율: 표 1/2(2), 그래프 1/4(1), 인사이트 1/4(1)
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
        # 히트맵 그리기
        sns.heatmap(lag_data, annot=True, cmap='RdYlBu_r', ax=ax, cbar=False, 
                    annot_kws={"size": 11, "weight": "bold"})
        
        # [강제 적용] 축 라벨 및 제목 폰트 수동 지정
        ax.set_title("시차별 상관계수", fontproperties=nanum_prop, fontsize=14, pad=15)
        ax.set_ylabel("분석 지표 (Time-Lag)", fontproperties=nanum_prop, fontsize=12)
        plt.setp(ax.get_yticklabels(), fontproperties=nanum_prop) # y축 항목 강제 적용
        
        st.pyplot(fig)

    with col3:
        st.subheader("💡 분석 결과")
        st.success("기업대출금리는 약 **6개월의 시차**를 두고 연체율과 가장 높은 상관관계를 형성합니다.")

# --- 섹션 2: 고객 이탈 ---
elif "2." in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-card'><b>분석 요약:</b> 이탈 고객(Attrited)과 유지 고객의 활동성 지표를 대조하여 이탈 징후를 식별합니다.</div>", unsafe_allow_html=True)

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

    with col2:
        st.subheader("📊 상담 횟수 비교")
        fig, ax = plt.subplots(figsize=(5, 8))
        sns.barplot(x=["유지", "이탈"], y=[2.35, 2.97], palette="coolwarm", ax=ax)
        
        # [강제 적용] 축 라벨 및 제목 폰트 수동 지정
        ax.set_title("집단별 평균 연락 횟수", fontproperties=nanum_prop, fontsize=12)
        ax.set_xlabel("고객 집단", fontproperties=nanum_prop)
        ax.set_ylabel("평균 연락 건수", fontproperties=nanum_prop)
        plt.setp(ax.get_xticklabels(), fontproperties=nanum_prop) # x축 항목 강제 적용
        
        st.pyplot(fig)

    with col3:
        st.subheader("📢 마케팅 제언")
        st.warning("상담 횟수가 3회를 초과하는 고객군은 불만이 누적된 상태이므로 즉각적인 케어가 필요합니다.")

# --- 섹션 3: FDS 개선 ---
else:
    st.title("🛡️ FDS 이상거래 탐지 모델 개선")
    st.markdown("<div class='report-card'><b>분석 요약:</b> 정밀도(Precision)를 개선하여 보안 관제 효율을 약 3.6배 높인 성과 요약입니다.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("🚀 모델 성능 지표")
        perf_df = pd.DataFrame({
            "평가 지표": ["정밀도 (Precision)", "재현율 (Recall)", "F1-Score"],
            "기존 모델": ["9.0%", "82.0%", "0.16"],
            "개선 모델": ["33.0%", "82.0%", "0.47"]
        })
        st.table(perf_df)

    with col2:
        st.subheader("📊 변수 기여도")
        top_v = pd.Series([803, 669, 661, 643, 639], index=["V4", "V27", "V18", "V8", "V1"])
        fig, ax = plt.subplots(figsize=(5, 8))
        top_v.sort_values().plot(kind='barh', color='#0047AB', ax=ax)
        
        # [강제 적용] 축 라벨 및 제목 폰트 수동 지정
        ax.set_title("핵심 탐지 변수 Top 5", fontproperties=nanum_prop, fontsize=12)
        ax.set_xlabel("중요도 점수", fontproperties=nanum_prop)
        ax.set_ylabel("PCA 변수명", fontproperties=nanum_prop)
        
        st.pyplot(fig)

    with col3:
        st.subheader("🛠️ 개선 조치 요약")
        st.markdown("""
            <div class='action-step'>
                <div class='step-header'>1. 변수 제거 (Feature Selection)</div>
                노이즈를 유발하는 하위 5개 변수를 제거함.
            </div>
            <div class='action-step'>
                <div class='step-header'>2. 데이터 합성 (SMOTE)</div>
                사기 거래 샘플을 인위적으로 생성해 학습 불균형 해소.
            </div>
            <div class='action-step'>
                <div class='step-header'>3. 임계치 최적화</div>
                탐지 임계치를 0.9로 설정하여 오탐지 대폭 절감.
            </div>
        """, unsafe_allow_html=True)
