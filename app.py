import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

st.set_page_config(
    page_title="Medallion Data Warehouse Dashboard",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

SERVER = "localhost\\SQLEXPRESS"
DATABASE = "DataWarehouse"
DRIVER = "ODBC Driver 17 for SQL Server"

def get_engine():
    conn_str = (
        f"mssql+pyodbc://@{SERVER}/{DATABASE}"
        f"?driver={quote_plus(DRIVER)}"
        f"&trusted_connection=yes"
    )
    return create_engine(conn_str, fast_executemany=True)

@st.cache_data(ttl=300)
def run_query(query):
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

@st.cache_data(ttl=300)
def load_data():
    bronze_cust = run_query("SELECT TOP 20 * FROM bronze.crm_cust_info")
    bronze_prd = run_query("SELECT TOP 20 * FROM bronze.crm_prd_info")
    bronze_sales = run_query("SELECT TOP 20 * FROM bronze.crm_sales_details")

    silver_cust = run_query("SELECT TOP 20 * FROM silver.crm_cust_info")
    silver_prd = run_query("SELECT TOP 20 * FROM silver.crm_prd_info")
    silver_sales = run_query("SELECT TOP 20 * FROM silver.crm_sales_details")

    gold_customers = run_query("SELECT TOP 20 * FROM gold.dim_customers")
    gold_products = run_query("SELECT TOP 20 * FROM gold.dim_products")
    gold_sales = run_query("SELECT TOP 20 * FROM gold.fact_sales")

    return (
        bronze_cust, bronze_prd, bronze_sales,
        silver_cust, silver_prd, silver_sales,
        gold_customers, gold_products, gold_sales
    )

(
    bronze_cust, bronze_prd, bronze_sales,
    silver_cust, silver_prd, silver_sales,
    gold_customers, gold_products, gold_sales
) = load_data()

st.markdown("""
//fonts.googleapis.com">
//fonts.gstatic.com" crossorigin>
//fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root{
    --bg:#0C1519;
    --sidebar:#162127;
    --card:#3A3534;
    --accent:#724B39;
    --highlight:#CF9D7B;
    --text:#F5EDE6;
    --text-soft:#E4D4C7;
    --border:rgba(207,157,123,0.22);
}

.stApp {
    background: linear-gradient(180deg, #0C1519 0%, #162127 100%);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

section[data-testid="stSidebar"] {
    background: var(--sidebar) !important;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1320px;
}

h1, h2, h3, h4, h5 {
    color: var(--highlight) !important;
    font-family: 'Cormorant Garamond', serif !important;
    letter-spacing: 0.4px;
}

p, label, div, span {
    font-family: 'Inter', sans-serif;
}

.hero {
    background: rgba(58, 53, 52, 0.78);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.28);
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
}

.hero h1 {
    color: var(--highlight) !important;
    margin-bottom: 10px;
}

.hero p {
    color: var(--text-soft) !important;
    font-size: 1.05rem;
}

div[data-testid="metric-container"] {
    background: rgba(58, 53, 52, 0.82) !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px !important;
    padding: 14px !important;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
}

div[data-testid="metric-container"] * {
    color: var(--text) !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border);
    background: rgba(58, 53, 52, 0.78) !important;
}

.stPlotlyChart {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border);
    background: rgba(58, 53, 52, 0.78);
    padding: 8px;
}

div[data-baseweb="select"] > div {
    background-color: #3A3534 !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}

div[role="listbox"] {
    background-color: #3A3534 !important;
    color: var(--text) !important;
}

input, textarea {
    color: var(--text) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(58, 53, 52, 0.68);
    color: var(--text-soft) !important;
    border-radius: 12px 12px 0 0;
    padding: 10px 18px;
    border: 1px solid transparent;
    font-family: 'Inter', sans-serif !important;
}

.stTabs [aria-selected="true"] {
    color: var(--highlight) !important;
    border-bottom: 2px solid var(--highlight) !important;
    background: rgba(58, 53, 52, 0.92);
}

div[data-testid="stAlert"] {
    background: rgba(114, 75, 57, 0.35) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}

div[data-testid="stAlert"] * {
    color: var(--text) !important;
}

button[kind="primary"] {
    background-color: var(--accent) !important;
    color: #fff7f1 !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

button[kind="secondary"] {
    background-color: rgba(58, 53, 52, 0.85) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Medallion")
    st.markdown("SQL Server Dashboard")
    st.markdown("---")
    menu = st.radio("Navigate", ["Overview", "Bronze", "Silver", "Gold & Insights"])

st.markdown("""
<div class="hero">
    <h1>Medallion Data Warehouse Dashboard</h1>
    <p>Directly reading Bronze, Silver, and Gold objects from SQL Server. No duplicate cleaning in Streamlit.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Bronze Tables", "3")
c2.metric("Silver Tables", "3")
c3.metric("Gold Views", "3")
c4.metric("Dashboard Ready", "Yes")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Bronze", "Silver", "Gold & Insights"])

with tab1:
    st.subheader("Overview")
    st.info("This app consumes SQL warehouse objects directly. ETL and transformations happen in SQL scripts, not in Python.")

with tab2:
    st.subheader("Bronze Layer")
    table = st.selectbox("Choose Bronze table", ["bronze.crm_cust_info", "bronze.crm_sales_details", "bronze.crm_prd_info"])
    query_map = {
        "bronze.crm_cust_info": "SELECT TOP 50 * FROM bronze.crm_cust_info",
        "bronze.crm_sales_details": "SELECT TOP 50 * FROM bronze.crm_sales_details",
        "bronze.crm_prd_info": "SELECT TOP 50 * FROM bronze.crm_prd_info",
    }
    st.dataframe(run_query(query_map[table]), use_container_width=True)

with tab3:
    st.subheader("Silver Layer")
    table = st.selectbox("Choose Silver table", ["silver.crm_cust_info", "silver.crm_sales_details", "silver.crm_prd_info"])
    query_map = {
        "silver.crm_cust_info": "SELECT TOP 50 * FROM silver.crm_cust_info",
        "silver.crm_sales_details": "SELECT TOP 50 * FROM silver.crm_sales_details",
        "silver.crm_prd_info": "SELECT TOP 50 * FROM silver.crm_prd_info",
    }
    st.dataframe(run_query(query_map[table]), use_container_width=True)

with tab4:
    st.subheader("Gold Layer & Insights")

    g1, g2, g3 = st.columns(3)
    g1.metric("Dim Customers", f"{len(gold_customers):,}")
    g2.metric("Dim Products", f"{len(gold_products):,}")
    g3.metric("Fact Sales", f"{len(gold_sales):,}")

    gold_table = st.radio(
        "Choose Gold object",
        ["gold.dim_customers", "gold.dim_products", "gold.fact_sales"],
        horizontal=True
    )

    gold_map = {
        "gold.dim_customers": "SELECT TOP 50 * FROM gold.dim_customers",
        "gold.dim_products": "SELECT TOP 50 * FROM gold.dim_products",
        "gold.fact_sales": "SELECT TOP 50 * FROM gold.fact_sales",
    }
    st.dataframe(run_query(gold_map[gold_table]), use_container_width=True)

    monthly = run_query("""
        SELECT
            CONVERT(char(7), order_date, 120) AS order_month,
            SUM(sales_amount) AS total_sales
        FROM gold.fact_sales
        GROUP BY CONVERT(char(7), order_date, 120)
        ORDER BY order_month
    """)

    fig1 = px.line(monthly, x="order_month", y="total_sales", markers=True, title="Monthly Sales Trend")
    fig1.update_traces(line=dict(color="#CF9D7B", width=3), marker=dict(color="#CF9D7B", size=8))
    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="#3A3534",
        plot_bgcolor="#3A3534",
        font=dict(color="#F5EDE6", family="Inter"),
        title_font=dict(color="#CF9D7B", family="Cormorant Garamond", size=24)
    )
    st.plotly_chart(fig1, use_container_width=True)

    category_sales = run_query("""
        SELECT TOP 10
            p.category,
            SUM(f.sales_amount) AS total_sales
        FROM gold.fact_sales f
        LEFT JOIN gold.dim_products p
            ON f.product_key = p.product_key
        GROUP BY p.category
        ORDER BY total_sales DESC
    """)

    fig2 = px.bar(category_sales, x="category", y="total_sales", title="Sales by Category", color_discrete_sequence=["#724B39"])
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#3A3534",
        plot_bgcolor="#3A3534",
        font=dict(color="#F5EDE6", family="Inter"),
        title_font=dict(color="#CF9D7B", family="Cormorant Garamond", size=24)
    )
    st.plotly_chart(fig2, use_container_width=True)

    country_sales = run_query("""
        SELECT TOP 10
            c.country,
            SUM(f.sales_amount) AS total_sales
        FROM gold.fact_sales f
        LEFT JOIN gold.dim_customers c
            ON f.customer_key = c.customer_key
        GROUP BY c.country
        ORDER BY total_sales DESC
    """)

    fig3 = px.bar(country_sales, x="country", y="total_sales", title="Sales by Country", color_discrete_sequence=["#CF9D7B"])
    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="#3A3534",
        plot_bgcolor="#3A3534",
        font=dict(color="#F5EDE6", family="Inter"),
        title_font=dict(color="#CF9D7B", family="Cormorant Garamond", size=24)
    )
    st.plotly_chart(fig3, use_container_width=True)

st.success("Dashboard connected to SQL Server warehouse successfully.")