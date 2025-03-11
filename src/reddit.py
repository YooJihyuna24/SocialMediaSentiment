from typing import Iterator
from praw import Reddit
from praw.models import Submission


def initialize_reddit_api(client_id: str, client_secret: str) -> Reddit:
    connection = Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="reddit_bot",
    )
    return connection


def get_hot_submissions(
    connection: Reddit, subreddit: str, count: int
) -> Iterator[Submission]:
    return connection.subreddit(subreddit).hot(limit=count)
