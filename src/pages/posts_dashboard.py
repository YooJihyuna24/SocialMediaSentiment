import streamlit as st
import plotly.express as px

from data_processor import get_posts_dashboard_data
from visual_helpers import create_wordcloud

st.title("Posts Dashboard")


url = st.text_input("Submission URL", "")

if url:
    with st.spinner():
        data = get_posts_dashboard_data(url)

        st.plotly_chart(
            px.pie(
                names=data["sentiment_count"].keys(),
                values=data["sentiment_count"].values(),
                title="Sentiment",
            ),
            use_container_width=True,
        )

        st.pyplot(create_wordcloud(data["comments"]))
