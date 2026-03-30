import streamlit as st
from utils import (
    extract_text_from_pdf,
    clean_text,
    calculate_similarity,
    get_missing_keywords,
    calculate_ats_score,
    generate_suggestions
)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer 💼")
st.write("Upload your resume and compare it with a job description")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type="pdf")
job_desc = st.text_area("📝 Paste Job Description")

# 🔥 NEW: Button
if st.button("🚀 Analyze Resume"):

    if uploaded_file and job_desc:

        resume_text = extract_text_from_pdf(uploaded_file)

        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(job_desc)

        score = calculate_similarity(cleaned_resume, cleaned_jd)
        missing_skills = get_missing_keywords(cleaned_resume, cleaned_jd)
        ats_score = calculate_ats_score(score, missing_skills)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Match Score")
            st.success(f"{score}%")

            st.subheader("⭐ ATS Score")
            st.success(f"{ats_score} / 100")

        with col2:
            st.subheader("❌ Missing Keywords")
            st.warning(missing_skills)

        # Suggestions
        suggestions = generate_suggestions(missing_skills)

        st.subheader("💡 Suggestions to Improve Resume")
        for s in suggestions:
            st.write(s)

        with st.expander("📄 View Original Resume Text"):
            st.write(resume_text)

        with st.expander("🧹 View Cleaned Resume Text"):
            st.write(cleaned_resume)

    else:
        st.error("⚠️ Please upload resume and paste job description")