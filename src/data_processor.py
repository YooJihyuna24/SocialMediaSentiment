import os
from collections import Counter
from typing import Dict, List, Tuple

import streamlit as st
from dotenv import load_dotenv

from models import models
from reddit import (
    create_reddit_connection,
    get_comments_text,
    get_submission_score,
    get_submissions_text,
    get_subreddit_subscriber_count,
    get_top_submission_url,
)
from sentiment_analyzer import (
    analyze_sentiment,
    clean_up_text,
    create_sentiment_pipeline,
)


def initialize_sentiment_pipelines() -> None:
    """
    Initializes sentiment analysis pipelines and stores them in the streamlit session state.
    """

    for nickname, model_name in models.items():
        st.session_state[nickname] = create_sentiment_pipeline(model_name)


def initialize_reddit_connection() -> None:
    """
    Initializes the Reddit connection using environment variables.
    The connection is stored in the streamlit session state.
    Raises:
        EnvironmentError: If either the 'CLIENT_ID' or 'CLIENT_SECRET' is missing from the environment.
    """
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if client_id is None or client_secret is None:
        raise EnvironmentError(
            "CLIENT_ID and CLIENT_SECRET are required for the connection to reddit. At least one is not set currently."
        )
    st.session_state.connection = create_reddit_connection(client_id, client_secret)


def get_subreddit_dashboard_data(subreddit: str) -> Dict:
    """
    Fetches dashboard data for a given subreddit.
    This function processes submissions for the specified subreddit and combines
    metrics into a dashboard data dictionary. It retrieves:
    - The number of subscribers.
    - The URL link for the top submission.
    - Sentiment analysis counts.
    - Submission text.
    Parameters:
        subreddit (str): The name of the subreddit for which to fetch data.
    Returns:
        dict: A dictionary containing:
            - "subscribers": The count of subreddit subscribers.
            - "top_submission_link": URL of the top submission.
            - "sentiment_count": A dictionary with sentiment labels as keys and their counts as values.
            - "submissions": A list of submission texts.
    """

    submissions, sentiment_count = process_submissions(subreddit)

    return {
        "subscribers": get_subreddit_subscriber_count(
            st.session_state.connection, subreddit
        ),
        "top_submission_link": get_top_submission_url(
            st.session_state.connection, subreddit
        ),
        "sentiment_count": sentiment_count,
        "submissions": submissions,
    }


def get_posts_dashboard_data(submission_url: str) -> Dict:
    """
    Retrieves and processes dashboard data for a given post submission.
    This function processes the comments associated with a submission and combines
    metrics into a dashboard data dictionary. It retrieves:
    - The submission score.
    - The comments associated with the submission.
    - Sentiment analysis counts for the comments.
    Parameters:
        submission_url (str): The URL identifier for the submission.
    Returns:
        dict: A dictionary containing:
            - "score": The submission score.
            - "comments": A list of the comments text.
            - "sentiment_count": A dictionary with sentiment labels as keys and their counts as values.
    """

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
    """
    Processes text submissions from a given subreddit by cleaning the text and analyzing its sentiment.
    Parameters:
        subreddit (str): The name of the subreddit from which submissions are fetched.
    Returns:
        - A list of cleaned submission texts.
        - A dictionary with sentiment labels as keys and their counts as values.
    """

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
