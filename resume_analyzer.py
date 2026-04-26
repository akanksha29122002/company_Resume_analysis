import math
import re
from collections import Counter
from io import BytesIO

from pypdf import PdfReader


SECTION_PATTERNS = {
    "Education": r"\b(education|academic|qualification|degree|university|college)\b",
    "Experience": r"\b(experience|employment|internship|work history|professional experience)\b",
    "Projects": r"\b(projects?|portfolio|case study)\b",
    "Skills": r"\b(skills?|technical skills|tools|technologies)\b",
    "Certifications": r"\b(certifications?|courses?|training|licenses?)\b",
    "Contact": r"\b(email|phone|mobile|linkedin|github|portfolio)\b",
}


SKILL_BANK = {
    "Programming": [
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c",
        "sql",
        "html",
        "css",
        "php",
        "r",
    ],
    "Data and AI": [
        "machine learning",
        "deep learning",
        "nlp",
        "natural language processing",
        "computer vision",
        "data analysis",
        "data visualization",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "opencv",
        "streamlit",
    ],
    "Web and Backend": [
        "react",
        "node",
        "express",
        "django",
        "flask",
        "fastapi",
        "rest api",
        "mongodb",
        "mysql",
        "postgresql",
        "firebase",
    ],
    "Cloud and Tools": [
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "gcp",
        "linux",
        "vercel",
        "render",
    ],
    "Soft Skills": [
        "communication",
        "teamwork",
        "leadership",
        "problem solving",
        "critical thinking",
        "time management",
    ],
}


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
    "you",
    "your",
    "will",
    "we",
    "our",
}


def extract_pdf_text(uploaded_file) -> str:
    """Extract text from an uploaded PDF file-like object."""
    data = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.read()
    reader = PdfReader(BytesIO(data))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return clean_text("\n".join(pages))


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Page\s+\d+", " ", text, flags=re.IGNORECASE)
    return text.strip()


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z+#.\-]{1,}", text.lower())
        if token not in STOP_WORDS and len(token) > 2
    ]


def cosine_similarity(text_a: str, text_b: str) -> float:
    tokens_a = Counter(tokenize(text_a))
    tokens_b = Counter(tokenize(text_b))
    if not tokens_a or not tokens_b:
        return 0.0

    common = set(tokens_a) & set(tokens_b)
    dot = sum(tokens_a[word] * tokens_b[word] for word in common)
    norm_a = math.sqrt(sum(value * value for value in tokens_a.values()))
    norm_b = math.sqrt(sum(value * value for value in tokens_b.values()))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def detect_sections(text: str) -> dict[str, bool]:
    return {
        section: bool(re.search(pattern, text, flags=re.IGNORECASE))
        for section, pattern in SECTION_PATTERNS.items()
    }


def detect_skills(text: str) -> dict[str, list[str]]:
    lowered = text.lower()
    found = {}
    for category, skills in SKILL_BANK.items():
        matches = []
        for skill in skills:
            pattern = r"(?<![a-zA-Z])" + re.escape(skill.lower()) + r"(?![a-zA-Z])"
            if re.search(pattern, lowered):
                matches.append(skill)
        found[category] = matches
    return found


def flatten_skills(skills_by_category: dict[str, list[str]]) -> list[str]:
    return sorted({skill for skills in skills_by_category.values() for skill in skills})


def keyword_overlap(resume_text: str, job_description: str) -> tuple[list[str], list[str], float]:
    resume_terms = set(tokenize(resume_text))
    job_terms = set(tokenize(job_description))
    if not job_terms:
        return [], [], 0.0

    matched = sorted(resume_terms & job_terms)
    missing = sorted(job_terms - resume_terms)
    return matched, missing[:30], len(matched) / len(job_terms)


def contact_quality(text: str) -> dict[str, bool]:
    return {
        "Email": bool(re.search(r"[\w.\-+]+@[\w.\-]+\.\w+", text)),
        "Phone": bool(re.search(r"(\+?\d[\d\s\-()]{8,}\d)", text)),
        "LinkedIn": "linkedin" in text.lower(),
        "GitHub": "github" in text.lower(),
    }


