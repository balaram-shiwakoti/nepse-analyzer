# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="NEPSE Stock Analyzer & Portfolio Tracker", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("nepse_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file 'nepse_data.csv' not found! Please run 'python data_generator.py' first.")
    st.stop()

st.title("📈 NEPSE Stock Market Analyzer & Portfolio Tracker")
st.write("Analyze performance, trends, and manage your portfolio with realistic tax metrics.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Navigation & Settings")
app_mode = st.sidebar.radio("Choose Section", ["Market Analyzer", "My Portfolio Tracker"])

if app_mode == "Market Analyzer":
    st.header("🔍 Stock Performance & Historical Charts")
    
    # Selecting symbol
    symbols = df['Symbol'].unique()
    selected_symbol = st.selectbox("Select Stock Symbol", symbols)
    
    # Filter historical records for this symbol
    stock_df = df[df['Symbol'] == selected_symbol].sort_values(by='Date')
    
    # Simple Moving Average Period Selection
    sma_period = st.sidebar.slider("SMA Period", min_value=5, max_value=50, value=20)
    stock_df['SMA'] = stock_df['Close'].rolling(window=sma_period).mean()
    
    # --- METRICS ROW ---
    latest_price = stock_df['Close'].iloc[-1]
    prev_price = stock_df['Close'].iloc[-2]
    price_change = latest_price - prev_price
    pct_change = (price_change / prev_price) * 100
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Latest Close", f"Rs. {latest_price:,.2f}", f"{price_change:+.2f} ({pct_change:+.2f}%)")
    with m2:
        st.metric("180-Day High", f"Rs. {stock_df['High'].max():,.2f}")
    with m3:
        st.metric("180-Day Low", f"Rs. {stock_df['Low'].min():,.2f}")
    with m4:
        st.metric("Average Volume", f"{int(stock_df['Volume'].mean()):,}")

    # --- PLOTLY CANDLESTICK CHART ---
    st.subheader("Candlestick Chart & Moving Average")
    
    fig = go.Figure()
    
    # Candlestick Trace
    fig.add_trace(go.Candlestick(
        x=stock_df['Date'],
        open=stock_df['Open'],
        high=stock_df['High'],
        low=stock_df['Low'],
        close=stock_df['Close'],
        name="Market Price"
    ))
    
    # SMA Trace
    fig.add_trace(go.Scatter(
        x=stock_df['Date'],
        y=stock_df['SMA'],
        line=dict(color='orange', width=1.5),
        name=f"{sma_period}-day SMA"
    ))
    
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        yaxis_title="Price (NPR)",
        xaxis_title="Date",
        margin=dict(l=40, r=40, t=20, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- PORTFOLIO TRACKER ---
else:
    st.header("💼 My Secondary Market Portfolio Tracker")
    st.write("Log your investments, track active value, and calculate capital gains tax outcomes.")
    
    # In-memory session state initialization for portfolio
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = [
            {"Symbol": "NTC", "Purchase Price": 850.00, "Units": 50, "Date": "2026-01-10"},
            {"Symbol": "GBIME", "Purchase Price": 220.00, "Units": 100, "Date": "2026-02-15"}
        ]
        
    # Transaction input form
    with st.expander("➕ Add New Transaction"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            sym_input = st.selectbox("Stock", df['Symbol'].unique(), key="port_sym")
        with col2:
            price_input = st.number_input("Purchase Price (NPR)", min_value=1.0, value=100.0, step=1.0)
        with col3:
            units_input = st.number_input("Units (Kitta)", min_value=10, value=10, step=10)
        with col4:
            date_input = st.date_input("Transaction Date", value=datetime.today())
            
        if st.button("Add to Portfolio"):
            new_trade = {
                "Symbol": sym_input,
                "Purchase Price": price_input,
                "Units": units_input,
                "Date": str(date_input)
            }
            st.session_state.portfolio.append(new_trade)
            st.success(f"Added {units_input} units of {sym_input} successfully!")

    # Calculate Portfolio Performance
    if len(st.session_state.portfolio) > 0:
        port_df = pd.DataFrame(st.session_state.portfolio)
        
        # Get current prices dynamically from load_data
        current_prices = {}
        for s in port_df['Symbol'].unique():
            current_prices[s] = df[df['Symbol'] == s].sort_values(by='Date')['Close'].iloc[-1]
            
        port_df['Current Price'] = port_df['Symbol'].map(current_prices)
        port_df['Total Cost'] = port_df['Purchase Price'] * port_df['Units']
        port_df['Current Value'] = port_df['Current Price'] * port_df['Units']
        port_df['Raw Profit/Loss'] = port_df['Current Value'] - port_df['Total Cost']
        
        # Calculate individual CGT (7.5% for short-term holdings on gains only)
        port_df['Capital Gains Tax (7.5%)'] = port_df['Raw Profit/Loss'].apply(lambda x: x * 0.075 if x > 0 else 0.0)
        port_df['Net Profit/Loss'] = port_df['Raw Profit/Loss'] - port_df['Capital Gains Tax (7.5%)']
        
        # Display Table
        st.subheader("Your Holdings")
        st.dataframe(
            port_df.style.format({
                "Purchase Price": "Rs. {:.2f}",
                "Current Price": "Rs. {:.2f}",
                "Total Cost": "Rs. {:.2f}",
                "Current Value": "Rs. {:.2f}",
                "Raw Profit/Loss": "Rs. {:.2f}",
                "Capital Gains Tax (7.5%)": "Rs. {:.2f}",
                "Net Profit/Loss": "Rs. {:.2f}"
            }),
            use_container_width=True
        )
        
        # Summary Metrics
        total_investment = port_df['Total Cost'].sum()
        total_value = port_df['Current Value'].sum()
        net_profit = port_df['Net Profit/Loss'].sum()
        total_cgt = port_df['Capital Gains Tax (7.5%)'].sum()
        
        st.markdown("---")
        st.subheader("Portfolio Summary")
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("Total Investment", f"Rs. {total_investment:,.2f}")
        with s2:
            st.metric("Current Portfolio Value", f"Rs. {total_value:,.2f}")
        with s3:
            st.metric("Est. Capital Gains Tax (7.5%)", f"Rs. {total_cgt:,.2f}")
        with s4:
            st.metric("Net Profit / Loss", f"Rs. {net_profit:,.2f}", delta=f"{net_profit:+.2f}")
            
    else:
        st.info("Your portfolio is currently empty. Add a transaction above to start tracking performance!")