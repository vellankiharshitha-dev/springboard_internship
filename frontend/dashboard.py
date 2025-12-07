import streamlit as st
from pathlib import Path
from datetime import datetime
from utils.database import update_user_resume_path


# ------------------------------
# CUSTOM CSS FOR DASHBOARD UI
# ------------------------------
def load_css():
    st.markdown(
        """
        <style>
        .dashboard-container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
            width: 70%;
            margin: auto;
            margin-top: 40px;
        }

        .welcome-title {
            font-size: 32px;
            font-weight: 700;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }

        .welcome-subtitle {
            font-size: 16px;
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }

        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 10px;
            color: #34495e;
        }

        .hint-text {
            font-size: 13px;
            color: #7f8c8d;
            margin-bottom: 10px;
        }

        .logout-container {
            text-align: center;
            margin-top: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ------------------------------
# DASHBOARD PAGE UI + RESUME UPLOAD
# ------------------------------
def show_dashboard():
    load_css()

    # Check if user is logged in
    if "user" not in st.session_state or st.session_state["user"] is None:
        st.warning("You must log in to access the dashboard.")
        st.info("Use the sidebar to go to the Login page.")
        return

    user = st.session_state["user"]

    # Dashboard container
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

    # Welcome section
    st.markdown(
        f'<div class="welcome-title">Welcome, {user["full_name"]} 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">Your personalized resume analysis dashboard is ready.</div>',
        unsafe_allow_html=True
    )

    # ------------------ RESUME UPLOAD SECTION ------------------
    st.markdown('<div class="section-title">📄 Upload Your Resume</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint-text">Allowed formats: PDF, DOCX • Max size: 5 MB</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx"])

    if uploaded_file is not None:
        # Size validation (5 MB)
        max_size = 5 * 1024 * 1024  # 5 MB
        if uploaded_file.size > max_size:
            st.error("File is too large. Maximum allowed size is 5 MB.")
        else:
            # Build a unique filename
            resumes_dir = Path("data/resumes")
            resumes_dir.mkdir(parents=True, exist_ok=True)

            extension = uploaded_file.name.split(".")[-1].lower()
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            filename = f"user_{user['id']}_{timestamp}.{extension}"

            save_path = resumes_dir / filename

            # Save file to disk
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Update database with resume path
            update_user_resume_path(user["id"], str(save_path))

            st.success("Resume uploaded successfully!")
            st.info(f"Saved as: {save_path}")

    # ------------------ PLACEHOLDER SECTIONS ------------------
    st.markdown('<div class="section-title">📝 Resume Analysis</div>', unsafe_allow_html=True)
    st.write("Resume analysis features will be added in the next milestone.")

    st.markdown('<div class="section-title">💼 Job Recommendations</div>', unsafe_allow_html=True)
    st.write("Job recommendation features will be added in a later milestone.")

    # Logout
    st.markdown('<div class="logout-container">', unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state["user"] = None
        st.session_state["page"] = "login"
        st.success("Logged out successfully!")

    st.markdown("</div>", unsafe_allow_html=True)  # logout container
    st.markdown("</div>", unsafe_allow_html=True)  # dashboard container