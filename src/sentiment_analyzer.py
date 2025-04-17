import re
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TextClassificationPipeline,
)
import streamlit as st


@st.cache_resource
def create_sentiment_pipeline(model_name: str) -> TextClassificationPipeline:
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


@st.cache_data(
    hash_funcs={
        TextClassificationPipeline: lambda pipeline: pipeline.model.config._name_or_path
    }
)
def analyze_sentiment(pipeline: TextClassificationPipeline, text: str) -> str:
    """
    Analyzes sentiment of the given text using the pipeline
    :param text: Input string
    :return: Sentiment label
    """
    try:
        result = pipeline(text)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]["label"]
        else:
            return "Unknown"
    except Exception:
        raise RuntimeError("An error occurred while analyzing sentiment.")
