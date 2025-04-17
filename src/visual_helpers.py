import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from wordcloud import WordCloud, STOPWORDS
from typing import List
import string
import re


def create_wordcloud(text_list: List[str]) -> Figure:
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
    match = re.search(r"(\/r\/[^\/]+\/comments\/[^\/]+)", post_url)
    if not match:
        raise ValueError("Invalid Reddit post URL")

    embed_path = match.group(1)
    embed_url = (
        f"https://www.redditmedia.com{embed_path}?ref_source=embed&ref=share&embed=true"
    )

    return embed_url
