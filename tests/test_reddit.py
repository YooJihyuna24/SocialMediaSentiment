import pytest
from unittest.mock import MagicMock
from reddit import (
    get_subreddit_user_count,
    get_top_submission_url,
)

# Gemeinsame Fixture für Reddit-Mock
@pytest.fixture
def mock_connection():
    # Submission Mock
    submission_mock = MagicMock()
    submission_mock.title = "Test Title"
    submission_mock.permalink = "/r/test/comments/abc123/test_post"

    # Subreddit Mock
    subreddit_mock = MagicMock()
    subreddit_mock.hot.return_value = [submission_mock]
    subreddit_mock.new.return_value = [submission_mock]
    subreddit_mock.top.return_value = iter([submission_mock])
    subreddit_mock.rising.return_value = [submission_mock]
    subreddit_mock.subscribers = 123456

    # Reddit Connection Mock
    reddit_mock = MagicMock()
    reddit_mock.subreddit.return_value = subreddit_mock

    return reddit_mock

def test_get_subreddit_user_count(mock_connection):
    count = get_subreddit_user_count(mock_connection, "test")
    
    assert isinstance(count, int)
    assert count == 123456

def test_get_top_submission_url(mock_connection):
    url = get_top_submission_url(mock_connection, "test")

    assert isinstance(url, str)
    assert url.startswith("https://reddit.com/r/test/comments/abc123")
