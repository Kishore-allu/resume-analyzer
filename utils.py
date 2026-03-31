import PyPDF2
import docx

# ---------- EXTRACT TEXT ----------
def extract_text(file):
    text = ""

    if file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text() or ""

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + " "

    return text.lower()


# ---------- SCORE ----------
def calculate_score(resume, job_desc):
    job_words = job_desc.lower().split()
    resume_words = resume.split()

    match = 0
    for word in job_words:
        if word in resume_words:
            match += 1

    if len(job_words) == 0:
        return 0

    return (match / len(job_words)) * 100


# ---------- MISSING ----------
def get_missing_keywords(resume, job_desc):
    job_words = set(job_desc.lower().split())
    resume_words = set(resume.split())

    missing = job_words - resume_words

    ignore = {"and", "or", "the", "a", "to", "for", "with", "in"}

    result = []
    for word in missing:
        if word not in ignore:
            result.append(word)

    return result


# ---------- SUMMARY ----------
def get_summary(text):
    lines = text.split(".")
    summary = []

    for line in lines:
        if len(line.strip()) > 30:
            summary.append(line.strip())

    return summary[:5]