from typing import Dict
from matplotlib.figure import Figure
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import data_processor


def create_wordcloud(text_data: str) -> Figure:
    wordcloud = WordCloud(width=400, height=400, background_color="white").generate(
        text_data
    )
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig


def create_line_chart(sentiment_over_time: Dict) -> Figure:
    fig = px.line(
        x=sentiment_over_time["dates"],
        y=sentiment_over_time["sentiment"],
        title="📈 Sentiment über Zeit",
        labels={"x": "Datum", "y": "Sentiment"},
        width=400,
        height=400,
    )
    return fig


def create_pie_chart(sentiment_count: Dict[str, int]) -> Figure:
    fig = px.pie(
        names=sentiment_count.keys(),
        values=sentiment_count.values(),
        title="🥧 Sentiment-Verteilung",
        width=400,
        height=400,
    )
    return fig


processor = data_processor.DataProcessor()


st.markdown(
    "<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>",
    unsafe_allow_html=True,
)

subreddit_name = st.text_input("Subreddit", "wallstreetbets")

with st.spinner("Fetching reddit submissions and classifying by sentiment..."):
    dashboard_data = processor.get_dashboard_data(subreddit_name)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="👥 Subreddit Subscribers", value=dashboard_data["subscribers"])
##        st.pyplot(
##           create_wordcloud(" ".join(dashboard_data["common_words"])),
##          use_container_width=True,
##     )

with col2:
    st.plotly_chart(
        create_pie_chart(dashboard_data["sentiment_count"]),
        use_container_width=True,
    )

with col3:
    st.link_button(label="🔥 Top post", url=dashboard_data["top_submission_link"])
