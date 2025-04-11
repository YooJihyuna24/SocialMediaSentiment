import streamlit as st
import plotly.express as px
from data_processor import DataProcessor
from visual_helpers import create_wordcloud


processor = DataProcessor()


st.markdown(
    "<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>",
    unsafe_allow_html=True,
)

subreddit_name = st.text_input("Subreddit", "wallstreetbets")

dashboard_data = processor.get_subreddit_dashboard_data(subreddit_name)

col1, col2 = st.columns([1, 2])


with col1:
    st.metric(label="👥 Subscribers", value=dashboard_data["subscribers"])
    st.link_button(
        url=dashboard_data["top_submission_link"],
        label="Top reddit post",
        icon="🔥",
    )

with col2:
    st.pyplot(
        create_wordcloud(dashboard_data["submissions"]),
    )


st.plotly_chart(
    px.pie(
        names=dashboard_data["sentiment_count"].keys(),
        values=dashboard_data["sentiment_count"].values(),
        title="Sentiment of recent submissions",
    ),
    use_container_width=True,
)
