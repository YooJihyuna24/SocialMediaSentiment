from typing import List, Literal

import streamlit as st
from praw import Reddit
from praw.exceptions import InvalidURL
from prawcore.exceptions import NotFound


@st.cache_resource
def create_reddit_connection(client_id: str, client_secret: str) -> Reddit:
    """
    Creates and returns a Reddit connection using the credentials.
    Parameters:
        client_id (str): The client ID for the Reddit API.
        client_secret (str): The client secret key for the Reddit API.
    Returns:
        Reddit: An authenticated Reddit instance.
    """
    connection = Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="reddit_bot",
    )
    return connection


def handle_subreddit_not_found(func):
    """
    Decorator to handle NotFound errors for subreddit-related functions
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            raise ValueError("The subreddit was not found.")

    return wrapper


def handle_submission_not_found(func):
    """
    Decorator to handle InvalidURL and NotFound errors for submission-related functions
    Raises:
        ValueError: If the submission URL is not valid or the submission was not found.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidURL:
            raise ValueError("The submission URL is not valid.")
        except NotFound:
            raise ValueError("The submission was not found.")

    return wrapper


@handle_subreddit_not_found
@st.cache_data
def get_submissions_text(
    _connection: Reddit,
    subreddit: str,
    submission_type: Literal["hot", "top", "new", "rising"],
    submission_count: int,
) -> List[str]:
    """
    Fetch submissions text from a subreddit using a given submission type.
    Parameters:
        _connection (Reddit): The Reddit API connection.
        subreddit (str): The name of the subreddit.
        submission_type (Literal["hot", "top", "new", "rising"]): The type of submissions to fetch.
        submissions_count (int): The number of submissions to fetch.
    Returns:
        List[str]: A list of strings where each string contains the title and selftext of a submission,
                   separated by a newline.
    """
    match submission_type:
        case "hot":
            submissions = _connection.subreddit(subreddit).hot(limit=submission_count)
        case "new":
            submissions = _connection.subreddit(subreddit).new(limit=submission_count)
        case "top":
            submissions = _connection.subreddit(subreddit).top(limit=submission_count)
        case "rising":
            submissions = _connection.subreddit(subreddit).rising(
                limit=submission_count
            )

    return [submission.title + "\n" + submission.selftext for submission in submissions]


@handle_subreddit_not_found
@st.cache_data
def get_subreddit_subscriber_count(
    _connection: Reddit,
    subreddit: str,
) -> int:
    """
    Return the number of subscribers for a given subreddit.
    Parameters:
        _connection (Reddit): The Reddit API connection.
        subreddit (str): The name of the subreddit.
    Returns:
        int: The subscriber count of subreddit.
    """
    return _connection.subreddit(subreddit).subscribers


@handle_subreddit_not_found
@st.cache_data
def get_top_submission_url(_connection: Reddit, subreddit: str) -> str:
    """
    Return the URL of the top submission in the subreddit over the past week.
    Parameters:
        _connection (Reddit): The Reddit API connection.
        subreddit (str): The name of the subreddit.
    Returns:
        str: A full URL linking to the top submission on reddit.com.
    """
    return (
        "https://reddit.com"
        + next(
            _connection.subreddit(subreddit).top(limit=1, time_filter="week")
        ).permalink
    )


@handle_submission_not_found
@st.cache_data
def get_comments_text(
    _connection: Reddit,
    submission_url: str,
    submission_count: int,
) -> List[str]:
    """
    Fetches comment texts from a Reddit submission.
    Parameters:
        _connection (Reddit): The Reddit API connection.
        submission_url (str): The URL of the Reddit submission.
        submission_count (int): The number of comments to fetch.
    Returns:
        List[str]: A list of comment texts from the submission.
    """
    submission = _connection.submission(url=submission_url)
    submission.comments.replace_more(limit=0)
    return [comment.body for comment in submission.comments[:submission_count]]


@handle_submission_not_found
@st.cache_data
def get_submission_score(
    _connection: Reddit,
    submission_url: str,
) -> int:
    """
    Retrieve the score of a Reddit submission.
    Parameters:
        _connection (Reddit): The Reddit API connection.
        submission_url (str): The URL of the Reddit submission.
    Returns:
        int: The score (upvotes minus downvotes) of the Reddit submission.
    """
    submission = _connection.submission(url=submission_url)
    return submission.score
