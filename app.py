import streamlit as st
import pandas as pd
from databricks import sql
import plotly.express as px

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")
st.title("📊 Sales Analytics Dashboard")

try:
    # Databricks connection
    connection = sql.connect(
        server_hostname="adb-7405608551394954.14.azuredatabricks.net",
        http_path="/sql/1.0/warehouses/fd7474d77ef7c8a5",
        access_token="dapia0d4e295e3605b1be5790cb4949e4fc5-3"
    )

    query = "SELECT * FROM gold_top_sales"
    df = pd.read_sql(query, connection)

    if df.empty:
        st.warning("No data found in Gold table")
    else:
        # Derived metrics
        df["margin_percent"] = df["total_margin"] / df["total_revenue"] * 100
        avg_order_value = df["total_revenue"].sum() / df["total_orders"].sum()
        top_product = df.sort_values("total_revenue", ascending=False).iloc[0]["Product"]
        top_category = df.groupby("cat_gorie")["total_revenue"].sum().idxmax()

        # KPI row
        st.subheader("Key Performance Indicators")
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
        kpi1.metric("Total Orders", int(df["total_orders"].sum()))
        kpi2.metric("Total Revenue", f"${df['total_revenue'].sum():,.0f}")
        kpi3.metric("Total Margin", f"${df['total_margin'].sum():,.0f}")
        kpi4.metric("Avg Order Value", f"${avg_order_value:,.2f}")
        kpi5.metric("Top Product", top_product)
        kpi6.metric("Top Category", top_category)

        # Optional: filter by category
        category_filter = st.selectbox("Filter by Category", options=["All"] + df["cat_gorie"].unique().tolist())
        filtered_df = df if category_filter == "All" else df[df["cat_gorie"] == category_filter]

        # Charts row
        st.subheader("Sales Visualizations")
        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.bar(
                filtered_df.sort_values("total_revenue", ascending=False),
                x="Product", y="total_revenue",
                title="Top Products by Revenue",
                text="total_revenue"
            )
            fig1.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.bar(
                filtered_df.groupby("cat_gorie")["total_revenue"].sum().reset_index(),
                x="cat_gorie", y="total_revenue",
                title="Revenue by Category",
                text="total_revenue"
            )
            fig2.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            st.plotly_chart(fig2, use_container_width=True)

        # Pie chart for revenue share
        st.subheader("Revenue Distribution by Product")
        fig3 = px.pie(
            filtered_df,
            names="Product",
            values="total_revenue",
            title="Revenue Share"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Show detailed data
        st.subheader("Detailed Data")
        st.dataframe(filtered_df)

except Exception as e:
    st.error(e)
