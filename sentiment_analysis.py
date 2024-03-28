from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

def preprocess(text):
    new_text = []


    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def init_model():
    task='sentiment'
    MODEL = f"cardiffnlp/twitter-roberta-base-{task}" # change to local path
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    # download label mapping
    labels=[]
    mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
    with urllib.request.urlopen(mapping_link) as f:
        html = f.read().decode('utf-8').split("\n")
        csvreader = csv.reader(html, delimiter='\t')
    labels = [row[1] for row in csvreader if len(row) > 1]

    # PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    model.save_pretrained(MODEL)

    return model, tokenizer, labels



# Function to get sentiment label for a tweet
def get_sentiment_label(tweet:str, model=None, tokenizer=None, labels=None):
    """
    This function will take a tweet as input and return the sentiment label.
    """
    if model is None or tokenizer is None or labels is None:
        # Initialize the model, tokenizer, and labels if not provided
        model, tokenizer, labels = init_model()
    
    tweet = preprocess(tweet)
    encoded_input = tokenizer(tweet, return_tensors='pt')
    output = model(**encoded_input)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    sentiment_index = np.argmax(scores)  # Get index of the highest score
    return labels[sentiment_index]

def apply_sentiment_labels(df:pd.DataFrame)->pd.DataFrame:
    """
    This function will take a dataframe as input and return a dataframe with the sentiment.
    """
    # Apply sentiment analysis to each tweet in df and add sentiment label to the DataFrame
    df['Sentiment'] = df['Tweet'].apply(get_sentiment_label)
    
    return df

def get_sentiment_scores(tweet, model=None, tokenizer=None, labels=None):
    if model is None or tokenizer is None or labels is None:
        # Initialize the model, tokenizer, and labels if not provided
        model, tokenizer, labels = init_model()
    
    tweet = preprocess(tweet)
    encoded_input = tokenizer(tweet, return_tensors='pt')
    output = model(**encoded_input)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    return {'Negative': scores[labels.index('negative')],
            'Neutral': scores[labels.index('neutral')],
            'Positive': scores[labels.index('positive')]}

def apply_sentiment_scores(df:pd.DataFrame)->pd.DataFrame:
    """
    This function will take a dataframe as input and return a dataframe with the sentiment.
    """
    # Apply sentiment analysis to each tweet in df and add Negative, Neutral and Positive label to the DataFrame
    df[['Negative', 'Neutral', 'Positive']] = df['Tweet'].apply(get_sentiment_scores).apply(pd.Series)
    
    return df

def perform_sentiment_analysis(df:pd.DataFrame)->pd.DataFrame:
    model, tokenizer, labels = init_model()
    df=apply_sentiment_labels(df)
    df=apply_sentiment_scores(df)
    return df


    
    
