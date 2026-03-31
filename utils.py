import streamlit as st
import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def clean_text(text):
    return text.lower()


def calculate_similarity(resume, job_desc):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, job_desc])
    similarity = cosine_similarity(matrix)[0][1]
    return similarity


def get_missing_keywords(resume, job_desc):
    resume_words = set(resume.split())
    job_words = set(job_desc.split())
    missing = job_words - resume_words
    return list(missing)


def generate_suggestions(missing_keywords):
    suggestions = []
    for word in missing_keywords:
        if word == "teamwork":
            suggestions.append("Collaborated with cross-functional teams to complete projects")
        elif word == "communication":
            suggestions.append("Effectively communicated ideas with team members and stakeholders")
        elif word == "leadership":
            suggestions.append("Led a team or managed responsibilities in projects")
        else:
            suggestions.append(f"Include the keyword '{word}' naturally in your resume")
    return suggestions


def generate_summary(resume_text):
    sentences = resume_text.split('.')
    summary = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 40:
            summary.append(sentence)
        if len(summary) == 5:
            break
    return summary