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


def _get_user_name():
    """Best-effort nice display name from st.session_state['user']."""
    user = st.session_state.get("user")
    if isinstance(user, dict):
        for key in ["full_name", "name", "username", "email"]:
            if key in user and user[key]:
                val = str(user[key])
                if "@" in val:
                    return val.split("@")[0].title()
                return val.title()
    if isinstance(user, str) and user:
        if "@" in user:
            return user.split("@")[0].title()
        return user.title()
    return "there"


DASHBOARD_SECTIONS = [
    "Overview",
    "Upload Resume",
    "Quick Analysis",
    "Job Recommendations",
]


def show_dashboard():
    st.markdown(
        """
        <style>
        .stApp {
            background: url("https://static.vecteezy.com/system/resources/thumbnails/031/624/617/small/a-green-wall-with-a-white-background-ai-generated-photo.jpg")
                        no-repeat center center fixed;
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    name = _get_user_name()
    left, right = st.columns([4, 1])
    with left:
        st.markdown(f"### Welcome, *{name}* 👋")
        st.caption("All resume & job insights in one place.")

    with right:
        if st.button("Logout", key="logout_top"):
            st.session_state["user"] = None
            st.session_state["page"] = "login"
            st.rerun()

    st.markdown("---")

    section = st.session_state.get("dashboard_section", "Overview")

    if "last_resume" not in st.session_state:
        st.session_state["last_resume"] = {
            "path": None,
            "uploaded_at": None,
            "analysis": None,
        }

    last_data = st.session_state["last_resume"]
    analysis = last_data.get("analysis")
    resume_path = last_data.get("path")

    if section == "Upload Resume":
        st.subheader("Upload / Replace Resume")
        st.caption("Upload your resume in PDF or DOCX (max ~5MB recommended).")

        uploaded_file = st.file_uploader(
            "Choose a resume file", type=["pdf", "docx"], label_visibility="collapsed"
        )

        if uploaded_file is not None:
            save_dir = "data/resumes"
            os.makedirs(save_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = os.path.splitext(uploaded_file.name)[1].lower() or ".pdf"
            filename = f"user_resume_{timestamp}{ext}"
            file_path = os.path.join(save_dir, filename)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            raw_extracted = extract_resume_text(file_path)
            analysis = basic_resume_analysis(raw_extracted)

            st.session_state["last_resume"] = {
                "path": file_path,
                "uploaded_at": timestamp,
                "analysis": analysis,
            }

            st.success("Resume uploaded and analysed successfully.")
            st.write(f"Saved as: {file_path}")
        else:
            st.info("Upload a resume to enable analysis and recommendations.")

        return 

    if not analysis or not analysis.get("clean_text"):
        st.info("No resume analysed yet. Go to *Upload Resume* section first.")
        return

    if section == "Overview":
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(90deg, #2563eb, #7c3aed);
                padding: 18px 22px;
                border-radius: 16px;
                color: white;
                margin-bottom: 18px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            ">
                <div style="font-size: 14px; opacity: 0.9;">
                    Overview · Resume & Job Snapshot
                </div>
                <div style="font-size: 22px; font-weight: 600; margin-top: 4px;">
                    Hi {name}, here is your profile summary ✨
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div style="
                    background-color: #f9fafb;
                    border-radius: 14px;
                    padding: 14px 16px;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
                ">
                    <div style="font-size: 12px; color:#6b7280;">Approx. word count</div>
                    <div style="font-size: 22px; font-weight: 600; margin-top:4px;">
                        {analysis.get("word_count", 0)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div style="
                    background-color: #f9fafb;
                    border-radius: 14px;
                    padding: 14px 16px;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
                ">
                    <div style="font-size: 12px; color:#6b7280;">Skills detected</div>
                    <div style="font-size: 22px; font-weight: 600; margin-top:4px;">
                        {len(analysis.get("skills", []))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            when = last_data.get("uploaded_at") or "N/A"
            st.markdown(
                f"""
                <div style="
                    background-color: #f9fafb;
                    border-radius: 14px;
                    padding: 14px 16px;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
                ">
                    <div style="font-size: 12px; color:#6b7280;">Last resume upload</div>
                    <div style="font-size: 16px; font-weight: 500; margin-top:4px;">
                        {when}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown(
                """
                <div style="
                    background-color:#ffffff;
                    border-radius:14px;
                    padding:16px 18px;
                    box-shadow:0 1px 4px rgba(0,0,0,0.06);
                    border:1px solid #e5e7eb;
                ">
                    <div style="font-size:15px;font-weight:600;margin-bottom:6px;">
                        Recent Activity
                    </div>
                    <ul style="font-size:13px; color:#4b5563; margin-left:18px;">
                        <li>Most recent resume analysed successfully.</li>
                        <li>Quick Analysis & Job Recommendations are ready.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if resume_path:
                st.caption(f"Latest file: {os.path.basename(resume_path)}")

        with col_right:
            st.markdown(
                """
                <div style="
                    background-color:#eff6ff;
                    border-radius:14px;
                    padding:14px 16px;
                    box-shadow:0 1px 4px rgba(0,0,0,0.04);
                    border:1px solid #dbeafe;
                ">
                    <div style="font-size:14px;font-weight:600;margin-bottom:4px;">
                        Next steps
                    </div>
                    <ul style="font-size:12px; color:#1f2933; margin-left:16px;">
                        <li>Review Quick Analysis tab.</li>
                        <li>Check Job Recommendations.</li>
                        <li>Upload updated resume after changes.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        return

    if section == "Quick Analysis":
        st.subheader("Quick Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.write("*Approx. word count:*", analysis.get("word_count", 0))
            skills = analysis.get("skills", [])
            if skills:
                st.write("*Skills detected:*", ", ".join(skills))
            else:
                st.write("*Skills detected:* None from common keywords.")

        with col2:
            st.markdown("### 🔍 Skill Highlights")
            skills = analysis.get("skills", [])

            if skills:
                cols = st.columns(3)
                for i, skill in enumerate(skills):
                    with cols[i % 3]:
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #f0f2f6;
                                padding: 12px;
                                border-radius: 10px;
                                text-align: center;
                                margin-bottom:10px;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                            ">
                                <h4 style="color:#333;margin:0;font-size:14px;">
                                    {skill.title()}
                                </h4>
                                <p style="font-size:12px;color:#555;margin-top:4px;">
                                    Detected in your resume
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.info("No major skills detected.")

        with st.expander("View extracted resume text"):
            st.text_area(
                "Resume Content",
                analysis.get("clean_text", ""),
                height=220,
            )
        return

    if section == "Job Recommendations":
        st.subheader("Job Recommendations")
        st.caption("Sample roles based on skills found in your resume.")

        jobs = get_job_recommendations(analysis)
        for job in jobs:
            st.markdown(
                f"""
                <div style="
                    background-color:#f8f9fb;
                    padding:15px;
                    border-radius:10px;
                    margin-bottom:10px;
                    box-shadow:0 1px 3px rgba(0,0,0,0.08);
                ">
                    <h4 style="margin:0 0 4px 0;">{job['title']}</h4>
                    <p style="margin:0 0 4px 0;font-size:13px;color:#555;">
                        {job['meta']}
                    </p>
                    <p style="margin:0;font-size:12px;color:#777;">
                        <strong>Skills:</strong> {job['tags']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        return

    st.write("Unknown section.")