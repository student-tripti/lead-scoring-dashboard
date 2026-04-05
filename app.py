import streamlit as st
import pandas as pd

# Title
st.title("🚀 Lead Scoring Dashboard")

# File Upload
file = st.file_uploader("Upload CSV")

# Score function
def score_lead(row):
    return (
        0.4 * row['engagement'] +
        0.3 * row['website_activity'] +
        0.2 * row['company_size'] +
        0.1 * row['industry_score']
    )

# Category function
def label_score(score):
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


if file:
    df = pd.read_csv(file)

    # Clean data 
    df = df.fillna("")

    numeric_cols = ['engagement', 'website_activity', 'company_size', 'industry_score']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Score calculation
    df['score'] = df.apply(score_lead, axis=1) * 100

    # Sorting
    df = df.sort_values(by='score', ascending=False)

    # Category column
    df['category'] = df['score'].apply(label_score)

    # 📊 Metrics
    st.subheader("📊 Summary")
    col1, col2 = st.columns(2)
    col1.metric("Top Score", int(df['score'].max()))
    col2.metric("Average Score", int(df['score'].mean()))

    # 🌍 Region Filter 
    if 'region' in df.columns:
        st.subheader("🌍 Filter by Region")
        region = st.selectbox("Select Region", ["All"] + list(df['region'].unique()))

        filtered_df = df.copy()

        if region != "All":
            filtered_df = filtered_df[filtered_df['region'] == region]
    else:
        filtered_df = df.copy()

    # 🏆 Best Lead
    st.subheader("🏆 Best Lead")
    st.write(filtered_df.iloc[0])

    # 📋 Data Table (safe display)
    st.subheader("📋 Lead Data")
    st.write(filtered_df)

    # 📈 Chart
    st.subheader("📈 Score Distribution")
    st.bar_chart(filtered_df['score'])

    # 📥 Download
    st.download_button(
        "Download Filtered Data",
        filtered_df.to_csv(index=False),
        file_name="filtered_leads.csv"
    )

    # 📌 Insights
    st.subheader("📌 Insights")
    st.write("• High scoring leads have higher engagement")
    st.write("• High-value leads are concentrated in specific regions")
    st.write("• Engagement contributes the most (40%)")