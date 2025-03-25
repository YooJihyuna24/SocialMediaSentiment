from typing import Dict
from matplotlib.figure import Figure
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import data_processor


# DataProcessor erstellen
processor = data_processor.DataProcessor()

dashboard_data = processor.fetch_and_process_data("wallstreetbets")


class SubredditDashboard:
    def __init__(self, subreddit: str):
        self.subreddit = subreddit

    @staticmethod
    def create_wordcloud(text_data: str) -> Figure:
        wordcloud = WordCloud(width=400, height=400, background_color="white").generate(text_data)
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        return fig

    @staticmethod
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

    @staticmethod
    def create_pie_chart(sentiment_count: Dict) -> Figure:
        fig = px.pie(
            names=sentiment_count.keys(),
            values=sentiment_count.values(),
            title="🥧 Sentiment-Verteilung",
            width=400,
            height=400,
        )
        return fig


# Streamlit UI
st.markdown("<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>", unsafe_allow_html=True)

subreddit_name = st.text_input("Subreddit auswählen", "wallstreetbets")

if st.button("📊 Daten abrufen"):
    # Daten abrufen
    submissions = processor.fetch_and_process_data(subreddit_name)
    sentiment_results = processor.analyze_sentiment(submissions)
    kpis = processor.aggregate_kpis(submissions, sentiment_results)
    dashboard_data = processor.prepare_dashboard_data(submissions, sentiment_results)

    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="👥 Anzahl der Beiträge", value=kpis["total_posts"])
        st.pyplot(SubredditDashboard.create_wordcloud(" ".join(submissions)), use_container_width=True)

    with col2:
        st.metric(label="🔥 Positive Posts", value=kpis["positive"])
        st.plotly_chart(SubredditDashboard.create_line_chart(dashboard_data), use_container_width=True)

    with col3:
        st.metric(label="📝 Sentiment-Verteilung", value="Analyzed")
        st.plotly_chart(SubredditDashboard.create_pie_chart(kpis), use_container_width=True)
