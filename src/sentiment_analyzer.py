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
        max_length=tokenizer.model_max_length,
    )


def analyze_sentiment(analyzer: TextClassificationPipeline, text: str) -> str:
    return analyzer(text)[0]["label"]
