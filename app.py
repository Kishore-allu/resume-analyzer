import streamlit as st
from utils import extract_text, calculate_score, get_missing_keywords, get_summary

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.stButton>button {
    background-color: #00c896;
    color: black;
    border-radius: 8px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("AI Resume Analyzer")

# ---------- FILE ----------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

# ---------- JOB DESC ----------
job_desc = st.text_area("Paste Job Description")

# ---------- BUTTON ----------
if st.button("Analyze Resume"):

    if uploaded_file is not None and job_desc != "":

        resume_text = extract_text(uploaded_file)

        score = calculate_score(resume_text, job_desc)
        missing = get_missing_keywords(resume_text, job_desc)
        summary = get_summary(resume_text)

        # ---------- SCORES ----------
        st.subheader("Match Score")
        st.progress(score / 100)
        st.write(f"{score:.2f}%")

        st.subheader("ATS Score")
        st.progress(score / 100)
        st.write(f"{score:.2f} / 100")

        # ---------- MISSING ----------
        st.subheader("Missing Keywords")
        for word in missing:
            st.write(f"• {word}")

        # ---------- SUGGESTIONS ----------
        st.subheader("Suggestions to Improve Resume")
        for word in missing:
            st.write(f"• Include the keyword '{word}' naturally in your resume")

        # ---------- SUMMARY ----------
        st.subheader("Quick Resume Summary")
        for point in summary:
            st.write(f"• {point}")

        # ---------- DOWNLOAD ----------
        report = f"""
AI Resume Analysis Report

Match Score: {score:.2f}%
ATS Score: {score:.2f}/100

Missing Keywords:
{', '.join(missing)}

Summary:
{chr(10).join(summary)}
        """

        st.download_button(
            label="Download Report",
            data=report,
            file_name="resume_report.txt",
            mime="text/plain"
        )

    else:
        st.warning("Please upload resume and enter job description")