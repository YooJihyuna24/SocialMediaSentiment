import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from data_processor import get_posts_dashboard_data
from visual_helpers import create_wordcloud, get_reddit_embed_url

st.title("Posts Dashboard")


url = st.text_input("Submission URL", "")

if url:
    with st.spinner():
        try:
            data = get_posts_dashboard_data(url)
        except Exception as e:
            st.error(f"Error fetching posts data: {str(e)} Try checking your input.")
        else:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(label="⬆️ Score", value=data["score"])

                embed_url = get_reddit_embed_url(url)
                components.iframe(embed_url, width=500, height=300, scrolling=True)

            with col2:
                st.plotly_chart(
                    px.pie(
                        names=data["sentiment_count"].keys(),
                        values=data["sentiment_count"].values(),
                        title="Sentiment",
                    ),
                    use_container_width=True,
                )

            st.pyplot(create_wordcloud(data["comments"]))
