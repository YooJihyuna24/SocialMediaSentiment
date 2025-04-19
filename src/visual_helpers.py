import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from wordcloud import WordCloud, STOPWORDS
from typing import List
import string
import re


def create_wordcloud(text_list: List[str]) -> Figure:
    """
    Create and return a word cloud figure based on a list of text strings.

    Parameters:
        text_list (List[str]): A list of strings to generate the word cloud from.

    Returns:
        Figure: A matplotlib Figure containing the generated word cloud.
    """

    STOPWORDS.update(string.ascii_letters)
    text = "".join(text_list)
    wordcloud = WordCloud(
        width=700, height=300, background_color="white", stopwords=STOPWORDS
    ).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig


def get_reddit_embed_url(post_url: str) -> str:
    """
    Generate an embeddable URL for a given Reddit post URL.
    Parameters:
        post_url (str): The original Reddit post URL.
    Returns:
        str: An embeddable URL formatted to be used for embedding the Reddit post.
    Raises:
        ValueError: If the post_url does not match the expected Reddit post pattern.
    """

    match = re.search(r"(\/r\/[^\/]+\/comments\/[^\/]+)", post_url)
    if not match:
        raise ValueError("Invalid Reddit post URL")

    embed_path = match.group(1)
    embed_url = (
        f"https://www.redditmedia.com{embed_path}?ref_source=embed&ref=share&embed=true"
    )

    return embed_url
