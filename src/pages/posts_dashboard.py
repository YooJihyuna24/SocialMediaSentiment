import streamlit as st
from data_processor import DataProcessor
import plotly.express as px
from visual_helpers import create_wordcloud

st.title("Posts Dashboard")

processor = DataProcessor("Standard")

url = st.text_input("Reddit-Post-URL eingeben:", "")
limit = st.slider("Wie viele Kommentare sollen analysiert werden?", 10, 100, 30)

if url:
    df = processor.get_posts_dashboard_data(url, limit=limit)
    st.subheader("📊 Sentiment-Verteilung der Kommentare")

    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]

    st.plotly_chart(
        px.pie(
            sentiment_counts,
            names="sentiment",
            values="count",
            title="Sentiment-Auswertung der Kommentare",
        ),
        use_container_width=True,
    )

    st.subheader("WordCloud der Kommentare")

    st.pyplot(create_wordcloud(df["comment"]))

    st.dataframe(df)
