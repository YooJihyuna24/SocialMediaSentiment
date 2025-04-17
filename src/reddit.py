from typing import List, Literal
from praw import Reddit
from prawcore.exceptions import NotFound
from praw.exceptions import InvalidURL
import streamlit as st


@st.cache_resource
def create_reddit_connection(client_id: str, client_secret: str) -> Reddit:
    """
    Initializes the reddit api connection
    :param client_id: Client ID for authentication
    :param client_secret: Secret for authentication
    :return: Reddit connection instance
    """
    connection = Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="reddit_bot",
    )
    return connection


def handle_subreddit_not_found(func):
    """
    Decorator to handle NotFound error from praw and raise a custom error
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            raise ValueError("The subreddit was not found.")

    return wrapper


@handle_subreddit_not_found
@st.cache_data
def get_submissions_text(
    _connection: Reddit,
    subreddit: str,
    submission_type: Literal["hot", "top", "new", "rising"],
    submissions_count: int,
) -> List[str]:
    """
    Fetches submissions from specified subreddit with title and text concatenated
    :param connection: reddit api connection
    :param subreddit: Subreddit to get submissions from
    :param submission_type: Filter on the reddit submission ranking system: "hot", "top", "new" or "rising"
    :param count: Amount of submissions to return
    :return: List of submissions text
    """
    match submission_type:
        case "hot":
            submissions = _connection.subreddit(subreddit).hot(limit=submissions_count)
        case "new":
            submissions = _connection.subreddit(subreddit).new(limit=submissions_count)
        case "top":
            submissions = _connection.subreddit(subreddit).top(limit=submissions_count)
        case "rising":
            submissions = _connection.subreddit(subreddit).rising(
                limit=submissions_count
            )

    return [submission.title + "\n" + submission.selftext for submission in submissions]


@handle_subreddit_not_found
@st.cache_data
def get_subreddit_user_count(
    _connection: Reddit,
    subreddit: str,
) -> int:
    """
    Fetches the amount of subscribers of specified subreddit
    :param connection: reddit api connection
    :param subreddit: Subreddit to get submissions from
    :return: Amount of subreddit subscribers
    """
    return _connection.subreddit(subreddit).subscribers


@handle_subreddit_not_found
@st.cache_data
def get_top_submission_url(_connection: Reddit, subreddit: str) -> str:
    """
    Fetches last week's top submission of the specified subreddit
    :param connection: reddit api connection
    :param subreddit: Subreddit to get submissions from
    :return: URL to the reddit submission
    """
    return (
        "https://reddit.com"
        + next(
            _connection.subreddit(subreddit).top(limit=1, time_filter="week")
        ).permalink
    )


@st.cache_data
def get_comments_text(
    _connection: Reddit,
    submission_url: str,
    submission_count: int,
) -> List[str]:
    """
    Fetches a specified number of comments from a Reddit submission.
    :param _connection: reddit api connection
    :param submission_url: URL of the Reddit post to fetch comments from
    :param limit: Maximum number of comments to return (default: 30)
    :return: List of comment texts (strings)
    """
    try:
        submission = _connection.submission(url=submission_url)
    except InvalidURL:
        raise ValueError("The submission URL is not valid.")
    except NotFound:
        raise ValueError("The submission was not found.")
    submission.comments.replace_more(limit=0)
    return [comment.body for comment in submission.comments[:submission_count]]
