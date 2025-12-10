import streamlit as st
from backend.resume_parser import extract_resume_text
import os
import datetime


def basic_resume_analysis(text):
    """Handle both string and (text, extra) tuple safely."""
    if isinstance(text, tuple):
        text = text[0]

    if not text or not isinstance(text, str):
        return {"word_count": 0, "skills": [], "clean_text": ""}

    lower = text.lower()
    words = text.split()
    length = len(words)

    skills = []
    for skill in [
        "python",
        "java",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "django",
        "flask",
        "machine learning",
        "data analysis",
    ]:
        if skill in lower:
            skills.append(skill)

    return {"word_count": length, "skills": skills, "clean_text": text}


def get_job_recommendations(analysis: dict):
    skills = set(analysis.get("skills", []))
    jobs = []

    if {"python", "sql"} & skills:
        jobs.append(
            {
                "title": "Junior Data Analyst",
                "meta": "Entry-level · Remote / Hybrid",
                "tags": "Python · SQL · Excel",
            }
        )

    if {"html", "css", "javascript"} <= skills:
        jobs.append(
            {
                "title": "Frontend Developer Intern",
                "meta": "Internship · Web Development",
                "tags": "HTML · CSS · JavaScript",
            }
        )

    if {"python", "django"} & skills:
        jobs.append(
            {
                "title": "Python / Django Developer Intern",
                "meta": "Internship · Backend",
                "tags": "Python · Django · REST APIs",
            }
        )

    if not jobs:
        jobs.append(
            {
                "title": "Software Developer Intern",
                "meta": "Internship · Generalist",
                "tags": "Problem Solving · OOP · Git",
            }
        )

    return jobs


def show_dashboard():
    # ------------ TOP ROW: TITLE + LOGOUT BUTTON ------------
    title_col, logout_col = st.columns([7, 1])

    with title_col:
        st.markdown("### WELCOME 👋 TO RESUME ANALYSER! ")
        st.markdown(
            "Upload your resume below to see quick analysis and sample job recommendations."
        )

    with logout_col:
        if st.button("Logout"):
            # remove logged-in user and send back to login page
            st.session_state["user"] = None
            st.session_state["page"] = "login"
            st.rerun()
    # --------------------------------------------------------

    st.markdown("#### Step 1 · Upload Resume")
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])

    if not uploaded_file:
        st.info("Upload a resume to view analysis and job suggestions.")
        return

    # Save resume
    save_dir = "data/resumes"
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_resume_{timestamp}.pdf"
    file_path = os.path.join(save_dir, filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Resume uploaded successfully.")
    st.write(f"Saved as: {file_path}")

    # Extract + analyse
    raw_extracted = extract_resume_text(file_path)
    analysis = basic_resume_analysis(raw_extracted)
    text = analysis["clean_text"]

    if not text:
        st.warning(
            "Could not extract text from this resume. "
            "Analysis and job suggestions are skipped for this file."
        )
        return

    st.markdown("---")
    st.markdown("#### Step 2 · Quick Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Approx. word count:", analysis.get("word_count", 0))
    with col2:
        skills = analysis.get("skills", [])
        if skills:
            st.write("Skills detected:", ", ".join(skills))
        else:
            st.write("Skills detected: None found from common keywords.")

    with st.expander("View extracted resume text"):
        st.text_area("Resume Content", text, height=220)

    st.markdown("---")
    st.markdown("#### Step 3 · Job Recommendations")

    st.caption("Sample roles based on the skills found in your resume text.")

    jobs = get_job_recommendations(analysis)
    for job in jobs:
        st.write(f"{job['title']}")
        st.write(f"{job['meta']}")
        st.write(f"Skills: {job['tags']}")
        st.markdown("---")