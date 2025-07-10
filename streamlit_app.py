import streamlit as st
import pandas as pd
from models.supervised import SupervisedModel
from utils.resume_parser import extract_text_from_pdf
from utils.matcher import match_jobs_from_dataset


model = SupervisedModel()

data_path = "data/job_postings.csv"
try:
    job_df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("Job postings dataset not found. Please upload 'data/job_postings.csv'")
    st.stop()

st.title(" Resume-based Job Recommendation App")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Parsed Resume Text")
    st.text_area("", resume_text, height=300)

    extracted_skills = resume_text.lower().split() 

    if st.button("🔍 Recommend Jobs"):
        try:
            predicted_roles = model.predict(extracted_skills)
            predicted_title = predicted_roles[0]["role"]

            recommended_jobs = match_jobs_from_dataset(job_df, predicted_title)

            st.subheader(f"Top Matches for: {predicted_title}")
            for job in recommended_jobs:
                st.markdown(f"""
                **{job['job_title']}** at *{job['company']}*  
                 {job['location']}  
                 Skills: {job['skills']}  
                ---
                """)
        except Exception as e:
            st.error(f"Failed to generate recommendations: {e}")
