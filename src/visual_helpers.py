import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from wordcloud import WordCloud, STOPWORDS
from typing import List
import string


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
