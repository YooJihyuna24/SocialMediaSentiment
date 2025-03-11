import streamlit as st
from transformers import pipeline
import praw
import dotenv
import os

dotenv.load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


st.title("Social Media Sentiment Analysis")
subreddit = st.text_input("Subreddit", "all")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="reddit_bot",
)
analyzer = pipeline("sentiment-analysis")


for listing in reddit.subreddit(subreddit).hot(limit=10):
    st.write(listing.title)
    st.write(analyzer(listing.title))
