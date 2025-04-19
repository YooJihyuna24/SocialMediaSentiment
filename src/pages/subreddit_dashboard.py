import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from data_processor import get_subreddit_dashboard_data
from visual_helpers import create_wordcloud, get_reddit_embed_url

st.title("Subreddit Dashboard")


subreddit_name = st.text_input("Subreddit", "wallstreetbets")

if subreddit_name:
    with st.spinner("Fetching subreddit data and classifying submissions..."):
        try:
            data = get_subreddit_dashboard_data(subreddit_name)
        except Exception as e:
            st.error(
                f"Error fetching dashboard data: {str(e)} Try checking your input."
            )
        else:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric(label="👥 Subscribers", value=data["subscribers"])

                embed_url = get_reddit_embed_url(data["top_submission_link"])
                components.iframe(embed_url, width=500, height=300, scrolling=True)

            with col2:
                st.plotly_chart(
                    px.pie(
                        names=data["sentiment_count"].keys(),
                        values=data["sentiment_count"].values(),
                        title="Sentiment of recent submissions",
                    ),
                    use_container_width=True,
                )

            st.pyplot(
                create_wordcloud(data["submissions"]),
            )
