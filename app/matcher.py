from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def create_vectors(resume_text, job_text):
    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(
        [resume_text.lower(), job_text.lower()]
    )

    return vectors


def calculate_skill_score(resume_text, job_text):

    resume_words = set(
        re.findall(r"[a-zA-Z0-9+#.]+", resume_text.lower())
    )

    job_words = set(
        re.findall(r"[a-zA-Z0-9+#.]+", job_text.lower())
    )

    if len(job_words) == 0:
        return 0

    matched = resume_words.intersection(job_words)

    score = (
        len(matched) /
        len(job_words)
    ) * 100

    return round(score, 2)


def calculate_match_score(resume_text, job_text):

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(
        [resume_text.lower(), job_text.lower()]
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    tfidf_score = similarity * 100

    skill_score = calculate_skill_score(
        resume_text,
        job_text
    )

    # Weighted ATS Score
    raw_score = (
        (0.4 * tfidf_score) +
        (0.6 * skill_score)
    )

    # Scale score to 60–82
    final_score = 60 + (raw_score * 0.22)

    if final_score > 82:
        final_score = 82

    if final_score < 60:
        final_score = 60

    return round(final_score, 2)


def find_missing_keywords(resume_text, job_text):

    resume_words = set(
        re.findall(r"[a-zA-Z0-9+#.]+", resume_text.lower())
    )

    job_words = set(
        re.findall(r"[a-zA-Z0-9+#.]+", job_text.lower())
    )

    stop_words = {
        "and", "or", "the", "a", "an",
        "to", "of", "in", "for",
        "with", "on", "at", "is",
        "are", "be", "by", "from",
        "this", "that", "will",
        "can", "should", "must"
    }

    missing = sorted(
        job_words - resume_words - stop_words
    )

    return missing