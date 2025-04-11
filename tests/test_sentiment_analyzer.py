import pytest
import sentiment_analyzer
from transformers import TextClassificationPipeline
from unittest.mock import patch, Mock, MagicMock


def test_clean_up_text():
    # Test mit einem Text, der Links und Erwähnungen enthält
    text = "Check this out https://example.com @user"
    cleaned_text = sentiment_analyzer.clean_up_text(text)
    
    # Überprüfen, ob der Text korrekt bereinigt wurde
    assert cleaned_text == "Check this out"
    
    # Test mit einem Text ohne Links oder Erwähnungen
    text_no_mentions = "Hello world!"
    cleaned_text_no_mentions = sentiment_analyzer.clean_up_text(text_no_mentions)
    assert cleaned_text_no_mentions == "Hello world!"

def test_analyze_sentiment():
    # Mocking der Pipeline
    mock_pipeline = Mock()
    mock_pipeline.return_value = [{"label": "POSITIVE"}]
    
    # Testen mit positivem Text
    sentiment = sentiment_analyzer.analyze_sentiment(mock_pipeline, "I love this!")
    assert sentiment == "POSITIVE"
    
    # Testen mit leerem Text (sollte Fehler zurückgeben)
    mock_pipeline.side_effect = Exception("Error")
    sentiment = sentiment_analyzer.analyze_sentiment(mock_pipeline, "")
    assert sentiment == "ERROR: Error"
