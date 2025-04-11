from typing import Dict
from dotenv import load_dotenv
from sentiment_analyzer import clean_up_text

import pandas as pd
from reddit import (
    get_submissions_text,
    get_subreddit_user_count,
    get_top_submission_url,
    create_reddit_connection,
    get_comments_text,
)
from sentiment_analyzer import analyze_sentiment, create_sentiment_pipeline
import os


class DataProcessor:
    def __init__(self, selected_model):
        load_dotenv()
        self.connection = create_reddit_connection(
            os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")
        )
        if selected_model == "Standard":
            self.sentiment_pipeline = create_sentiment_pipeline(
                model_name="bhadresh-savani/distilbert-base-uncased-emotion"
            )
        elif selected_model == "Political":
            self.sentiment_pipeline = create_sentiment_pipeline(
                model_name="m-newhauser/distilbert-political-tweets"
            )

        self.data = pd.DataFrame()

    def get_subreddit_dashboard_data(
        self, subreddit: str, submissions_count: int
    ) -> Dict:
        self.process_submission_to_sentiment(subreddit, submissions_count)
        return {
            "subscribers": get_subreddit_user_count(self.connection, subreddit),
            "top_submission_link": get_top_submission_url(self.connection, subreddit),
            "sentiment_count": self.data["sentiment"].value_counts().to_dict(),
            "submissions": self.data["submission"].to_list(),
        }

    def process_submission_to_sentiment(
        self, subreddit: str, submissions_count: int
    ) -> None:
        self.data = self.data.assign(
            submission=get_submissions_text(
                self.connection, subreddit, "hot", submissions_count
            )
        )
        self.data.submission = self.data.submission.apply(
            lambda text: clean_up_text(text)
        )

        self.data = self.data.assign(
            sentiment=lambda df: df["submission"].apply(
                lambda text: analyze_sentiment(self.sentiment_pipeline, text)
            )
        )

    def get_posts_dashboard_data(
        self, submission_url: str, limit: int = 30
    ) -> pd.DataFrame:
        comments = get_comments_text(self.connection, submission_url, limit)
        sentiments = [
            analyze_sentiment(self.sentiment_pipeline, text) for text in comments
        ]
        return pd.DataFrame({"comment": comments, "sentiment": sentiments})
