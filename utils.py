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

    smart_map = {
        "teamwork": [
            "Collaborated with cross-functional teams",
            "Worked effectively in team environments"
        ],
        "communication": [
            "Demonstrated strong verbal and written communication",
            "Presented ideas clearly to stakeholders"
        ],
        "leadership": [
            "Led a team/project successfully",
            "Took initiative in key decisions"
        ],
        "python": [
            "Built projects using Python",
            "Worked on automation scripts using Python"
        ],
        "management": [
            "Managed project timelines and deliverables",
            "Handled multiple tasks efficiently"
        ]
    }

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