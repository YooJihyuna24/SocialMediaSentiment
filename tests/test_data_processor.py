import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from data_processor import DataProcessor


def test_get_subreddit_dashboard_data_structure():
    processor = DataProcessor("Standard")
    data = processor.get_subreddit_dashboard_data("wallstreetbets", 5)
    assert isinstance(data, dict)
    assert "sentiment_count" in data
    assert "subscribers" in data
    assert "top_submission_link" in data
    assert isinstance(data["sentiment_count"], dict)
