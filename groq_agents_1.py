import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd

# Load API keys
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ API key not found. Please set it in your .env file.")
    st.stop()

# Function to normalize company input and handle Indian stocks
def get_company_symbol(company: str) -> str:
    """
    Returns a valid stock symbol.
    Supports Indian stocks with '.NS' suffix.
    """
    company = company.strip().title()
    symbols = {
        "Infosys": "INFY.NS",
        "Tcs": "TCS.NS",
        "Reliance": "RELIANCE.NS",
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL",
    }
    # Return mapped symbol if known, else use input directly
    return symbols.get(company, company.upper())

# 🎯 Stock Data Agent
stock_agent = Agent(
    name="Stock Data Agent",
    model=Groq(id="llama-3.3-70b-versatile", api_key=groq_api_key),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    instructions=["Use tables to display stock data."],
    show_tool_calls=False,
    markdown=True,
    debug_mode=False,
)

# 🎯 Finance Analysis Team (with stock agent)
agent_team = Agent(
    name="Finance Analysis Team",
    model=Groq(id="llama-3.3-70b-versatile", api_key=groq_api_key),
    team=[stock_agent],
    instructions=["Use tables for comparisons and include analyst insights."],
    show_tool_calls=False,
    markdown=True,
    debug_mode=False,
)

# Streamlit UI
st.set_page_config(page_title="📈 Financial Insights", layout="wide")
st.title("📈 Financial AI - Stock Prices, Analyst Ratings & Fundamentals")

# User Input
col1, col2 = st.columns(2)
with col1:
    company_1 = st.text_input("Enter first company (e.g., 'Tesla', 'Reliance'):")
with col2:
    company_2 = st.text_input("Enter second company (optional):")

if st.button("Get Stock Analysis"):

    if not company_1:
        st.warning("Please enter at least one company.")
        st.stop()

    symbol_1 = get_company_symbol(company_1)
    symbol_2 = get_company_symbol(company_2) if company_2 else None

    # Fetch and display historical stock prices (chart)
    with st.spinner(f"Fetching stock data for {symbol_1}..."):
        try:
            data_1 = yf.download(symbol_1, period="6mo")
            st.subheader(f"📈 {symbol_1} - Last 6 Months Closing Price")
            st.line_chart(data_1["Close"])
        except Exception as e:
            st.warning(f"Could not fetch historical data for {symbol_1}: {e}")

    if symbol_2:
        try:
            data_2 = yf.download(symbol_2, period="6mo")
            st.subheader(f"📈 {symbol_2} - Last 6 Months Closing Price")
            st.line_chart(data_2["Close"])
        except Exception as e:
            st.warning(f"Could not fetch historical data for {symbol_2}: {e}")

    # Generate agent query for fundamentals and analyst recommendations
    query = f"Summarize and compare analyst recommendations and fundamentals for {symbol_1}"
    if symbol_2:
        query += f" and {symbol_2}"
    query += ". Show in tables."

    with st.spinner("Generating financial analysis with AI..."):
        try:
            response = agent_team.run(query)
            st.subheader("💡 AI Insights & Stock Analysis")
            st.markdown(response.content)
        except Exception as e:
            st.error(f"Error generating analysis: {e}")