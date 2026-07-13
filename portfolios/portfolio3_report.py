import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_portfolio3_data():
    try:
        return pd.read_csv("Include/포폴3_Data/credit_card_small.csv")
    except FileNotFoundError:
        return None

def portfolio3_report():
    st.title("🛡️ FDS 이상거래 탐지 모델 개선")
    st.markdown(
        "<div class='report-card'>"
        "<b>핵심 성과:</b> 정밀도를 9% → 33%로 3.6배 개선하여 운영 효율을 극대화했습니다."
        "</div>",
        unsafe_allow_html=True,
    )

    df = load_portfolio3_data()

    # --- Performance Table ---
    st.subheader("🚀 모델 성능 비교")

    left, right = st.columns([3, 2])

    with left:
        if df is not None and "f1_score" in df.columns:
            perf = df.sort_values("f1_score", ascending=False)[
                ["model_name", "accuracy", "precision", "recall", "f1_score", "auc_roc"]
            ].copy()
            for col in ["accuracy", "precision", "recall", "f1_score", "auc_roc"]:
                perf[col] = (perf[col] * 100).round(1).astype(str) + "%"
            st.dataframe(perf, use_container_width=True, hide_index=True)
        else:
            st.table(
                pd.DataFrame({
                    "모델": ["LightGBM (개선)", "LightGBM (기존)", "XGBoost", "RandomForest"],
                    "정밀도": ["33.0%", "9.0%", "21.5%", "18.2%"],
                    "재현율": ["82.0%", "82.0%", "79.3%", "74.1%"],
                    "F1-Score": ["47.0%", "16.2%", "33.8%", "29.2%"],
                })
            )

    # --- Feature Importance (네이티브) ---
    with right:
        st.subheader("📊 변수 기여도 (Top 5)")
        feature_imp = pd.DataFrame(
            {"기여도 점수": [803, 669, 661, 643, 639]},
            index=["V4", "V27", "V18", "V8", "V1"],
        )
        st.bar_chart(feature_imp, use_container_width=True)

    # --- Action Steps ---
    st.subheader("🛠️ 3단계 개선 조치")
    st.markdown(
        """
        <div class='action-step'>
            <div class='step-header'>Step 1. 변수 제거 (Feature Diet)</div>
            중요도가 낮은 V20, V21 등 노이즈 변수를 제거하여 모델 정밀도를 확보하였습니다.
        </div>
        <div class='action-step'>
            <div class='step-header'>Step 2. 데이터 불균형 해소 (SMOTE)</div>
            0.17%에 불과한 사기 거래 샘플을 합성하여 정상:사기 = 1:1 비율로 학습시켰습니다.
        </div>
        <div class='action-step'>
            <div class='step-header'>Step 3. 임계치 튜닝 (Threshold)</div>
            탐지 임계치를 0.9로 상향 조정하여 오탐지율을 대폭 감소시켰습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- KPI 요약 ---
    st.subheader("📋 최종 성능 지표")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Best Model", "LightGBM", "Diet")
    kpi2.metric("F1-Score", "47.0%", "+30.8pp")
    kpi3.metric("AUC-ROC", "94.6%", "")
    kpi4.metric("Precision", "33.0%", "+24.0pp")
    kpi5.metric("False Alarm ↓", "1/3.6x", "-72%")
