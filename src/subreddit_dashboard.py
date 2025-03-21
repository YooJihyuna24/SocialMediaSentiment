from typing import Dict
from matplotlib.figure import Figure
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

import mock_data


def create_wordcloud(text_data: str) -> Figure:
    wordcloud = WordCloud(width=400, height=400, background_color="white").generate(
        text_data
    )
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<h3 style="font-size:16px; font-family: Source Sans Pro;"><b>☁️ Wordcloud</b></h3>',
        unsafe_allow_html=True,
    )

    return fig


def create_line_chart(sentiment_over_time: Dict):
    fig = px.line(
        x=sentiment_over_time["dates"],
        y=sentiment_over_time["sentiment"],
        title="📈 Sentiment über Zeit",
        labels={"x": "Datum", "y": "Sentiment"},
        width=400,
        height=400,
    )
    return fig


def create_pie_chart(sentiment_count: Dict):
    fig = px.pie(
        names=sentiment_count.keys(),
        values=sentiment_count.values(),
        title="🥧 Sentiment-Verteilung",
        width=400,
        height=400,
    )
    return fig


st.markdown(
    "<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>",
    unsafe_allow_html=True,
)

subreddit = st.text_input("Subreddit auswählen", mock_data.subreddit_name)

st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="👥 Anzahl der Mitglieder", value="120K")
    st.pyplot(create_wordcloud(mock_data.text_data))

with col2:
    st.metric(label="🔥 Aktive Nutzer", value="5.2K")
    st.plotly_chart(
        create_line_chart(mock_data.sentiment_over_time), use_container_width=True
    )

with col3:
    st.metric(label="📝 Posts pro Tag", value="320")
    st.plotly_chart(
        create_pie_chart(mock_data.sentiment_count), use_container_width=True
    )

