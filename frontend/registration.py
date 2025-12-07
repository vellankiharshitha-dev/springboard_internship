import streamlit as st
from backend.auth import register_user


# ------------------------------
# CUSTOM CSS FOR BEAUTIFUL UI
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

        .rule-box {
            background: #eef2f7;
            padding: 10px;
            font-size: 13px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
            border-radius: 4px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ------------------------------
# REGISTRATION PAGE UI
# ------------------------------
def show_registration_page():
    load_css()

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown('<div class="title">Create Your Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Fill the details below to register</div>', unsafe_allow_html=True)

    # Display password rules
    st.markdown(
        """
        <div class="rule-box">
        <b>Password Rules:</b><br>
        • Minimum 8 characters<br>
        • At least 1 uppercase letter<br>
        • At least 1 lowercase letter<br>
        • At least 1 number<br>
        • At least 1 special character (!@#$%^&*)<br>
        </div>
        """,
        unsafe_allow_html=True
    )

    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        success, message = register_user(full_name, email, password, confirm_password)

        if success:
            st.success(message)
            st.info("Go to the Login page from the sidebar.")
        else:
            st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)