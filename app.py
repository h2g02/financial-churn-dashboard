import streamlit as st
import pandas as pd
import numpy as np

# --- 1. 페이지 레이아웃 설정 (최상단 유지) ---
st.set_page_config(page_title="금융 데이터 리포트", layout="wide")

# CSS 스타일링 (대시보드 예술성 유지)
st.markdown("""
    <style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 4px solid #0047AB; }
    .action-step { background-color: #F8F9FA; padding: 15px; border-radius: 8px; border-left: 5px solid #0047AB; margin-bottom: 12px; }
    .step-header { font-weight: bold; color: #0047AB; margin-bottom: 3px; font-size: 1.05em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 사이드바 구성 ---
st.sidebar.title("📁 분석 포트폴리오")
selection = st.sidebar.radio("보고서 선택", ["1. 기업 연체율 시차 분석", "2. 신용카드 고객 이탈 분석", "3. FDS 성능 개선 조치"])

# --- 섹션 1: 기업 연체율 ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>분석 요약:</b> 금리 지표가 기업 부실에 미치는 영향을 시차별로 정량화하여 리스크 관리의 근거를 제시합니다.</div>", unsafe_allow_html=True)

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
        # 데이터프레임 구조 생성
        lag_data = pd.DataFrame({
            "상관계수": [1.00, 0.69, 0.64, 0.59, -0.35]
        }, index=["기업연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])
        
        # 안전한 내장 차트로 시각화
        st.bar_chart(lag_data, color="#0047AB")

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
        chart_data = pd.DataFrame({
            "평균 연락 건수": [2.35, 2.97]
        }, index=["유지", "이탈"])
        
        st.bar_chart(chart_data, color="#0047AB")

    with col3:
        st.subheader("📢 마케팅 제언")
        st.success("상담 횟수가 3회를 초과하는 고객군은 불만이 누적된 상태이므로 즉각적인 케어가 필요합니다.")

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
        top_v = pd.DataFrame({
            "중요도 점수": [639, 643, 661, 669, 803]
        }, index=["V1", "V8", "V18", "V27", "V4"])
        
        st.bar_chart(top_v, color="#0047AB")

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
