from typing import Dict
from dotenv import load_dotenv
from sentiment_analyzer import clean_up_text

import pandas as pd
from reddit import (
    get_submissions_text,
    get_subreddit_user_count,
    get_top_submission,
    create_reddit_connection,
)
from sentiment_analyzer import analyze_sentiment, create_sentiment_pipeline
import os


class DataProcessor:
    def __init__(self):
        load_dotenv()
        self.connection = create_reddit_connection(
            os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")
        )
        self.sentiment_pipeline = create_sentiment_pipeline()
        self.data = pd.DataFrame()

    def get_dashboard_data(self, subreddit: str) -> Dict:
        self.process_submission_to_sentiment(subreddit)
        return {
            "subscribers": get_subreddit_user_count(self.connection, subreddit),
            "top_submission_link": get_top_submission(self.connection, subreddit),
            "sentiment_count": self.data["sentiment"].value_counts().to_dict(),
            "submissions": self.data["submission"].to_list(),
        }

    def process_submission_to_sentiment(self, subreddit: str) -> None:
        self.data = self.data.assign(
            submission=get_submissions_text(self.connection, subreddit, "hot")
        )
        self.data.submission = self.data.submission.apply(
            lambda text: clean_up_text(text)
        ) 
        
        self.data = self.data.assign(
            sentiment=lambda df: df["submission"].apply(
                lambda text: analyze_sentiment(self.sentiment_pipeline, text)
            )
        )
