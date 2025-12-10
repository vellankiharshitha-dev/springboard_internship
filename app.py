import streamlit as st
from frontend.registration import show_registration_page
from frontend.login import show_login_page
from frontend.dashboard import show_dashboard


DASHBOARD_SECTIONS = [
    "Overview",
    "Upload Resume",
    "Quick Analysis",
    "Job Recommendations",
]


def init_session_state():
    if "page" not in st.session_state:
        st.session_state["page"] = "register"
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "dashboard_section" not in st.session_state:
        st.session_state["dashboard_section"] = "Overview"


def sidebar_navigation():
    with st.sidebar:
        st.title("Navigation")

        if st.button("Register", key="nav_register"):
            st.session_state["page"] = "register"

        if st.button("Login", key="nav_login"):
            st.session_state["page"] = "login"

        if st.button("Dashboard", key="nav_dashboard"):
            st.session_state["page"] = "dashboard"

        st.markdown("---")

        if (
            st.session_state.get("user") is not None
            and st.session_state.get("page") == "dashboard"
        ):
            st.caption("Dashboard Sections")

            current = st.session_state.get("dashboard_section", "Overview")
            try:
                idx = DASHBOARD_SECTIONS.index(current)
            except ValueError:
                idx = 0

            selected = st.radio(
                "Dashboard Sections",
                DASHBOARD_SECTIONS,
                index=idx,
                label_visibility="collapsed",
                key="dashboard_sections_sidebar",
            )

            st.session_state["dashboard_section"] = selected

        st.markdown("---")

        if st.session_state.get("user"):
            if st.button("Logout", key="nav_logout"):
                st.session_state["user"] = None
                st.session_state["page"] = "login"
                st.experimental_rerun()
        else:
            st.caption("Not signed in")

        st.markdown("---")
        st.caption("Use the navigation buttons above to move between pages.")


def main():

    st.set_page_config(page_title="Resume App", layout="wide")
    init_session_state()

    sidebar_navigation()

    page = st.session_state.get("page", "register")

    if page == "register":
        show_registration_page()

    elif page == "login":
        show_login_page()

    elif page == "dashboard":
        if st.session_state.get("user") is None:
            st.warning("You must log in to access the dashboard.")
            st.info("Please use the Login option in the sidebar.")
        else:
            show_dashboard()

    else:
        st.session_state["page"] = "register"
        st.experimental_rerun()


if __name__ == "__main__":
    main()