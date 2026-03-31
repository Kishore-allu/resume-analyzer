import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.lower()

def calculate_match_score(resume, job_desc):
    resume_words = set(resume.split())
    job_words = set(job_desc.split())

    matched = resume_words.intersection(job_words)
    score = len(matched) / len(job_words) * 100 if job_words else 0

    missing = job_words - resume_words

    return score, list(missing)

def generate_suggestions(missing_keywords):
    suggestions = []

    for word in missing_keywords:
        if word == "teamwork":
            suggestions.append("Mention teamwork experience like: 'Collaborated with cross-functional teams to complete projects'")
        
        elif word == "communication":
            suggestions.append("Add communication skills like: 'Effectively communicated ideas with team members and stakeholders'")
        
        elif word == "leadership":
            suggestions.append("Include leadership experience like: 'Led a team or managed responsibilities in projects'")
        
        else:
            suggestions.append(f"Try including the keyword '{word}' naturally in your resume")

    return suggestions

    for word in missing_keywords:
        if word in smart_map:
            suggestions.append(f"👉 Improve '{word}' by adding:")
            for line in smart_map[word]:
                suggestions.append(f"   - {line}")
        else:
            suggestions.append(f"👉 Consider including '{word}' in your resume")

    return suggestions

def highlight_text(resume, job_desc):
    resume_words = resume.split()
    job_words = set(job_desc.split())

    highlighted = []

    for word in resume_words:
        if word in job_words:
            highlighted.append(f"<span style='color:#00ffcc'>{word}</span>")
        else:
            highlighted.append(word)

    return " ".join(highlighted)