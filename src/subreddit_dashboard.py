from matplotlib.figure import Figure
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import data_processor
import string
import reddit

def create_wordcloud(text_data: str) -> Figure:
    stop_words =  set(STOPWORDS).union(set(string.ascii_letters))
    additional_stopwords = ["html","https","com","www","reddit","r","reddit.com","reddit.com/r",]
    stop_words.update(additional_stopwords)

    wordcloud = WordCloud(
        width=500,
        height=300,
        background_color="white",
        stopwords=stop_words
        ).generate(text_data)
    
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.imshow(wordcloud, interpolation="auto")
    ax.axis("off")
    return fig


processor = data_processor.DataProcessor()

st.markdown(
    "<h1 style='text-align: center;'>📊 Subreddit Dashboard</h1>",
    unsafe_allow_html=True,
)

subreddit_name = st.text_input("Subreddit", "wallstreetbets")

with st.spinner("Fetching reddit submissions and classifying by sentiment..."):
    dashboard_data = processor.get_dashboard_data(subreddit_name)

col1, col2 = st.columns([1, 2])


with col1:
    st.metric(label="👥 Subscribers", value=dashboard_data["subscribers"])
    dashboard_top_submission_url = reddit.get_top_submission_url(
        processor.connection, subreddit_name
    )
    dashboard_embed_iframe = reddit.get_reddit_embed_iframe(
        dashboard_top_submission_url
    )
    st.markdown(dashboard_embed_iframe, unsafe_allow_html=True)    

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
        create_wordcloud(" ".join(dashboard_data["submissions"])),
        use_container_width=True,
    )