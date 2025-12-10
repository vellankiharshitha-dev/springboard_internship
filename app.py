#app.py
import streamlit as st
from utils.database import init_db
from frontend.registration import show_registration_page
from frontend.login import show_login_page
from frontend.dashboard import show_dashboard


def add_global_css():
    st.markdown(
        """
        <style>
        /* Background image */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1501785888041-af3ef285b470");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .block-container {
            max-width: 900px;
            margin: 80px auto 40px auto !important; 
            background: rgba(255,255,255,0.97);
            border-radius: 24px;
            box-shadow: 0 18px 40px rgba(15,23,42,0.35);
            padding: 32px 32px 36px 32px;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #111827;
        }
        section[data-testid="stSidebar"] h1 {
            color: #fbbf24;
        }
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #e5e7eb;
        }
        section[data-testid="stSidebar"] .stButton>button {
            width: 100%;
            margin-bottom: 8px;
            border-radius: 999px;
            padding: 0.45rem 1rem;
            border: none;
            background: #2563eb;
            color: #ffffff;
            font-weight: 600;
        }
        section[data-testid="stSidebar"] .stButton>button:hover {
            background: #1d4ed8;
        }

        .stButton>button {
            border-radius: 999px;
            padding: 0.45rem 1.2rem;
            border: none;
            background: #2563eb;
            color: #ffffff;
            font-weight: 600;
        }
        .stButton>button:hover {
            background: #1d4ed8;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="Resume App",
        page_icon="📄",
        layout="centered",
    )

    add_global_css()
    init_db()

    # Init session
    if "page" not in st.session_state:
        st.session_state["page"] = "register"
    if "user" not in st.session_state:
        st.session_state["user"] = None

    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        if st.button("Register"):
            st.session_state["page"] = "register"
        if st.button("Login"):
            st.session_state["page"] = "login"
        if st.button("Dashboard"):
            st.session_state["page"] = "dashboard"

    page = st.session_state["page"]

    if page == "register":
        show_registration_page()

    elif page == "login":
        show_login_page()

    elif page == "dashboard":
        if st.session_state.get("user") is None:
            st.warning("You must log in to access the dashboard.")
            st.info("Please use the *Login* option in the sidebar.")
        else:
            show_dashboard()


if __name__ == "__main__":
    main()