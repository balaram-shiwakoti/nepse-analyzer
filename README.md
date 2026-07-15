
# 📈 NEPSE Stock Market Analyzer & Portfolio Tracker

An interactive data analytics and financial dashboard built specifically for the **Nepal Stock Exchange (NEPSE)** context. This application allows users to perform technical analysis on historical stock data, calculate trend indicators (Simple Moving Averages), and track custom portfolios with built-in Nepalese financial rules, including the **7.5% Capital Gains Tax (CGT)** for short-term holdings.

---

## 🛠️ Project Architecture & Pipeline


 Raw Market Data                     User Transaction Inputs
(nepse_data.csv)                       (Symbol, Buy Price, Units)
       │                                          │
       ▼                                          ▼

```

Pandas Data Processing                   Dynamic Portfolio Valuation
[Rolling SMA, Min/Max Highs]            [Cost vs Current, Tax (CGT) Deductions]
│                                          │
└───────────────────┬──────────────────────┘
▼
Interactive Streamlit UI
[Plotly Candlesticks & Progress Metrics]

```

---

## 📂 Project Structure

```text
nepse_analyzer/
│
├── data_generator.py     # Generates realistic 180-day historical stock prices for NEPSE
├── app.py                # Main Streamlit dashboard code (Technical analysis & Tracker)
├── nepse_data.csv        # Generated CSV file containing historical trade logs (Generated after step 1)
└── README.md             # Project documentation

```

---

## 🚀 Getting Started

Follow these steps to run the application on your computer:

### 1. Prerequisite Installations

Open your terminal (or Command Prompt) and install the necessary data science, charting, and UI libraries:

```bash
pip install -r requirements.txt 

```

### 2. Generate the Historical Data

Run the mock generator script to create 180 days of realistic financial data for popular NEPSE listings like **NTC, GBIME, NIL, and HDL**:

```bash
python data_generator.py

```

This will successfully create a `nepse_data.csv` file in your project directory.

### 3. Launch the Dashboard

Run the interactive Streamlit web application:

```bash
streamlit run app.py

```

This will open the dashboard in your default browser at `http://localhost:8501`.

---

## 📊 Key Features & Tech Stack

### 📈 Market Analyzer Section

* **Plotly Interactive Candlestick Charts**: Smooth zooming, hovering, and tracking of historical prices.
* **Moving Average Indicators**: Dynamic **Simple Moving Average (SMA)** overlays using pandas rolling window calculations (`df['Close'].rolling().mean()`).
* **Summary Metrics**: Automatically extracts historical 180-day Highs, Lows, Average Volumes, and Daily Percentage Changes.

### 💼 Portfolio Tracker Section

* **Transaction Entry**: Input your purchase price, volume (Kitta), and transaction dates.
* **Dynamic Net Asset Valuation**: Live calculations of current holdings value against original purchase costs.
* **Nepalese Tax Rules Compliance**: Automatically applies a **7.5% Capital Gains Tax (CGT)** strictly on profitable transactions, outputting your actual Net Profit/Loss.

