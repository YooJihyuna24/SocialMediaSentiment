import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

subreddit_name = "MachineLearning"
total_users = 200_000
active_users = 5_000
total_posts = 10_000

sentiment_over_time = {
                    "dates": ["2024-03-10", "2024-03-11", "2024-03-12"],
                    "sentiment": [0.1, -0.2, 0.4]
                    }
sentiment_count = {"Positive": 50, "Neutral": 30, "Negative": 20}
text_data = "Machine Learning AI Data Science Deep Learning Python NLP"

def create_wordcloud(text_data):
    wordcloud = WordCloud(width=400, height=400, background_color="white").generate(text_data)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.markdown(
    '<h3 style="font-size:16px; font-family: Source Sans Pro;"><b>☁️ Wordcloud</b></h3>', 
    unsafe_allow_html=True
    )

    return fig

def create_line_chart(sentiment_over_time):
    fig = px.line(
                x=sentiment_over_time["dates"], 
                y=sentiment_over_time["sentiment"], 
                title="📈 Sentiment über Zeit",
                labels={"x": "Datum", "y": "Sentiment"},
                width=400, height=400)
    return fig

def create_pie_chart(sentiment_count):
    fig = px.pie(
                names=sentiment_count.keys(), 
                values=sentiment_count.values(), 
                title="🥧 Sentiment-Verteilung",
                width=400, height=400)
    return fig

def page_subreddit_dashboard():
    st.markdown(
        "<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>",
        unsafe_allow_html=True
        )
    
    subreddit = st.text_input("Subreddit auswählen", subreddit_name)
    
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="👥 Anzahl der Mitglieder", value="120K")

    with col2:
        st.metric(label="🔥 Aktive Nutzer", value="5.2K")

    with col3:
        st.metric(label="📝 Posts pro Tag", value="320")

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.pyplot(create_wordcloud(text_data))

    with col2:
        st.plotly_chart(create_line_chart(sentiment_over_time), use_container_width=True)

    with col3:
        st.plotly_chart(create_pie_chart(sentiment_count), use_container_width=True)

page_subreddit_dashboard()