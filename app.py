import streamlit as st
import PyPDF2
from utils import clean_text, calculate_match_score, generate_suggestions, highlight_text

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #00ffcc;
}

.section {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #00ffcc;
    color: black;
    border-radius: 8px;
    font-weight: bold;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<div class='big-title'>📄 AI Resume Analyzer 🚀</div>", unsafe_allow_html=True)

# ------------------ FILE UPLOAD ------------------
st.markdown("### 📤 Upload your Resume")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# ------------------ JOB DESCRIPTION ------------------
st.markdown("### 📝 Paste Job Description")
job_description = st.text_area("Enter job description here...")

# ------------------ BUTTON ------------------
analyze = st.button("🚀 Analyze Resume")

# ------------------ PDF FUNCTION ------------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ------------------ MAIN LOGIC ------------------
if analyze:
    if uploaded_file is not None and job_description:

        # Extract text
        resume_text = extract_text_from_pdf(uploaded_file)

        # Clean text
        clean_resume = clean_text(resume_text)
        clean_job = clean_text(job_description)

        # Score calculation
        score, missing = calculate_match_score(clean_resume, clean_job)
        ats_score = score * 0.8

        # ------------------ MATCH SCORE ------------------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📊 Match Score")
        st.progress(int(score))
        st.write(f"### {score:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)

        # ------------------ ATS SCORE ------------------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("⭐ ATS Score")
        st.progress(int(ats_score))
        st.write(f"### {ats_score:.2f} / 100")
        st.markdown("</div>", unsafe_allow_html=True)

        # ------------------ MISSING KEYWORDS ------------------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("❌ Missing Keywords")
        st.write(missing)
        st.markdown("</div>", unsafe_allow_html=True)

        # ------------------ SUGGESTIONS ------------------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("💡 Smart Suggestions")

        suggestions = generate_suggestions(missing)

        for s in suggestions:
            st.write(s)

        st.markdown("</div>", unsafe_allow_html=True)

        # ------------------ HIGHLIGHT ------------------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📄 Resume with Highlights")

        highlighted_resume = highlight_text(clean_resume, clean_job)
        st.markdown(highlighted_resume, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ------------------ DOWNLOAD REPORT ------------------
        report = f"""
AI Resume Analysis Report

Match Score: {score:.2f}%
ATS Score: {ats_score:.2f}/100

Missing Keywords:
{', '.join(missing)}

Suggestions:
"""

        for s in suggestions:
            report += f"\n{s}"

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="resume_analysis.txt",
            mime="text/plain"
        )

    else:
        st.warning("⚠️ Please upload resume and paste job description.")