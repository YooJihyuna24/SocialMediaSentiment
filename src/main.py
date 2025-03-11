import streamlit as st
import pandas as pd
import dotenv
import os
import plotly.express as px

from reddit import get_hot_submissions, initialize_reddit_api
from sentiment_analyzer import initialize_analyzer, analyze_sentiment
import settings

# initialization
dotenv.load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
if CLIENT_ID is None or CLIENT_SECRET is None:
    raise ValueError(
        "One or both environment variables for the reddit api are missing: 'CLIENT_ID' and 'CLIENT_SECRET'"
    )
reddit_connection = initialize_reddit_api(CLIENT_ID, CLIENT_SECRET)
sentiment_analyzer = initialize_analyzer()


st.title("Social Media Sentiment Analysis")
subreddit = st.text_input("Subreddit", "MachineLearning")

submissions = get_hot_submissions(
    reddit_connection, subreddit=subreddit, count=settings.SUBMISSION_COUNT
)

data = pd.DataFrame({"text": [submission.selftext for submission in submissions]})
data = data.assign(
    sentiment=[
        analyze_sentiment(sentiment_analyzer, text) for text in data["text"].to_list()
    ]
)
st.write(data)

sentiment_count = data["sentiment"].value_counts()
fig = px.pie(
    names=sentiment_count.index,
    values=sentiment_count.values,
    title="Sentiment Distribution",
)
st.plotly_chart(fig)
