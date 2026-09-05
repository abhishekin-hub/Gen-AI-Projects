import streamlit as st
from utils import *

st.set_page_config(page_title="HR Assistant", page_icon='robot')
st.header("HR-Resume Screening Assistant")
st.subheader("I find perfect match for your requirements")

requirements = st.text_area("Share the job requirements")
no_of_job_openings = st.slider("How many matches are you looking for?", 1,3,1)

with st.sidebar:
    resumes = st.file_uploader("Upload resumes (PDF Only)", type=["pdf"], accept_multiple_files=True)

Submit = st.button("Assist me")

if Submit:
    with st.spinner("Wait for it..."):

        response = process(resumes, requirements, no_of_job_openings)
        st.write(response)