import streamlit as st
from utils import *


st.set_page_config(page_title="HR Assistant", page_icon='robot')
st.header("Resume Screening Assistant")
st.write("**Let me find the perfect match for your requirements.**")

requirements = st.text_area("Share the job requirements")
no_of_job_openings = st.slider("How many matches are you looking for?", 1,3,1)

with st.sidebar:
    st.subheader("Upload Resumes:")
    resume_folder = st.text_input("Path to resumes folder", value="C:/Users/AB263004/Downloads/RAG_HR_Resumes_Dump")
    uploaded_files = st.file_uploader("Upload resumes (PDF Only)", type=["pdf"], accept_multiple_files=True)

Submit = st.button("Assist me")

if Submit:
    with st.spinner("Wait for it..."):

        response = process(resume_folder, uploaded_files, requirements, no_of_job_openings)
        st.write(response)
