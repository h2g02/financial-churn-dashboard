import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# --- 1. [안전] 폰트 설정: 외부 URL 다운로드 없이 로컬만 사용 ---
@st.cache_resource
def _init_font():
    """
    메모리 누수 방지를 위해 @st.cache_resource로 단 한 번만 실행.
    외부 URL 다운로드 없이 시스템 폰트 경로만 확인.
    """
    # Ubuntu 시스템 폰트 경로들
    system_font_paths = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/AppleGothic.ttf",
        "c:/Windows/Fonts/malgun.ttf",
    ]
    
    font_family = 'sans-serif'
    for fpath in system_font_paths:
        if os.path.exists(fpath):
            try:
                fm.fontManager.addfont(fpath)
                font_family = fm.FontProperties(fname=fpath).get_name()
                break
            except:
                pass
    
    plt.rcParams['font.family'] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    return font_family

FONT_FAMILY = _init_font()

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="금융 분석 대시보드", layout="wide")

# --- 3. CSS (Streamlit 네이티브 UI의 한글은 브라우저 기본 폰트가 처리) ---
st.markdown("""
<style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 20px;
        border-top: 4px solid #0047AB; }
    .action-step { background-color: #F8F9FA; padding: 15px; border-radius: 8px;
        border-left: 5px solid #0047AB; margin-bottom: 12px; }
    .step-header { font-weight: bold; color: #0047AB; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# --- 4. 사이드바 ---
st.sidebar.title("📁 분석 포트폴리오")
selection = st.sidebar.radio("보고서 선택", [
    "1. 기업 연체율 시차 분석",
    "2. 신용카드 고객 이탈 분석",
    "3. FDS 성능 개선 조치"
])

# --- 5. [성능] 대체 데이터 캐싱 ---
@st.cache_data
def get_summary_p1():
    return pd.DataFrame({
        "항목": ['기준금리','기업대출금리','가계대출금리','기업연체율','회사채수익률','CD수익률'],
        "평균": [2.46, 4.27, 4.17, 0.53, 3.61, 2.83],
        "표준편차": [1.08, 0.89, 0.84, 0.19, 0.87, 0.97],
        "최고치": [3.50, 5.31, 5.08, 0.90, 5.49, 4.02]
    })

@st.cache_data
def get_lag_data():
    return pd.DataFrame({"상관계수": [1.00, 0.69, 0.64, 0.59, -0.35]},
                         index=["기업연체율(T)", "금리(T-6)", "CD(T-6)", "금리(T-5)", "회사채(T-1)"])

@st.cache_data
def get_comp_p2():
    return pd.DataFrame({
        "구분": ["이탈 고객", "유지 고객"],
        "평균 거래 횟수": [44.9, 68.7],
        "평균 상담 횟수": [2.97, 2.35],
        "평균 한도 소진율": ["16.2%", "29.6%"]
    })

@st.cache_data
def get_perf_p3():
    return pd.DataFrame({
        "평가 지표": ["정밀도", "재현율", "F1-Score"],
        "기존 모델": ["9.0%", "82.0%", "0.16"],
        "개선 모델": ["33.0%", "82.0%", "0.47"]
    })

# --- 6. [안전] 히트맵만 st.pyplot 유지 ---
@st.cache_resource
def create_heatmap_fig():
    data = get_lag_data()
    fig, ax = plt.subplots(figsize=(3.5, 4.5))
    sns.heatmap(data, annot=True, cmap='RdYlBu_r', ax=ax, cbar=False,
                annot_kws={"size": 11, "weight": "bold"})
    ax.set_title("시차별 상관계수", fontsize=13, pad=12)
    return fig

# --- 7. 포트폴리오 섹션 ---
if "1." in selection:
    st.title("📈 기업 연체율 및 금리 시차 분석")
    st.markdown("<div class='report-card'><b>핵심 인사이트:</b> 금리 인상은 약 6개월의 시차를 두고 기업 연체율에 가장 강한 영향을 미칩니다.</div>", unsafe_allow_html=True)

    left, mid, right = st.columns([2, 1, 1])

    with left:
        st.subheader("📊 지표별 통계 요약")
        st.table(get_summary_p1())

    with mid:
        st.subheader("🌡️ 시차 상관계수")
        fig = create_heatmap_fig()
        st.pyplot(fig)

    with right:
        st.subheader("💡 분석 결과")
        st.success("기업대출금리와 CD수익률은 약 **6개월의 시차**를 두고 연체율과 0.69의 높은 상관성을 보입니다.")

elif "2." in selection:
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown("<div class='report-card'><b>핵심 인사이트:</b> 거래 55회 미만 & 한도소진율 2.7% 이하 → 이탈률 72%</div>", unsafe_allow_html=True)

    left, mid, right = st.columns([2, 1, 1])

    with left:
        st.subheader("🔍 집단별 행동 비교")
        st.table(get_comp_p2())

    with mid:
        st.subheader("📊 상담 횟수 비교")
        # [네이티브] st.bar_chart로 전환 — 메모리 안전, C 백엔드 미사용
        chart_data = pd.DataFrame({"횟수": [2.35, 2.97]}, index=["유지", "이탈"])
        st.bar_chart(chart_data, use_container_width=True)

    with right:
        st.subheader("📢 마케팅 제언")
        st.warning("상담 횟수 3회 초과 시 이탈 확률이 급증합니다. 해당 고객군에 선제적 케어가 필요합니다.")

else:
    st.title("🛡️ FDS 이상거래 탐지 모델 개선")
    st.markdown("<div class='report-card'><b>핵심 성과:</b> 정밀도를 9% → 33%로 3.6배 개선하여 운영 효율을 극대화했습니다.</div>", unsafe_allow_html=True)

    left, mid, right = st.columns([2, 1, 1])

    with left:
        st.subheader("🚀 모델 성능 지표")
        st.table(get_perf_p3())

    with mid:
        st.subheader("📊 변수 기여도")
        # [네이티브] st.bar_chart로 전환
        top_data = pd.DataFrame({"기여도": [803, 669, 661, 643, 639]},
                                index=["V4", "V27", "V18", "V8", "V1"])
        st.bar_chart(top_data, use_container_width=True)

    with right:
        st.subheader("🛠️ 개선 조치")
        st.markdown("""
            <div class='action-step'><div class='step-header'>1. 변수 제거 (Diet)</div>
            노이즈 변수 5종을 제거하여 모델 정밀도 확보.</div>
            <div class='action-step'><div class='step-header'>2. 데이터 합성 (SMOTE)</div>
            사기 샘플을 인위적으로 생성해 학습 불균형 해소.</div>
            <div class='action-step'><div class='step-header'>3. 임계치 튜닝</div>
            탐지 임계치 0.9로 상향 → 오탐지 대폭 감소.</div>
        """, unsafe_allow_html=True)
