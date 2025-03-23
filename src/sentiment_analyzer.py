import re
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TextClassificationPipeline,
)

import settings


def create_sentiment_pipeline(
    model_name: str = settings.TEXT_CLASSIFICATION_MODEL,
) -> TextClassificationPipeline:
    """
    Retrieves a text classification model from hugging face and returns a pipeline
    :param model_name: Text classification model string name
    :return: Transformers pipeline
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    return TextClassificationPipeline(
        task="text-classification",
        model=model,
        tokenizer=tokenizer,
        truncation=True,
    )


LINKS_PATTERN = re.compile(r"https?://\S+|www\.\S+")
MENTIONS_PATTERN = re.compile(r"@\w+")


def clean_up_text(text: str) -> str:
    """
    Removes links and mentions from the text
    :param text: String to clean up
    :return: Clean string without links and mentions
    """
    text = re.sub(LINKS_PATTERN, "", text)
    text = re.sub(MENTIONS_PATTERN, "", text)

    # after removing links and mentions there is always some whitespace left
    text = " ".join(text.split())
    return text


def analyze_sentiment(pipeline: TextClassificationPipeline, text: str) -> str:
    """
    Analyzes sentiment of the given text using the pipeline
    :param text: Input string
    :return: Sentiment label
    """
    try:
        result = list(pipeline(text))
        return result[0]["label"]
    except Exception as e:
        return f"ERROR: {str(e)}"
