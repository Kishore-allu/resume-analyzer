import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def clean_text(text):
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

def calculate_similarity(resume, job_desc):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, job_desc])
    similarity = cosine_similarity(vectors[0], vectors[1])
    return round(similarity[0][0] * 100, 2)

def get_missing_keywords(resume, job_desc):
    resume_words = set(resume.split())
    jd_words = set(job_desc.split())
    missing = jd_words - resume_words
    return list(missing)[:20]

def calculate_ats_score(similarity_score, missing_keywords):
    score = similarity_score
    penalty = len(missing_keywords) * 2
    final_score = score - penalty

    if final_score < 0:
        final_score = 0
    elif final_score > 100:
        final_score = 100

    return round(final_score, 2)