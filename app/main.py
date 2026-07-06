from app.parsers import parse_resume
from app.preprocessor import preprocess_text
from app.heuristics import analyze_resume
from app.matcher import calculate_match_score, find_missing_keywords
from app.advisor import get_resume_advice

from database.db_manager import (
    create_database,
    save_result,
    get_results
)

import streamlit as st
import pandas as pd

create_database()

st.title("AI Resume Analyzer")

st.caption(
    "Analyze resumes, calculate ATS score, identify missing skills and generate AI suggestions."
)

candidate_name = st.text_input(
    "Enter Candidate Name"
)

st.write("Upload Resume and Check ATS Score")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

job_description = st.text_area(
    "Paste Job Description Here"
)

if st.button("Analyze Resume"):

    if candidate_name and uploaded_file and job_description:

        # Resume Parsing
        resume_text = parse_resume(uploaded_file)

        # Text Cleaning
        clean_resume = preprocess_text(resume_text)
        clean_job = preprocess_text(job_description)

        # ATS Score
        score = calculate_match_score(
            clean_resume,
            clean_job
        )

        # Missing Skills
        missing = find_missing_keywords(
            clean_resume,
            clean_job
        )

        st.success("Analysis Complete")

        save_result(
            candidate_name,
            score
        )

        st.divider()

        st.metric(
            "ATS Score",
            f"{score}%"
        )

        if score >= 80:
            status = "Excellent Resume"
            st.success(status)

        elif score >= 60:
            status = "Good Resume"
            st.warning(status)

        else:
            status = "Needs Improvement"
            st.error(status)

        # Heuristics
        heuristics = analyze_resume(resume_text)

        # Gemini Advice
        advice = get_resume_advice(
            resume_text,
            job_description
        )

        st.divider()

        st.subheader("Heuristics Result")
        st.write(heuristics)

        st.divider()

        st.subheader("Missing Skills")

        if missing:
            for skill in missing:
                st.write(f"• {skill.title()}")
        else:
            st.success("No Missing Skills Found")

        st.divider()

        st.subheader("AI Suggestions")
        st.info(advice)

        # Download Report
        report = f"""
Candidate Name : {candidate_name}

ATS Score : {score}%

Resume Status :
{status}

Missing Skills :
{", ".join(missing) if missing else "None"}

AI Suggestions :
{advice}
"""

        st.download_button(
            label="Download Report",
            data=report,
            file_name="Resume_Report.txt",
            mime="text/plain"
        )

    else:
        st.warning(
            "Please enter candidate name, upload resume and enter job description."
        )

st.divider()

st.caption(
    "Developed using Python, Streamlit, SQLite and NLP."
)