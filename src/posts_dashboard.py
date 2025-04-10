import streamlit as st
import data_processor


st.markdown(
    "<h1 style='text-align: center;'>📊 Posts Dashboard</h1>",
    unsafe_allow_html=True,
)

submission_name = st.text_input("Submission", placeholder="Enter submission URL")

processor = data_processor.DataProcessor()