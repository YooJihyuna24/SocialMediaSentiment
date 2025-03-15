from typing import List, Literal
from praw import Reddit
from praw.models import Submission

import settings


def initialize_reddit_api(client_id: str, client_secret: str) -> Reddit:
    connection = Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="reddit_bot",
    )
    return connection


def get_submissions_text(
    connection: Reddit,
    subreddit: str,
    type: Literal["hot", "top", "new", "rising"],
    count: int = settings.SUBMISSION_COUNT,
) -> List[Submission]:
    match type:
        case "hot":
            submissions = connection.subreddit(subreddit).hot(limit=count)
        case "new":
            submissions = connection.subreddit(subreddit).new(limit=count)
        case "top":
            submissions = connection.subreddit(subreddit).top(limit=count)
        case "rising":
            submissions = connection.subreddit(subreddit).rising(limit=count)
    return [submission.title + submission.selftext for submission in submissions]


def get_subreddit_user_count(
    connection: Reddit,
    subreddit: str,
) -> int:
    return connection.subreddit(subreddit).subscribers
