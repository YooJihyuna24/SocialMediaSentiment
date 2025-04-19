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
    Retrieves a text classification model from Hugging Face and returns a pipeline
    Parameters:
        model_name (str): The name of the model to load.
    Returns:
        TextClassificationPipeline: A pipeline for text classification.
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
    Removes links and mentions from the text.
    Parameters:
        text (str): The input string to clean.
    Returns:
        str: The cleaned string with links and mentions removed.
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
    Analyzes sentiment of the given text using the pipeline.
    Parameters:
        pipeline (TextClassificationPipeline): The sentiment analysis pipeline.
        text (str): The input string to analyze.
    Returns:
        str: The sentiment label of the text.
    Raises:
        RuntimeError: If an error occurs during sentiment analysis.
    """
    try:
        result = pipeline(text)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]["label"]
        else:
            return "Unknown"
    except Exception:
        raise RuntimeError("An error occurred while analyzing sentiment.")
