from sentiment_analyzer import (
    analyze_sentiment,
    clean_up_text,
    create_sentiment_pipeline,
)


def test_clean_text():
    text = "This is my dirty string: https://mywebsite.com. @you Hope you didn't see that website."
    expected = "This is my dirty string: Hope you didn't see that website."
    result = clean_up_text(text)

    assert result == expected


def test_classify_text():
    pipeline = create_sentiment_pipeline(
        "bhadresh-savani/distilbert-base-uncased-emotion"
    )
    text = "I love it"
    expected = "love"

    result = analyze_sentiment(pipeline, text)
    assert result == expected

    text = "I'm so sad"
    expected = "sadness"

    result = analyze_sentiment(pipeline, text)

    assert result == expected
