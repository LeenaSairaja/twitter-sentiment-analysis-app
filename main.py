import streamlit as st
import pandas as pd
import plotly.express as px
import time
from utils import get_sentiment_score
from core import get_df
from sentiment_analysis import perform_sentiment_analysis

# Page title
st.set_page_config(page_title='Sentimental Analysis', page_icon='🤖')
st.title('📈 Sentimental Analysis')

option = st.selectbox(
    'Choose the required stock',
    ('TSLA', 'XYZ'), index=None, placeholder="Select...",)

st.write('You selected:', option)


if option=='TSLA':

    with st.spinner('Performing Sentiment Analysis...'):
        TSLA_tweet_sentiments = get_df(datetime='2021-09-30 00:00:00+00:00',stock='TSLA',next_x_hours=24)
        time.sleep(2)
    st.success('Done!')

    # tweets table
    st.header("Tweets of TSLA stock on 30th September 2021")

    
    TSLA_tweet_sentiments_output=TSLA_tweet_sentiments[['Tweet','Sentiment']]
    st.markdown(f"{len(TSLA_tweet_sentiments_output)} Tweets found")
    TSLA_tweet_sentiments_output

    
    # sentiment
    
    sentiment_score, total_positive, total_neutral, total_negative=get_sentiment_score(TSLA_tweet_sentiments)
    st.header(f"Sentiment score: {round(sentiment_score,2)}")
    st.write(f"Scale: -1 to 1")

    # add number of positive, negative and neutral tweets
    st.markdown(f"Number of positive tweets: _**{total_positive}**_")
    st.markdown(f"Number of neutral tweets: _**{total_neutral}**_")
    st.markdown(f"Number of negative tweets: _**{total_negative}**_")

    # box - positive, negative, neutral
    if sentiment_score>0.2:
        st.success("The sentiment score is positive")
    elif sentiment_score<-0.2:
        st.error("The sentiment score is negative")
    else:
        st.warning("The sentiment score is neutral")

    # graph
    st.header("Price of TSLA stock 7 days around 30-09-2021")

    st.markdown("Interval: 1d")
    st.markdown("Source: Yahoo Finance")
    TSLA_stock_prices = pd.read_csv("TSLA 14 days stock price.csv")
    fig=px.line(TSLA_stock_prices,x="Date",y="Close")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    st.markdown("Choose the required stock")