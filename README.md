# Multi-Agent Financial Insights Dashboard – AI-Driven Stock Analysis

A **multi-agent AI dashboard** for real-time stock analysis. This project leverages **LLaMA 3.3** and **Groq agents** to fetch stock prices, compare fundamentals, and summarize analyst recommendations — all visualized in interactive charts and tables using **Streamlit**. Ideal for finance enthusiasts, analysts, and developers exploring agentic AI in the stock market.

---

## Features

- **Agentic AI System**: Multiple agents collaborate to fetch, analyze, and summarize stock data.  
- **Real-Time Stock Prices**: Fetch historical and current stock prices with `yfinance`.  
- **Fundamentals & Analyst Recommendations**: Compare key financial metrics and analyst insights.  
- **Interactive Visualization**: Line charts, tables, and summaries rendered via Streamlit.  
- **Multi-Market Support**: Works with both global and Indian stocks.  
- **Extensible**: Easily add more agents or financial tools for deeper insights.  

---

## Tech Stack

- **AI Models:** LLaMA 3.3 via Groq API  
- **Agent Framework:** Custom multi-agent system (`phi.agent`)  
- **Tools:** `YFinanceTools`, `yfinance` for stock data  
- **Web Framework:** Streamlit  
- **Environment Management:** Python + dotenv for API keys  

---
## Usage
- Enter one or two company names (e.g., “Tesla” or “Reliance”).
- Click Get Stock Analysis.
- View historical stock prices, AI-generated fundamentals, and analyst insights.
