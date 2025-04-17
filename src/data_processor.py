import streamlit as st
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from sentiment_analyzer import clean_up_text
from collections import Counter

from reddit import (
    get_submissions_text,
    get_subreddit_user_count,
    get_top_submission_url,
    create_reddit_connection,
    get_comments_text,
    get_submission_score,
)
from sentiment_analyzer import analyze_sentiment, create_sentiment_pipeline
import os
from models import models


def initialize_sentiment_pipelines() -> None:
    for nickname, model_name in models.items():
        st.session_state[nickname] = create_sentiment_pipeline(model_name)


def initialize_reddit_connection() -> None:
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if client_id is None or client_secret is None:
        raise EnvironmentError(
            "CLIENT_ID and CLIENT_SECRET are required for the connection to reddit. At least one is not set currently."
        )
    st.session_state.connection = create_reddit_connection(client_id, client_secret)


def get_subreddit_dashboard_data(subreddit: str) -> Dict:
    submissions, sentiment_count = process_submissions(subreddit)

    return {
        "subscribers": get_subreddit_user_count(st.session_state.connection, subreddit),
        "top_submission_link": get_top_submission_url(
            st.session_state.connection, subreddit
        ),
        "sentiment_count": sentiment_count,
        "submissions": submissions,
    }


def get_posts_dashboard_data(submission_url: str) -> Dict:
    comments = get_comments_text(
        st.session_state.connection,
        submission_url,
        st.session_state.submission_count,
    )
    sentiments = [
        analyze_sentiment(st.session_state[st.session_state.selected_model], comment)
        for comment in comments
    ]
    sentiment_count = Counter(sentiments)

    return {
        "score": get_submission_score(st.session_state.connection, submission_url),
        "comments": comments,
        "sentiment_count": sentiment_count,
    }


def process_submissions(subreddit: str) -> Tuple[List[str], Dict[str, int]]:
    submissions = [
        clean_up_text(submission)
        for submission in get_submissions_text(
            st.session_state.connection,
            subreddit,
            st.session_state.filter_mode,
            st.session_state.submission_count,
        )
    ]
    sentiments = [
        analyze_sentiment(
            st.session_state[st.session_state.selected_model],
            submission,
        )
        for submission in submissions
    ]

    return (submissions, Counter(sentiments))
