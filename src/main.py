import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.logo("Logo1.png")

pg = st.navigation(
    [
        st.Page("pages/subreddit_dashboard.py", title="Subreddit Dashboard"),
        st.Page("pages/posts_dashboard.py", title="Posts Dashboard"),
    ]
)
pg.run()
