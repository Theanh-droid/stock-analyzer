
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import streamlit as st

st.set_page_config(page_title="Phân tích Cổ phiếu", layout="centered")
st.title("Phân tích thông tin và biểu đồ giá cổ phiếu")

symbol = st.text_input("Nhập mã cổ phiếu (Ví dụ: FPT.VN, VNM.VN, AAPL):", value="FPT.VN")

if symbol:
    try:
        df = yf.download(symbol, period="6mo", interval="1d")
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()

        st.subheader(f"Biểu đồ giá đóng cửa và MA20, MA50: {symbol}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Giá đóng cửa'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50'))
        fig.update_layout(title=f"Giá cổ phiếu {symbol} trong 6 tháng",
                          xaxis_title="Thời gian", yaxis_title="Giá", template="plotly_white")
        st.plotly_chart(fig)

        ticker = yf.Ticker(symbol)
        info = ticker.info
        st.subheader("Thông tin cơ bản")
        st.markdown(f"**Tên công ty**: {info.get('longName', 'N/A')}")
        st.markdown(f"**Ngành nghề**: {info.get('sector', 'N/A')}")
        st.markdown(f"**Vốn hóa**: {info.get('marketCap', 'N/A'):,} VND")
        st.markdown(f"**P/E Ratio**: {info.get('trailingPE', 'N/A')}")
        st.markdown(f"**Tăng trưởng EPS**: {info.get('earningsGrowth', 'N/A')}")
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu cho mã: {symbol}. Chi tiết: {e}")
