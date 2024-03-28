import pandas as pd
from sentiment_analysis import perform_sentiment_analysis
import yfinance as yf
from datetime import datetime, timedelta

def get_tweets()->pd.DataFrame:
    """
    This function will read the Stock Tweets for Sentiment Analysis and Prediction dataset and return the dataframe.
    """
    tweets = pd.read_csv("https://raw.githubusercontent.com/lem0n4id/twitter-sentiment-analysis/main/stock_tweets.csv")
    tweets['Date'] = pd.to_datetime(tweets['Date'])
    
    return tweets

def tweets_within_hours(df:pd.DataFrame, datetime:str='2021-09-30 00:13:26+00:00', stock_name:str='TSLA', next_x_hours:int=24) -> pd.DataFrame:
    """
    This function will filter the tweets for the specified stock and within the next x hours from the given datetime.
    """
    # Convert datetime string to datetime object
    datetime = pd.to_datetime(datetime)

    stock_name=stock_name.upper()

    # Filter dataframe for the specified stock and within the next x hours from the given datetime
    filtered_df = df[(df['Stock Name'] == stock_name) &
                     (df['Date'] >= datetime) &
                     (df['Date'] <= datetime + pd.Timedelta(hours=next_x_hours))]

    return filtered_df

def filter_unwanted_tweets(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    This function will filter the tweets that contain the specified stock ticker.
    """
    keywords = ['$' + ticker.capitalize(), '$' + ticker.lower(), '$' + ticker.upper(),
                '#' + ticker.capitalize(), '#' + ticker.lower(), '#' + ticker.upper()]

    filtered_tweets = []

    for index, row in df.iterrows():
        tweet = row['Tweet']
        for keyword in keywords:
            if keyword in tweet:
                filtered_tweets.append(row)
                break  # Once a keyword is found, move to the next tweet
                # If you want to include multiple occurrences of the keyword in the same tweet, remove the break statement

    return pd.DataFrame(filtered_tweets)

def get_df(datetime:str='2021-09-30 00:13:26+00:00',stock:str='TSLA',next_x_hours:int=24)->pd.DataFrame:
    try:
        df=get_tweets()
        TSLA_tweets_specified=tweets_within_hours(df, datetime=datetime, stock_name=stock, next_x_hours=next_x_hours)
        TSLA_tweets_filtered=filter_unwanted_tweets(TSLA_tweets_specified, ticker=stock)
        TSLA_tweets_sentiments=perform_sentiment_analysis(TSLA_tweets_filtered)
        print("Success")
        x=True
        return TSLA_tweet_sentiments
    except Exception as e:
        # if loading the model fails
        TSLA_tweet_sentiments = pd.read_csv("TSLA tweets score.csv",parse_dates=['Date'], index_col=['Date'])
        x=False
        return TSLA_tweet_sentiments

def get_stock_data(ticker:str, date:str="2021-09-30", days_around:int=7) -> pd.DataFrame:

    # make sure ticker is in upper case
    ticker=ticker.upper()

    # TODO: make sure the ticker is valid

    # Define the date
    date_obj = datetime.strptime(date, '%Y-%m-%d') # format of the date- yyyy-mm-dd

    # Calculate start and end dates
    start_date = (date_obj - timedelta(days=days_around)).strftime('%Y-%m-%d')
    end_date = (date_obj + timedelta(days=days_around)).strftime('%Y-%m-%d')

    try:
        # Download stock data for given ticker
        ticker_stock_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        return ticker_stock_data
    except Exception as e:
        print("Error downloading the data from yfinance. Details: ")
        print(e)
        TSLA_stock_prices = pd.read_csv("TSLA 14 days stock price.csv")
        return TSLA_stock_prices
