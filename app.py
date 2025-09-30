
# Streamlit dashboard for Lulu Hypermarket - Sales by Demographics (synthetic dataset)
# Run: streamlit run app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lulu Sales Dashboard", layout="wide")

st.title("Lulu Hypermarket — Sales by Demographics (Synthetic)")
st.markdown("Interactive dashboard showing sales breakdown by demographic filters. Dataset: 50 synthetic transactions.")

@st.cache_data
def load_data(path="lulu_transactions_50rows.csv"):
    return pd.read_csv(path, parse_dates=["Date"])

df = load_data("lulu_transactions_50rows.csv")

# Sidebar filters
st.sidebar.header("Filters")
stores = st.sidebar.multiselect("Store", options=df["Store"].unique(), default=list(df["Store"].unique()))
genders = st.sidebar.multiselect("Gender", options=df["Gender"].unique(), default=list(df["Gender"].unique()))
nationalities = st.sidebar.multiselect("Nationality", options=df["Nationality"].unique(), default=list(df["Nationality"].unique()))
cats = st.sidebar.multiselect("Category", options=df["Category"].unique(), default=list(df["Category"].unique()))
payment = st.sidebar.multiselect("Payment Method", options=df["PaymentMethod"].unique(), default=list(df["PaymentMethod"].unique()))
age_range = st.sidebar.slider("Age range", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

# Apply filters
mask = (
    df["Store"].isin(stores) &
    df["Gender"].isin(genders) &
    df["Nationality"].isin(nationalities) &
    df["Category"].isin(cats) &
    df["PaymentMethod"].isin(payment) &
    df["Age"].between(age_range[0], age_range[1])
)
filtered = df[mask]

st.metric("Total Sales (AED)", f"{filtered['TotalAmount'].sum():.2f}", delta=None)
st.metric("Number of Transactions", len(filtered))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    if filtered.empty:
        st.info("No data for selected filters")
    else:
        sales_cat = filtered.groupby("Category")["TotalAmount"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6,4))
        sales_cat.plot.bar(ax=ax)
        ax.set_ylabel("Sales (AED)")
        ax.set_title("Sales by Category")
        st.pyplot(fig)

with col2:
    st.subheader("Sales by Age Group")
    if filtered.empty:
        st.info("No data for selected filters")
    else:
        bins = [15,25,35,45,55,100]
        labels = ["16-24","25-34","35-44","45-54","55+"]
        filtered["AgeGroup"] = pd.cut(filtered["Age"], bins=bins, labels=labels, right=False)
        sales_age = filtered.groupby("AgeGroup")["TotalAmount"].sum().reindex(labels).fillna(0)
        fig2, ax2 = plt.subplots(figsize=(6,4))
        sales_age.plot.bar(ax=ax2)
        ax2.set_ylabel("Sales (AED)")
        ax2.set_title("Sales by Age Group")
        st.pyplot(fig2)

st.subheader("Raw data (filtered)")
st.dataframe(filtered.reset_index(drop=True))

st.markdown('---')
st.caption('This dashboard and dataset are synthetic for demonstration purposes.')
