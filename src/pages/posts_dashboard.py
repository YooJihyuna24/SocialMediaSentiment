import streamlit as st
import plotly.express as px

from data_processor import get_posts_dashboard_data
from visual_helpers import create_wordcloud

st.title("Posts Dashboard")


url = st.text_input("Submission URL", "")

if url:
    with st.spinner():
        try:
            data = get_posts_dashboard_data(url)
        except Exception as e:
            st.error(f"Error fetching posts data: {str(e)} Try checking your input.")
        else:
            st.plotly_chart(
                px.pie(
                    names=data["sentiment_count"].keys(),
                    values=data["sentiment_count"].values(),
                    title="Sentiment",
                ),
                use_container_width=True,
            )
            st.pyplot(create_wordcloud(data["comments"]))
