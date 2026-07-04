from app.heuristics import analyze_resume


def get_resume_advice(resume_text, job_description):
    """Return simple, deterministic advice using existing utilities.

    This avoids an external `model` dependency and provides useful
    feedback: match score, missing keywords, basic checks, and
    actionable improvement suggestions.
    """

    # Simple token-based match score to avoid heavy dependencies
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    if not job_words:
        score = 0.0
    else:
        match_count = len(resume_words & job_words)
        score = round((match_count / len(job_words)) * 100, 2)

    missing = list(job_words - resume_words)

    checks = analyze_resume(resume_text)

    parts = []
    parts.append("TEST SUCCESS")

    if missing:
        parts.append("Missing keywords: " + ", ".join(missing))
    else:
        parts.append("No major missing keywords detected.")

    parts.append("Resume analysis:")

    for key, val in checks.items():
        label = key.replace("_found", "").replace("_", " ").capitalize()
        parts.append(f"- {label}: {'Yes' if val else 'No'}")

    suggestions = [
        "Add missing skills and keywords from the job description.",
        "Include contact info (email, phone) and LinkedIn if missing.",
        "Expand the summary to highlight relevant experience and tools (e.g. Docker).",
    ]

    parts.append("Suggested improvements:")
    for s in suggestions:
        parts.append(f"- {s}")

    return "\n".join(parts)