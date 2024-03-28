import pandas as pd

def get_sentiment_score(df:pd.DataFrame)->pd.DataFrame:
    """
    This function will take a dataframe as input and return the final sentiment score of the tweets as well as number of positive, neutral and negative tweets.
    """
    total_negative = df['Negative'].sum()
    total_neutral = df['Neutral'].sum()
    total_positive = df['Positive'].sum()

    total_negative_count = 0
    total_neutral_count = 0
    total_positive_count = 0


    for index, row in df.iterrows():
        if row['Sentiment']=='negative':
            total_negative_count+=1
        if row['Sentiment']=='neutral':
            total_neutral_count+=1
        if row['Sentiment']=='positive':
            total_positive_count+=1


    # Calculate the total number of tweets
    total_tweets = len(df)

    # Calculate the average sentiment score for each category
    avg_negative = total_negative / total_tweets
    avg_neutral = total_neutral / total_tweets
    avg_positive = total_positive / total_tweets
    
    final_score=avg_positive-avg_negative
    
    return final_score, total_positive_count, total_neutral_count, total_negative_count