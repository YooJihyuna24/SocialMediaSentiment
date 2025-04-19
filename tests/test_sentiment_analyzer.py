import sentiment_analyzer


def test_clean_up_text():
    text = "Check this out https://example.com @user"
    cleaned_text = sentiment_analyzer.clean_up_text(text)
    assert cleaned_text == "Check this out"

    text_no_mentions = "Hello world!"
    cleaned_text_no_mentions = sentiment_analyzer.clean_up_text(text_no_mentions)
    assert cleaned_text_no_mentions == "Hello world!"
