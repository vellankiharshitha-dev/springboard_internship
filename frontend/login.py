import streamlit as st
from backend.auth import login_user


# ------------------------------
# CUSTOM CSS (same design as registration)
# ------------------------------
def load_css():
    st.markdown(
        """
        <style>
        .main-container {
            background-color: #f5f7fa;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
            width: 420px;
            margin: auto;
        }

        .title {
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
            color: #2c3e50;
        }

        .subtitle {
            text-align: center;
            font-size: 14px;
            margin-bottom: 25px;
            color: #7f8c8d;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ------------------------------
# LOGIN PAGE UI
# ------------------------------
def show_login_page():
    load_css()

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<div class="title">Welcome Back</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Log in to continue</div>', unsafe_allow_html=True)

    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, message, user = login_user(email, password)

        if success:
            st.success(message)
            # store user and go to dashboard
            st.session_state["user"] = user
            st.session_state["page"] = "dashboard"

            # force rerun so app.py immediately shows dashboard
            try:
                st.rerun()                # new Streamlit
            except Exception:
                st.experimental_rerun()   # old Streamlit fallback
        else:
            st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)