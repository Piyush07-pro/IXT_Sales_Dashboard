import streamlit as st
import pandas as pd
from databricks import sql
import plotly.express as px

st.set_page_config(page_title="KPI Dashboard", layout="wide")

st.title("📈 Sales KPI Dashboard")

# Databricks connection
connection = sql.connect(
    server_hostname="adb-7405608551394954.14.azuredatabricks.net",
    http_path="/sql/1.0/warehouses/fd7474d77ef7c8a5",
    access_token="dapi895a0e73e16722556bab00071b81aac2-3"
)

query = "SELECT * FROM gold_top_sales"
df = pd.read_sql(query, connection)

# Sidebar filters
st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    df["cat_gorie"].unique(),
    default=df["cat_gorie"].unique()
)

product = st.sidebar.multiselect(
    "Product",
    df["Product"].unique(),
    default=df["Product"].unique()
)

df = df[
    (df["cat_gorie"].isin(category)) &
    (df["Product"].isin(product))
]

# KPI metrics
total_orders = df["total_orders"].sum()
total_revenue = df["total_revenue"].sum()
total_margin = df["total_margin"].sum()
avg_order_value = total_revenue / total_orders

top_product = df.sort_values(
    "total_revenue", ascending=False
).iloc[0]["Product"]

top_category = df.groupby(
    "cat_gorie"
)["total_revenue"].sum().idxmax()

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("Total Orders", int(total_orders))
k2.metric("Total Revenue", f"${total_revenue:,.0f}")
k3.metric("Total Margin", f"${total_margin:,.0f}")
k4.metric("Avg Order Value", f"${avg_order_value:,.2f}")
k5.metric("Top Product", top_product)

# Charts
c1,c2 = st.columns(2)

with c1:
    fig1 = px.bar(
        df.groupby("Product")["total_revenue"].sum().reset_index(),
        x="Product",
        y="total_revenue",
        title="Revenue by Product"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.bar(
        df.groupby("cat_gorie")["total_revenue"].sum().reset_index(),
        x="cat_gorie",
        y="total_revenue",
        title="Revenue by Category"
    )
    st.plotly_chart(fig2, use_container_width=True)