def analyze_resume(resume_text: str, job_description: str) -> dict:
    sections = detect_sections(resume_text)
    skills_by_category = detect_skills(resume_text)
    job_skills_by_category = detect_skills(job_description)
    found_skills = flatten_skills(skills_by_category)
    job_skills = flatten_skills(job_skills_by_category)
    matched_keywords, missing_keywords, overlap_score = keyword_overlap(resume_text, job_description)
    semantic_score = cosine_similarity(resume_text, job_description) if job_description.strip() else 0.0
    contacts = contact_quality(resume_text)

    required_skills = set(job_skills)
    resume_skills = set(found_skills)
    skill_score = len(resume_skills & required_skills) / len(required_skills) if required_skills else 0.6
    section_score = sum(sections.values()) / len(sections)
    contact_score = sum(contacts.values()) / len(contacts)
    length_score = _length_score(len(tokenize(resume_text)))

    ats_score = round(
        100
        * (
            0.30 * skill_score
            + 0.25 * semantic_score
            + 0.20 * section_score
            + 0.15 * overlap_score
            + 0.05 * contact_score
            + 0.05 * length_score
        )
    )
    ats_score = max(0, min(100, ats_score))

    missing_sections = [name for name, present in sections.items() if not present]
    missing_skills = sorted(required_skills - resume_skills)
    strengths = _strengths(sections, skills_by_category, contacts, ats_score)
    weaknesses = _weaknesses(missing_sections, missing_skills, missing_keywords, contacts, len(tokenize(resume_text)))
    suggestions = _suggestions(missing_sections, missing_skills, missing_keywords, job_description)

    return {
        "ats_score": ats_score,
        "semantic_match": round(semantic_score * 100, 1),
        "keyword_match": round(overlap_score * 100, 1),
        "word_count": len(tokenize(resume_text)),
        "sections": sections,
        "contacts": contacts,
        "skills_by_category": skills_by_category,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords[:40],
        "missing_keywords": missing_keywords,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }


def _length_score(word_count: int) -> float:
    if 350 <= word_count <= 850:
        return 1.0
    if 250 <= word_count < 350 or 850 < word_count <= 1100:
        return 0.7
    if word_count > 0:
        return 0.4
    return 0.0


def _strengths(sections, skills_by_category, contacts, ats_score):
    strengths = []
    if ats_score >= 70:
        strengths.append("Resume has a strong overall match with the target job description.")
    if sections.get("Projects"):
        strengths.append("Project section is present, which helps demonstrate practical experience.")
    if sections.get("Skills"):
        strengths.append("Dedicated skills section makes the resume easier for ATS systems to parse.")
    if any(skills_by_category.values()):
        strengths.append("Relevant technical and professional skills were detected.")
    if contacts.get("Email") and contacts.get("Phone"):
        strengths.append("Basic contact details are available.")
    return strengths or ["Resume text was extracted successfully and is ready for improvement."]


def _weaknesses(missing_sections, missing_skills, missing_keywords, contacts, word_count):
    weaknesses = []
    if missing_sections:
        weaknesses.append("Missing or unclear sections: " + ", ".join(missing_sections[:4]) + ".")
    if missing_skills:
        weaknesses.append("Important job-related skills are not visible: " + ", ".join(missing_skills[:8]) + ".")
    if missing_keywords:
        weaknesses.append("Several job description keywords are absent from the resume.")
    if not contacts.get("LinkedIn"):
        weaknesses.append("LinkedIn profile is not clearly mentioned.")
    if word_count < 250:
        weaknesses.append("Resume content looks short; add measurable details and project outcomes.")
    elif word_count > 1100:
        weaknesses.append("Resume content may be too long for quick screening.")
    return weaknesses or ["No major weakness detected from the available text."]


def _suggestions(missing_sections, missing_skills, missing_keywords, job_description):
    suggestions = []
    if missing_sections:
        suggestions.append("Add clear headings for " + ", ".join(missing_sections[:3]) + ".")
    if missing_skills:
        suggestions.append("Include relevant skills where truthful: " + ", ".join(missing_skills[:8]) + ".")
    if missing_keywords:
        suggestions.append("Mirror important job keywords naturally in project and experience bullet points.")
    if job_description.strip():
        suggestions.append("Rewrite 2-3 bullets to show impact using action verb + tool + measurable result.")
    suggestions.append("Keep formatting simple: standard headings, PDF export, readable fonts, and no heavy graphics.")
    return suggestions
