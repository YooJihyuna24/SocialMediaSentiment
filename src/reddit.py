from typing import List, Literal
from praw import Reddit

import settings
import re


def initialize_reddit_api(client_id: str, client_secret: str) -> Reddit:
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


def get_submissions_text(
    connection: Reddit,
    subreddit: str,
    submission_type: Literal["hot", "top", "new", "rising"],
    count: int = settings.SUBMISSION_COUNT,
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
            submissions = connection.subreddit(subreddit).hot(limit=count)
        case "new":
            submissions = connection.subreddit(subreddit).new(limit=count)
        case "top":
            submissions = connection.subreddit(subreddit).top(limit=count)
        case "rising":
            submissions = connection.subreddit(subreddit).rising(limit=count)
    return [submission.title + "\n" + submission.selftext for submission in submissions]


def get_subreddit_user_count(
    connection: Reddit,
    subreddit: str,
) -> int:
    """
    Fetches the amount of subscribers of specified subreddit
    :param connection: reddit api connection
    :param subreddit: Subreddit to get submissions from
    :return: Amount of subreddit subscribers
    """
    return connection.subreddit(subreddit).subscribers


def get_top_submission_url(
    connection: Reddit,
    subreddit: str
) -> str:
    """
    Fetches last week's top submission of the specified subreddit
    :param connection: reddit api connection
    :param subreddit: Subreddit to get submissions from
    :return: URL to the reddit submission
    """
    return (
        "https://reddit.com"
        + next(
            connection.subreddit(subreddit).top(limit=1, time_filter="week")
        ).permalink
    )

def get_top_submission_title(
        connection: Reddit,
        subreddit: str
) -> str:
    return (next(connection.subreddit(subreddit).top(limit=1, time_filter="week")).title)