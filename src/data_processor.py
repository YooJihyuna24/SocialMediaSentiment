from typing import List, Dict
from dotenv import load_dotenv

import pandas as pd
import reddit
import sentiment_analyzer 
import os


class DataProcessor:
    def __init__(self):
        load_dotenv()
        self.connection = reddit.initialize_reddit_api(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
        self.sentiment_analyzer = sentiment_analyzer.initialize_analyzer()

    def fetch_and_process_data(self, subreddit: str) -> List[dict]:
        posts_data = reddit.get_hot_submissions_with_dates(self.connection, subreddit)
        processed_data = []
        for post in posts_data:
            sentiment = sentiment_analyzer.analyze_sentiment(self.sentiment_analyzer, post["text"])
            processed_data.append({
                "title": post["title"],
                "text": post["text"],
                "created_date": post["created_date"],
                "sentiment": sentiment
            })
        
        return processed_data

    def analyze_sentiment(self, submissions: List[str]) -> List[str]:
        """
        Führt eine Sentiment-Analyse für eine Liste von Texten durch.

        :param submissions: Liste der Reddit-Beiträge
        :return: Liste der Sentiment-Ergebnisse (z. B. "positive", "negative", "neutral")
        """
        return [sentiment_analyzer.analyze_sentiment(self.sentiment_analyzer, text) for text in submissions]

    def aggregate_kpis(self, submissions: List[str], sentiment_results: List[str]) -> Dict[str, int]:
        """
        Berechnet relevante KPIs wie Anzahl der Beiträge und Sentiment-Verteilung.

        :param submissions: Liste der Reddit-Beiträge
        :param sentiment_results: Liste der Sentiment-Analyse-Ergebnisse
        :return: Dictionary mit berechneten KPIs
        """
        sentiment_counts = pd.Series(sentiment_results).value_counts().to_dict()

        return {
            "total_posts": len(submissions),
            "positive": sentiment_counts.get("positive", 0),
            "negative": sentiment_counts.get("negative", 0),
            "neutral": sentiment_counts.get("neutral", 0),
        }

    def prepare_dashboard_data(self, submissions: List[str], sentiment_results: List[str]) -> pd.DataFrame:
        """
        Bereitet die Daten für das Dashboard auf, indem ein DataFrame erstellt wird.

        :param submissions: Liste der Reddit-Beiträge
        :param sentiment_results: Liste der Sentiment-Analyse-Ergebnisse
        :return: DataFrame mit Text und zugehörigem Sentiment
        """
        return pd.DataFrame({"text": submissions, "sentiment": sentiment_results})
