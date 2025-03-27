from typing import Dict
from dotenv import load_dotenv

import pandas as pd
from reddit import (
    get_submissions_text,
    get_subreddit_user_count,
    get_top_submission,
    initialize_reddit_api,
)
from sentiment_analyzer import analyze_sentiment, create_sentiment_pipeline
import os


class DataProcessor:
    def __init__(self):
        load_dotenv()
        self.connection = initialize_reddit_api(
            os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")
        )
        self.sentiment_pipeline = create_sentiment_pipeline()

    def get_dashboard_data(self, subreddit: str) -> Dict:
        sentiment_count = self.process_submission_to_sentiment(subreddit)
        return {
            "subscribers": get_subreddit_user_count(self.connection, subreddit),
            "top_submission_link": get_top_submission(self.connection, subreddit),
            "sentiment_count": sentiment_count,
        }

    def process_submission_to_sentiment(self, subreddit: str) -> Dict[str, int]:
        submissions = pd.DataFrame(
            {"submission": get_submissions_text(self.connection, subreddit, "hot")}
        )

        submissions_with_sentiment = submissions.assign(
            sentiment=lambda df: df["submission"].apply(
                lambda text: analyze_sentiment(self.sentiment_pipeline, text)
            )
        )
        sentiment_count = (
            submissions_with_sentiment["sentiment"].value_counts().to_dict()
        )

        return sentiment_count
