import streamlit as st
import plotly.express as px
from data_processor import DataProcessor
from visual_helpers import create_wordcloud
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
import re


def get_reddit_embed_iframe(post_url: str) -> str:
    match = re.search(r"(\/r\/[^\/]+\/comments\/[^\/]+)", post_url)
    if not match:
        raise ValueError("Invalid Reddit post URL")

    embed_path = match.group(1)
    embed_url = (
        f"https://www.redditmedia.com{embed_path}?ref_source=embed&ref=share&embed=true"
    )

    return components.iframe(embed_url, width=500, height=300, scrolling=True)


st.markdown(
    "<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>",
    unsafe_allow_html=True,
)

with st.sidebar:
    selected_model = st.pills(
        "Model", ["Standard", "Political"], selection_mode="single", default="Standard"
    )
    submissions_count = st.select_slider(
        "Number of submissions", options=range(1, 101), value=10
    )

processor = DataProcessor(selected_model)
subreddit_name = st.text_input("Subreddit", "wallstreetbets")

dashboard_data = processor.get_subreddit_dashboard_data(
    subreddit_name, submissions_count
)

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
    create_wordcloud(dashboard_data["submissions"]),
)
