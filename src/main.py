import streamlit as st
import dotenv
import os

pg = st.navigation([
    st.Page("subreddit_dashboard.py", title="Subreddit Dashboard"),
    st.Page("posts_dashboard.py", title="Posts Dashboard"),
])
pg.run()