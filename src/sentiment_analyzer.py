import re
from transformers import (
    TFAutoModelForSequenceClassification,
    AutoTokenizer,
    TextClassificationPipeline,
)

import settings


def initialize_analyzer() -> TextClassificationPipeline:
    model_name = settings.TEXT_CLASSIFICATION_MODEL

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

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


def analyze_sentiment(analyzer: TextClassificationPipeline, text: str) -> str:
    return analyzer(text)[0]["label"]
