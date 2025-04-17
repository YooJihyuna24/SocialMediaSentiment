import streamlit as st
import plotly.express as px

from data_processor import get_subreddit_dashboard_data
from visual_helpers import create_wordcloud, get_reddit_embed_url
import streamlit.components.v1 as components
import plotly.express as px


st.title("Subreddit Dashboard")


subreddit_name = st.text_input("Subreddit", "wallstreetbets")

if subreddit_name:
    with st.spinner():
        dashboard_data = get_subreddit_dashboard_data(subreddit_name)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(label="👥 Subscribers", value=dashboard_data["subscribers"])

            embed_url = get_reddit_embed_url(dashboard_data["top_submission_link"])
            components.iframe(embed_url, width=500, height=300, scrolling=True)

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
