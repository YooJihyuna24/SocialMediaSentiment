from matplotlib.figure import Figure
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import data_processor
import string
import re


def create_wordcloud(text_data: str) -> Figure:
    STOPWORDS.update(string.ascii_letters)

    wordcloud = WordCloud(
        width=700,
        height=200,
        background_color="white",
        stopwords=STOPWORDS
        ).generate(text_data)
    
    fig, ax = plt.subplots(figsize=(7, 2))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig


def get_reddit_embed_iframe(post_url: str) -> str:

    match = re.search(r"(\/r\/[^\/]+\/comments\/[^\/]+)", post_url)
    if not match:
        raise ValueError("Invalid Reddit post URL")

    embed_path = match.group(1)
    embed_url = (
        f"https://www.redditmedia.com{embed_path}?ref_source=embed&ref=share&embed=true"
    )

    return components.iframe(embed_url, width = 500, height = 300, scrolling = True)

processor = data_processor.DataProcessor()

st.markdown(
    "<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>",
    unsafe_allow_html=True,
)

subreddit_name = st.text_input("Subreddit", "wallstreetbets")

dashboard_data = processor.get_dashboard_data(subreddit_name)

col1, col2 = st.columns([1, 2])


with col1:
    st.metric(label="👥 Subscribers", value=dashboard_data["subscribers"])

    get_reddit_embed_iframe(dashboard_data["top_submission_link"])

with col2:
    st.plotly_chart(
        px.pie(
            names=dashboard_data["sentiment_count"].keys(),
            values=dashboard_data["sentiment_count"].values(),
            title="Sentiment of recent submissions",
        ),
        use_container_width=True,
    )

st.pyplot(
    create_wordcloud(" ".join(dashboard_data["submissions"])),
    use_container_width=True,
)
