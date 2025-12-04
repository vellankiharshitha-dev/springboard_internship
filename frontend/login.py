import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from utils.database import SessionLocal, User
from backend.auth import check_password

st.set_page_config(page_title="Login", page_icon="🔑")
st.title("User Login")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    if not email or not password:
        st.error("Please fill all fields.")
    else:
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(email=email).first()
            if not user:
                st.error("User not found.")
            else:
                if check_password(password, user.hashed_password):
                    st.success(f"Login successful! Welcome {user.full_name} 🎉")
                else:
                    st.error("Incorrect password.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            db.close()
