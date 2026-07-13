import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_portfolio2_data():
    try:
        return pd.read_csv("Include/포폴2_Data/credit_card_customer.csv")
    except FileNotFoundError:
        return None

def portfolio2_report():
    st.title("💳 신용카드 고객 이탈 패턴 분석")
    st.markdown(
        "<div class='report-card'>"
        "<b>핵심 인사이트:</b> 거래 55회 미만 & 한도소진율 2.7% 이하 "
        "→ 이탈률 72% (초고위험군)"
        "</div>",
        unsafe_allow_html=True,
    )

    df = load_portfolio2_data()

    # --- Comparison Table ---
    st.subheader("🔍 이탈 고객 vs 유지 고객 비교")

    if df is not None and "churn_status" in df.columns:
        comp = df.groupby("churn_status").agg(
            avg_utilization=("utilization_ratio", "mean"),
            avg_late_payments=("late_payment_count", "mean"),
            avg_support_calls=("support_calls", "mean"),
            customer_count=("customer_id", "count"),
        ).reset_index()
        comp["churn_status"] = comp["churn_status"].map({0: "유지", 1: "이탈"})
        st.table(comp)
    else:
        st.table(
            pd.DataFrame({
                "구분": ["이탈 고객", "유지 고객"],
                "평균 거래 횟수": [44.9, 68.7],
                "평균 상담 횟수": [2.97, 2.35],
                "평균 한도 소진율": ["16.2%", "29.6%"],
            })
        )

    # --- Bar Charts (네이티브) ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📊 카드 등급별 이탈률")
        churn_rate = pd.DataFrame(
            {"이탈률 (%)": [16.1, 11.3, 18.9, 14.2]},
            index=["Blue", "Silver", "Gold", "Platinum"],
        )
        st.bar_chart(churn_rate, use_container_width=True)

    with chart_col2:
        st.subheader("📊 소득 구간별 이탈률")
        income_churn = pd.DataFrame(
            {"이탈률 (%)": [21.0, 15.3, 11.8, 9.5]},
            index=["<$40K", "$40K-$60K", "$60K-$80K", ">$80K"],
        )
        st.bar_chart(income_churn, use_container_width=True)

    # --- Business Rules ---
    st.subheader("⚙️ 이탈 방지 비즈니스 룰")

    rule1, rule2, rule3 = st.columns(3)
    with rule1:
        st.metric("Rule 1: 한도 소진율 > 80%", "2,341", delta="23% of base")
    with rule2:
        st.metric("Rule 2: 연체 횟수 > 2회", "1,156", delta="11% of base")
    with rule3:
        st.metric("Rule 3: 상담 > 5회", "487", delta="4.8% of base")

    st.info(
        "📢 **마케팅 제언:** 상담 횟수 3회 초과 시 이탈 확률이 급증하므로 "
        "해당 고객군에 선제적 케어가 필요합니다."
    )
