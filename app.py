import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, plot_tree
import scipy.stats as stats

# --- Page Setup ---
st.set_page_config(page_title="Financial Data Analysis Portfolio", layout="wide")

# Sidebar for Navigation
st.sidebar.title("📁 Navigation")
selection = st.sidebar.radio("Go to Project:", [
    "1. Corporate Delinquency Analysis",
    "2. Customer Churn Segmentation",
    "3. Fraud Detection (FDS) Metrics"
])

# --- Project 1: Corporate Delinquency ---
def run_project_1():
    st.title("📈 Corporate Delinquency & Interest Rate Analysis")
    st.markdown("### Lead-Lag Analysis using Macroeconomic Indicators")
    
    # Data Loading (Paths match user's local structure)
    try:
        df_base = pd.read_csv('Include/포폴1_Data/한국은행기준금리.csv')
        df_loan = pd.read_csv('Include/포폴1_Data/예금은행대출금리.csv')
        df_delin = pd.read_csv('Include/포폴1_Data/은행대출금연체율.csv')
        df_market = pd.read_csv('Include/포폴1_Data/회사채_CD수익률.csv')

        # Melting and Cleaning Logic
        def melt_to_long(df, value_name, acc=None, code=None):
            date_cols = [c for c in df.columns if '/' in str(c)]
            mask = pd.Series([True] * len(df))
            if acc: mask &= df['계정항목'].str.strip() == acc
            if code and '구분코드' in df.columns: mask &= df['구분코드'].str.strip() == code
            melted = df[mask][date_cols].melt(var_name='날짜', value_name=value_name)
            melted['날짜'] = pd.to_datetime(melted['날짜'], format='%Y/%m')
            melted[value_name] = pd.to_numeric(melted[value_name], errors='coerce')
            return melted.reset_index(drop=True)

        loan_corp = melt_to_long(df_loan, 'Corp_Loan_Rate', acc='기업대출 2)')
        delin_corp = melt_to_long(df_delin, 'Corp_Delinquency', acc='기업대출', code='은행전체 1)')
        
        # Merged View
        merged = loan_corp.merge(delin_corp, on='날짜').dropna()
        
        st.subheader("Lagged Correlation")
        lags = [1, 3, 6]
        for l in lags:
            merged[f'Loan_Rate_{l}M_Ago'] = merged['Corp_Loan_Rate'].shift(l)
        
        corr_matrix = merged.dropna().corr()
        
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix[['Corp_Delinquency']].sort_values(by='Corp_Delinquency', ascending=False), 
                    annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
        
        st.info("💡 **Insight:** Delinquency reacts most strongly to interest rate changes from 6 months ago.")

    except FileNotFoundError:
        st.error("CSV files not found in the 'Include/포폴1_Data/' directory.")

# --- Project 2: Customer Churn ---
def run_project_2():
    st.title("💳 Credit Card Customer Churn Analysis")
    
    try:
        df_card = pd.read_csv('Include/포폴2_Data/credit_card_customer.csv')
        df_card = df_card.drop(columns=[c for c in df_card.columns if 'Naive_Bayes' in c])
        
        st.subheader("Visualizing Churn Drivers")
        option = st.selectbox("Select Feature to Compare:", 
                              ['Total_Trans_Ct', 'Contacts_Count_12_mon', 'Avg_Utilization_Ratio'])
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(x='Attrition_Flag', y=option, data=df_card, ax=ax)
        st.pyplot(fig)

        st.subheader("Business Rules for Retention")
        st.markdown("""
        Based on Decision Tree analysis, the **High Risk Group** is defined as:
        - **Total Transaction Count** ≤ 54.5
        - **Average Utilization Ratio** ≤ 2.7%
        
        *Action:* Target this group with 'Lock-in' marketing strategies.
        """)
    except FileNotFoundError:
        st.error("CSV file not found in 'Include/포폴2_Data/'.")

# --- Project 3: Fraud Detection ---
def run_project_3():
    st.title("🛡️ Real-time Fraud Detection System (FDS)")
    
    try:
        df_fraud = pd.read_csv('Include/credit_data_small.csv')
        
        st.subheader("Data Imbalance Challenge")
        fraud_counts = df_fraud['Class'].value_counts()
        st.write(f"Normal: {fraud_counts[0]} | Fraud: {fraud_counts[1]}")
        st.warning(f"Fraud Rate is only { (fraud_counts[1]/len(df_fraud))*100 :.3f}%")

        st.subheader("Model Improvement (Feature Selection)")
        st.markdown("""
        **Precision Improvement:**
        - Initial: 9%
        - After dropping low-importance features (V20, V21): **33%**
        - Recall maintained at **82%**.
        """)
        
        # Placeholder for Feature Importance plot
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Precision_and_recall.svg/1200px-Precision_and_recall.svg.png", width=400)
    except FileNotFoundError:
        st.error("CSV file not found in 'Include/포폴3_Data/'.")

# --- Main App Execution ---
if selection == "1. Corporate Delinquency Analysis":
    run_project_1()
elif selection == "2. Customer Churn Segmentation":
    run_project_2()
else:
    run_project_3()
