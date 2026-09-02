import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Streamlit Page Setup
st.set_page_config(
    page_title="Stock Portfolio Tracker | CodeAlpha",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #E6F4EA;
        color: #1F2937;
    }

    /* Top Navbar Header */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 12px 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }

    .nav-brand {
        font-weight: 700;
        font-size: 1.1rem;
        color: #047857;
    }

    /* Hero Banner Card */
    .hero-card {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        border-radius: 20px;
        padding: 28px 32px;
        color: white;
        box-shadow: 0 8px 20px rgba(5, 150, 105, 0.18);
        margin-bottom: 24px;
    }
    
    .hero-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.9;
        margin-bottom: 6px;
        font-weight: 600;
    }
    
    .hero-balance {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 18px;
    }

    .sub-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 10px 18px;
        display: inline-block;
        margin-right: 12px;
    }

    /* Section Labels */
    .violet-pill {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        padding: 5px 14px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
    }

    /* Sidebar Fixes */
    section[data-testid="stSidebar"] {
        background-color: #047857 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #065F46 !important;
        color: #FFFFFF !important;
        border: 1px solid #10B981 !important;
    }
    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }
    div[data-baseweb="input"] input {
        background-color: #065F46 !important;
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.2);
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Predefined Stock Prices (NSE - INR)
STOCK_PRICES = {
    "TITAN": 3450,
    "RELIANCE": 2980,
    "TCS": 4120,
    "INFY": 1820,
    "HDFCBANK": 1640,
    "TATAMOTORS": 995,
    "BHARTIARTL": 1520,
    "LT": 3680
}

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {"TITAN": 10, "RELIANCE": 5, "TATAMOTORS": 15}

# Top Bar with Authentication & Rating Controls
nav_col1, nav_col2, nav_col3 = st.columns([4, 2, 2])
with nav_col1:
    st.markdown('<div class="nav-brand">CodeAlpha Financial Dashboard</div>', unsafe_allow_html=True)
with nav_col2:
    rating = st.selectbox("Rate Platform", ["⭐⭐⭐⭐⭐ (5/5)", "⭐⭐⭐⭐ (4/5)", "⭐⭐⭐ (3/5)"], label_visibility="collapsed")
with nav_col3:
    auth_choice = st.selectbox("Account Access", ["Account: Active", "Login / Switch", "Sign Up"], label_visibility="collapsed")

st.markdown("---")

# Sidebar Controls
st.sidebar.markdown("### Portfolio Management")
st.sidebar.markdown("Configure holdings and assets:")

selected_stock = st.sidebar.selectbox("Select Asset Symbol", list(STOCK_PRICES.keys()))
quantity = st.sidebar.number_input("Shares Quantity", min_value=1, step=1, value=1)

sb_col1, sb_col2 = st.sidebar.columns(2)
with sb_col1:
    if st.button("Add Asset"):
        if selected_stock in st.session_state.portfolio:
            st.session_state.portfolio[selected_stock] += quantity
        else:
            st.session_state.portfolio[selected_stock] = quantity
        st.rerun()

with sb_col2:
    if st.button("Reset"):
        st.session_state.portfolio = {}
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Secured via CodeAlpha Financial Systems")

# Data Processing
df_data = []
total_val = 0
for symbol, qty in st.session_state.portfolio.items():
    price = STOCK_PRICES[symbol]
    inv_val = qty * price
    total_val += inv_val
    df_data.append({
        "Asset": symbol,
        "Quantity": qty,
        "Market Price (INR)": f"₹{price:,.2f}",
        "Total Value (INR)": inv_val
    })

df = pd.DataFrame(df_data)

# Hero Header
st.markdown(f"""
    <div class="hero-card">
        <div class="hero-title">Total Investment Valuation</div>
        <div class="hero-balance">₹{total_val:,.2f} INR</div>
        <div>
            <div class="sub-card">
                <span style="font-size:0.78rem;">Active Positions</span><br>
                <strong>{len(df)} Holdings</strong>
            </div>
            <div class="sub-card">
                <span style="font-size:0.78rem;">Largest Holding</span><br>
                <strong>{df.loc[df['Total Value (INR)'].idxmax()]['Asset'] if not df.empty else 'None'}</strong>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Grid Layout: Left Table & Right Analytics
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<span class="violet-pill">Holdings</span> &nbsp; **Asset Distribution Breakdown**', unsafe_allow_html=True)
    st.write("")
    if not df.empty:
        st.dataframe(
            df.style.format({"Total Value (INR)": "₹{:,.2f}"}),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No holdings present in your portfolio. Add assets from the sidebar panel.")

with col_right:
    st.markdown('<span class="violet-pill">Allocation</span> &nbsp; **Percentage Breakdown (%)**', unsafe_allow_html=True)
    
    if not df.empty:
        # Interactive Percentage Donut Chart
        fig_donut = px.pie(
            df, 
            names='Asset', 
            values='Total Value (INR)', 
            hole=0.55,
            color_discrete_sequence=['#8B5CF6', '#10B981', '#3B82F6', '#F59E0B', '#EC4899']
        )
        fig_donut.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Value: ₹%{value:,.2f}<br>Share: %{percent}'
        )
        fig_donut.update_layout(
            showlegend=False,
            height=260,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.write("Add assets to view percentage share.")

# Statement Export
st.markdown("---")
if st.button("Generate Statement File"):
    summary_text = "OFFICIAL PORTFOLIO SUMMARY STATEMENT (INR)\n=========================================\n"
    for row in df_data:
        summary_text += f"Stock: {row['Asset']} | Qty: {row['Quantity']} | Value: ₹{row['Total Value (INR)']}\n"
    summary_text += f"\nTotal Net Valuation: ₹{total_val:,.2f} INR"
    
    st.download_button(
        label="Save Summary Text File",
        data=summary_text,
        file_name="portfolio_summary.txt",
        mime="text/plain"
    )