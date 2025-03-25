import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

pg = st.navigation(
    [
        st.Page("subreddit_dashboard.py", title="Subreddit Dashboard"),
        st.Page("posts_dashboard.py", title="Posts Dashboard"),
    ]
)
pg.run()
