import streamlit as st
from utils import (
    extract_text_from_pdf,
    clean_text,
    calculate_similarity,
    get_missing_keywords,
    generate_suggestions,
    generate_summary
)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0d1117; color: white; }
h1 { color: #00ffaa; }
h2, h3 { color: #58a6ff; }
.stButton>button { background-color: #00ffaa; color: black; border-radius: 10px; font-weight: bold; }
.stTextArea textarea { background-color: #161b22; color: white; }
.stFileUploader { background-color: #161b22; }
</style>
""", unsafe_allow_html=True)

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if uploaded_file is not None and job_description.strip() != "":
        resume_text = extract_text_from_pdf(uploaded_file)
        cleaned_resume = clean_text(resume_text)
        cleaned_job = clean_text(job_description)
        score = calculate_similarity(cleaned_resume, cleaned_job)
        missing_keywords = get_missing_keywords(cleaned_resume, cleaned_job)
        suggestions = generate_suggestions(missing_keywords)
        summary_points = generate_summary(cleaned_resume)
        
        st.subheader("Match Score")
        st.progress(score)
        st.markdown(f"### {score*100:.2f}%")
        
        st.subheader("ATS Score")
        st.progress(score)
        st.markdown(f"### {score*100:.2f} / 100")
        
        st.subheader("Missing Keywords")
        if missing_keywords:
            for word in missing_keywords[:10]:
                st.markdown(f"• {word}")
        else:
            st.success("No missing keywords found!")
        
        st.subheader("Suggestions to Improve Resume")
        for s in suggestions[:5]:
            st.markdown(f"• {s}")
        
        st.subheader("Quick Resume Summary")
        for point in summary_points:
            st.markdown(f"• {point}")
    else:
        st.warning("Please upload resume and paste job description")