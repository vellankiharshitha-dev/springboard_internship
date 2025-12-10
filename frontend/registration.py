import streamlit as st
from backend.auth import register_user


def load_css():
    st.markdown(
        """
        <style>
        /* Center the registration content inside the main white card */
        .reg-container {
            max-width: 150px;      
            margin: 0 auto;        
        }

        .reg-header {
            width: 70%;
            margin: 0 auto 14px auto;
            padding: 4px 5px;
            border-radius: 10px;
            background: linear-gradient(135deg, #2563eb, #ec4899);
            text-align: center;
        }
        .reg-header-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 700;
            margin: 0;
        }
        .reg-header-sub {
            color: #e5e7eb;
            font-size: 11px;
            margin: 0;
        }

        .pw-box {
            margin-top: 12px;
            padding: 10px 12px;
            border-radius: 10px;
            background: rgba(249, 250, 251, 0.96);
            border: 1px solid #e5e7eb;
            font-size: 12px;
            color: #111827;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_registration_page():
    load_css()

    st.markdown('<div class="reg-container">', unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div class="reg-header">
            <p class="reg-header-title">Create Your Account</p>
            <p class="reg-header-sub">Fill in your details to register.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Password rules 
    st.markdown(
        """
        <div class="pw-box">
            <b>Password requirements:</b><br>
            • Minimum 8 characters<br>
            • At least 1 uppercase & 1 lowercase letter<br>
            • At least 1 number<br>
            • At least 1 special character (!@#$%^&*)<br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Register"):
        success, message = register_user(full_name, email, password, confirm_password)
        if success:
            st.success(message)
            st.info("Use the Login option in the sidebar to sign in.")
        else:
            st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)