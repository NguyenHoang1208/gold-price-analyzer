import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta

st.set_page_config(layout="wide")
st.title("📈 Phân tích kỹ thuật giá vàng bằng AI cơ bản")

# --- Chọn thời gian ---
st.sidebar.header("Cài đặt")
start_date = st.sidebar.date_input("Ngày bắt đầu", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("Ngày kết thúc", pd.to_datetime("today"))

# --- Tải dữ liệu giá vàng ---
@st.cache_data
def load_data(start, end):
    df = yf.download('GC=F', start=start, end=end)
    df['MA20'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
    df['MA50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    df['Buy'] = (df['RSI'] < 30) & (df['MACD'] > df['MACD_signal'])
    df['Sell'] = (df['RSI'] > 70) & (df['MACD'] < df['MACD_signal'])
    return df

df = load_data(start_date, end_date)

# --- Biểu đồ giá + MA + tín hiệu ---
st.subheader("📊 Biểu đồ giá vàng + tín hiệu mua bán")
fig1, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(df['Close'], label='Giá vàng', color='blue')
ax1.plot(df['MA20'], label='MA20', linestyle='--', color='orange')
ax1.plot(df['MA50'], label='MA50', linestyle='--', color='green')
ax1.scatter(df[df['Buy']].index, df[df['Buy']]['Close'], label='MUA', marker='^', color='lime', s=100)
ax1.scatter(df[df['Sell']].index, df[df['Sell']]['Close'], label='BÁN', marker='v', color='red', s=100)
ax1.set_title('Giá vàng và các đường MA')
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# --- Biểu đồ RSI ---
st.subheader("📈 Chỉ báo RSI")
fig2, ax2 = plt.subplots(figsize=(14, 2.5))
ax2.plot(df['RSI'], color='purple', label='RSI')
ax2.axhline(70, color='red', linestyle='--')
ax2.axhline(30, color='green', linestyle='--')
ax2.set_title('RSI (Relative Strength Index)')
ax2.grid(True)
st.pyplot(fig2)

# --- Biểu đồ MACD ---
st.subheader("📉 Chỉ báo MACD")
fig3, ax3 = plt.subplots(figsize=(14, 2.5))
ax3.plot(df['MACD'], label='MACD', color='blue')
ax3.plot(df['MACD_signal'], label='MACD Signal', color='red')
ax3.axhline(0, color='gray', linestyle='--')
ax3.set_title('MACD và MACD Signal')
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)
