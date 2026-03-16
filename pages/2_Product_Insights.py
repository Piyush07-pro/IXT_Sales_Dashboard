import streamlit as st
import pandas as pd
from databricks import sql
import plotly.express as px

st.set_page_config(page_title="Product Insights", layout="wide")

st.title("📦 Product Insights")

# Databricks connection
connection = sql.connect(
    server_hostname="adb-7405608551394954.14.azuredatabricks.net",
    http_path="/sql/1.0/warehouses/fd7474d77ef7c8a5",
    access_token="dapi895a0e73e16722556bab00071b81aac2-3"
)

query = "SELECT * FROM gold_top_sales"
df = pd.read_sql(query, connection)

# Category filter
category = st.sidebar.selectbox(
    "Category",
    ["All"] + df["cat_gorie"].unique().tolist()
)

if category != "All":
    df = df[df["cat_gorie"] == category]

# Top product chart
fig1 = px.bar(
    df.sort_values("total_revenue", ascending=False),
    x="Product",
    y="total_revenue",
    title="Top Products by Revenue",
    text="total_revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# Revenue vs margin chart
fig2 = px.scatter(
    df,
    x="total_revenue",
    y="total_margin",
    size="total_orders",
    color="cat_gorie",
    hover_name="Product",
    title="Revenue vs Margin"
)

st.plotly_chart(fig2, use_container_width=True)

# Revenue distribution
fig3 = px.pie(
    df,
    names="Product",
    values="total_revenue",
    title="Revenue Share"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Detailed Data")

st.dataframe(df)
