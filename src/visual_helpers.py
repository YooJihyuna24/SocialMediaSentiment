import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from wordcloud import WordCloud
from typing import List


def create_wordcloud(text_list: List[str]) -> Figure:
    text = "".join(text_list)
    wordcloud = WordCloud(width=700, height=300, background_color="white").generate(
        text
    )
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig
