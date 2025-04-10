import streamlit as st
from data_processor import DataProcessor
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt




def show_sentiment_dashboard(df):
    st.subheader("📊 Sentiment-Verteilung der Kommentare")

    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]

    st.plotly_chart(
        px.pie(
            sentiment_counts,
            names="sentiment",
            values="count",
            title="Sentiment-Auswertung der Kommentare"
        ),
        use_container_width=True
    )

    st.subheader("WordCloud der Kommentare")
    wordcloud = WordCloud(width=700, height=300, background_color="white").generate(" ".join(df["comment"]))
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    st.subheader("📝 Einzelne Kommentare")
    for _, row in df.iterrows():
        st.markdown(f"**{row['sentiment']}**: {row['comment']}")


def page_posts_dashboard():
    st.title("Posts Dashboard")
    st.write("Hier werden individuelle Post-Analysen angezeigt.")

    processor = DataProcessor()

    url = st.text_input("Reddit-Post-URL eingeben:","")
    limit = st.slider("Wie viele Kommentare sollen analysiert werden?", 10, 100, 30)

    if url:
        with st.spinner("Kommentare werden analysiert..."):
            df = processor.analyze_comments(url, limit=limit)
            show_sentiment_dashboard(df)


page_posts_dashboard()