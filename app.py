import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

try:
    st.title('Stock Dashboard')
    st.header('Streamlit header')
    st.subheader('Streamlit header')
    st.write('My content will be written here!')
    st.caption('My caption are here!')

    tickers = ('NVDA','MSFT','GOOGL','META','IBM')
    ticker = st.sidebar.selectbox('Pick your Stock Ticker',tickers)
    #ticker = st.sidebar.text_input('Ticker')
    start_date = st.sidebar.date_input('Start Date')
    end_date = st.sidebar.date_input('End Date')

    # tick_value = yf.Ticker(ticker)
    # data = tick_value.history(start=start_date, end=end_date)
    # data

    data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker')
    # data = data.drop(columns=data.rows.levels[0][0], axis=1, level=0, inplace=False)
    #data = data.drop(columns="MSFT", axis=1, level=0)
    #data.columns = data.columns.remove_unused_levels()
    data = data.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)
    data
    fig = px.line(data, x = data.index, y=data['Adj Close'], title=ticker)
    st.plotly_chart(fig)

    pricing_data, news = st.tabs(["Pricing Data", "Top 10 News"])

    with pricing_data:
        st.header('Price Movements')
        #st.write(data)
        data2 = data
        data2['% Change'] = data['Adj Close']/data['Adj Close'].shift(1) - 1
        data2.dropna(inplace=True)
        st.write(data2)
        annual_return = data2['% Change'].mean()*252*100
        st.write('Annual Return is ',annual_return, '%')

    from stocknews import StockNews
    with news:
        st.header(f'News of {ticker}')
        sn = StockNews(ticker, save_news=False)
        data_news = sn.read_rss()
        for i in range(10):
            st.subheader(f'News{i+1}')
            st.write(data_news['published'][i])
            st.write(data_news['title'][i])
            st.write(data_news['summary'][i])
            title_sentiment = data_news['sentiment_title'][i]
            st.write(f'Title Sentiment{title_sentiment}')
            news_sentiment = data_news['sentiment_summary'][i]
            st.write(f'News Sentiment{news_sentiment}')    

except Exception as e:
    st.error(f"PLease select Stock Ticker and proper values for Start and End Dates ")
