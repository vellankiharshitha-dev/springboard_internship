import streamlit as st
from utils.database import init_db
from frontend.registration import show_registration_page
from frontend.login import show_login_page
from frontend.dashboard import show_dashboard


def main():
    # Basic page setup
    st.set_page_config(page_title="Resume App", page_icon="📄", layout="centered")

    # Initialize DB
    init_db()

    # Session defaults
    if "page" not in st.session_state:
        # first time: show Register
        st.session_state["page"] = "register"

    if "user" not in st.session_state:
        st.session_state["user"] = None

    # ---- Sidebar navigation (buttons, NOT radio) ----
    with st.sidebar:
        st.title("Navigation")

        if st.button("Register"):
            st.session_state["page"] = "register"

        if st.button("Login"):
            st.session_state["page"] = "login"

        if st.button("Dashboard"):
            st.session_state["page"] = "dashboard"

    # ---- Decide which page to show ----
    page = st.session_state["page"]

    if page == "register":
        show_registration_page()
    elif page == "login":
        show_login_page()
    elif page == "dashboard":
        show_dashboard()


if __name__ == "__main__":
    main()