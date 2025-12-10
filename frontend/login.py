import streamlit as st
from backend.auth import login_user


def show_login_page():
    st.markdown(
        """
        <style>
        .stApp {
            background: #EEAECA;
            background: radial-gradient(circle, rgba(238, 174, 202, 1) 0%, rgba(148, 187, 233, 1) 100%);
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    st.markdown("### Login")
    st.markdown(
        "<p style='font-size:13px; color:#6b7280;'>Enter your email and password to continue.</p>",
        unsafe_allow_html=True,
    )

    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Login" ,key="login_form_submit"):
        success, message, user = login_user(email, password)

        if success:
            st.success(message)
            st.session_state["user"] = user
            st.session_state["page"] = "dashboard"
            try:
                st.rerun()
            except Exception:
                st.experimental_rerun()
        else:
            st.error(message)

    st.markdown("New user? Use the *Register* option in the sidebar.")