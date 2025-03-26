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


def test_classify_very_long_text():
    # this test should verify that the pipeline correctly truncates the text
    # and does not run into token index errors
    pipeline = create_sentiment_pipeline(
        "bhadresh-savani/distilbert-base-uncased-emotion"
    )

    # generated by chatGPT
    text = """
    I have always been fascinated by the way human emotions manifest in written text. Words have an incredible power to convey joy, sorrow, excitement, and despair, often in ways that transcend simple definitions. Consider, for example, a heartfelt letter from a soldier to his family, written during a time of war. The words on the page might express longing, love, and hope, even as they are overshadowed by the grim realities of conflict. Similarly, a passionate review of a long-awaited book or film can overflow with enthusiasm, capturing the writer's intense emotional response to the experience.

    But not all emotions are so straightforward. Sometimes, language becomes a tangled web of conflicting sentiments, making it difficult to discern the author's true feelings. Sarcasm, for instance, is a prime example of how words can mean the opposite of what they seem to say. 'Oh great, another delay in my flight. Just what I needed today!' The surface words suggest enthusiasm, but the sentiment is clearly one of frustration. This complexity makes sentiment analysis a challenging yet fascinating field, requiring sophisticated models that can capture subtle nuances in meaning.

    Beyond individual sentences, sentiment can also evolve over the course of a longer text. A personal blog post might begin with a sense of optimism, gradually shift into frustration, and end with a feeling of resignation. A product review could start with excitement over a new purchase, only to reveal disappointment as flaws become apparent. These fluctuations pose unique challenges for sentiment analysis models, which must determine whether to assign an overall sentiment score or recognize multiple emotional shifts within the same text.

    To handle such variations effectively, sentiment analysis algorithms must consider not only the words themselves but also their context. Consider the phrase 'This is unbelievable!' Standing alone, it could express either amazement or disbelief. Only by examining the surrounding text can we determine whether the sentiment is positive or negative. This need for contextual understanding is why deep learning approaches, particularly transformer-based models like BERT, have revolutionized the field. By capturing relationships between words across long passages, these models can interpret sentiment with greater accuracy than earlier methods, which relied solely on word counts or simple polarity measures.

    However, despite these advances, sentiment analysis still faces limitations, especially when dealing with lengthy texts. Tokenization and truncation introduce practical constraints, as most NLP models have a maximum input length. This raises important questions: How much of a long text should be analyzed? Does truncating the input distort the sentiment? If a review starts with praise but ends with criticism, does truncating the latter portion misrepresent the overall sentiment? These are the challenges developers and researchers must address when designing robust sentiment analysis systems.

    Ultimately, sentiment analysis is more than just a technical problem; it is an exploration of human expression. Whether analyzing customer feedback, social media posts, or literature, the goal remains the same: to understand the emotions embedded in language. As models continue to improve, they bring us closer to this understanding, but there will always be new complexities to unravel. After all, language is fluid, evolving, and deeply tied to human experience—a reality that no algorithm can ever fully capture.
    """
    analyze_sentiment(pipeline, text)
