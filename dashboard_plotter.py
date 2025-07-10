import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from models.supervised import SupervisedModel
from utils.resume_parser import extract_text_from_pdf
from utils.matcher import match_jobs_from_dataset

# === Streamlit Page Config ===
st.set_page_config(page_title="PathGenie", layout="wide")

# === Sidebar Navigation ===
st.sidebar.title("🔍 PathGenie Navigator")
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Dashboard"])

# === Load Job Dataset ===
data_path = "data/job_postings.csv"
try:
    job_df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("Job postings dataset not found.")
    st.stop()

# === Load Model ===
model = SupervisedModel()

# === Home Page ===
if page == "🏠 Home":
    st.title("📄 Resume-based Job Recommendation App")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.subheader("📃 Extracted Resume Text")
        st.text_area("", resume_text, height=300)

        extracted_skills = resume_text.lower().split()

        if st.button("🔎 Recommend Jobs"):
            try:
                predicted_roles = model.predict(extracted_skills)
                predicted_title = predicted_roles[0]["role"]

                recommended_jobs = match_jobs_from_dataset(job_df, predicted_title)

                st.success(f"🎯 Predicted Role: {predicted_title}")
                st.markdown("---")

                for job in recommended_jobs:
                    st.markdown(f"""
                    <div style='background-color:#f0f0f5; padding:15px; border-radius:10px; margin-bottom:10px;'>
                        <h5>{job['job_title']} at <span style='color:#2c3e50'>{job['company']}</span></h5>
                        📍 <b>{job['location']}</b><br>
                        🛠️ Skills: {job['skills']}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Failed to generate recommendations: {e}")

# === Dashboard Page ===
elif page == "📊 Dashboard":
    st.markdown("## 📊 Model Dashboard")
    st.markdown("Visualize model performance metrics in real-time:")

    df = job_df.dropna(subset=["skills", "job_title"])
    df["skills"] = df["skills"].str.lower()
    X_raw = df["skills"]
    y_raw = df["job_title"]

    vectorizer = TfidfVectorizer(max_features=161)
    X_vec = vectorizer.fit_transform(X_raw)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_raw)
    scaler = StandardScaler(with_mean=False)
    X_scaled = scaler.fit_transform(X_vec)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

    model = SupervisedModel(vectorizer, label_encoder, scaler)
    model.train(X_train, y_train)
    y_pred = model.model.predict(X_test)

    # === Confusion Matrix ===
    st.subheader("📉 Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred, labels=np.unique(y_test))
    fig, ax = plt.subplots(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
    disp.plot(ax=ax, cmap='Blues', colorbar=False)
    st.pyplot(fig)

    # === Metrics ===
    st.markdown("---")
    st.subheader("📈 Evaluation Metrics")
    metrics = model.evaluate(X_test, y_test)
    for key, value in metrics.items():
        st.markdown(f"**{key.capitalize()}**")
        st.progress(value)
        st.write(f"{value*100:.2f}%")