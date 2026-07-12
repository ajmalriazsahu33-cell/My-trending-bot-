import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="AI Trading Signal Bot", page_icon="📈", layout="centered")

st.title("📈 AI Trading Signal Bot")
st.write("Real-time market analysis aur signals ke liye neeche diye gaye button par click karein.")

ticker = st.selectbox("Asset Select Karein:", ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD"])
interval = st.selectbox("Timeframe (Candle Time):", ["1m", "5m", "15m"], index=1)

if st.button("🔄 Get Live Signal", type="primary"):
    with st.spinner("Market ka taza data check kiya ja raha hai..."):
        try:
            data = yf.download(tickers=ticker, period="1d", interval=interval)
            
            if data.empty:
                st.error("Data nahi mil saka. Sunday ko market band hoti hai!")
            else:
                close_prices = data['Close'].squeeze()
                rsi_series = ta.momentum.rsi(close_prices, window=14)
                ema_short_series = ta.trend.ema_indicator(close_prices, window=9)
                ema_long_series = ta.trend.ema_indicator(close_prices, window=21)

                last_price = float(close_prices.iloc[-1])
                rsi_val = float(rsi_series.iloc[-1])
                ema_s = float(ema_short_series.iloc[-1])
                ema_l = float(ema_long_series.iloc[-1])

                st.subheader(f"--- Analysis for {ticker} ---")
                col1, col2 = st.columns(2)
                col1.metric(label="Current Price", value=f"{last_price:.4f}")
                col2.metric(label="RSI Value", value=f"{rsi_val:.2f}")

                if rsi_val < 35 or ema_s > ema_l:
                    st.success("🟢 BOT RECOMMENDATION: BUY SIGNAL (Market Upar Ja Sakti Hai)")
                elif rsi_val > 65 or ema_s < ema_l:
                    st.error("🔴 BOT RECOMMENDATION: SELL SIGNAL (Market Niche Ja Sakti Hai)")
                else:
                    st.info("⚪ NO SIGNAL (Abhi Wait Karein)")
        except Exception as e:
            st.error(f"Koi error aya hai: {e}")

st.caption("Note: Yeh bot real international market ka data dikhata hai, OTC market ka nahi.")
              
