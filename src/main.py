import streamlit as st

from models import models
from data_processor import initialize_reddit_connection, initialize_sentiment_pipelines

st.logo("Logo1.png")

initialize_sentiment_pipelines()
initialize_reddit_connection()

with st.sidebar:
    st.session_state.selected_model = st.pills(
        "model",
        models.keys(),
        selection_mode="single",
        default="standard",
    )

    st.session_state.filter_mode = st.pills(
        "filter",
        ["hot", "top", "new", "rising"],
        selection_mode="single",
        default="hot",
    )

    st.session_state.submission_count = st.select_slider(
        "number of submissions",
        options=range(1, 101),
        value=10,
    )

pg = st.navigation(
    [
        st.Page("pages/subreddit_dashboard.py", title="Subreddit Dashboard"),
        st.Page("pages/posts_dashboard.py", title="Posts Dashboard"),
    ]
)
pg.run()
