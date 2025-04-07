from matplotlib.figure import Figure
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import data_processor
import string

def create_wordcloud(text_data: str) -> Figure:
    stop_words =  set(STOPWORDS).union(set(string.ascii_letters))
    additional_stopwords = ["html","https","com","www","reddit","r","reddit.com","reddit.com/r",]
    stop_words.update(additional_stopwords)

    wordcloud = WordCloud(
        width=700,
        height=200,
        background_color="white",
        stopwords=stop_words
        ).generate(text_data)
    
    fig, ax = plt.subplots(figsize=(7, 2))
    ax.imshow(wordcloud, interpolation="bilinear")
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
    st.link_button(
        url=dashboard_data["top_submission_link"],
        label="Top reddit post",
        icon="🔥",
    )
    
with col2:
    st.pyplot(
        create_wordcloud(" ".join(dashboard_data["submissions"])),
        use_container_width=True,
    )


st.plotly_chart(
    px.pie(
        names=dashboard_data["sentiment_count"].keys(),
        values=dashboard_data["sentiment_count"].values(),
        title="Sentiment of recent submissions",
    ),
    use_container_width=True,
)
