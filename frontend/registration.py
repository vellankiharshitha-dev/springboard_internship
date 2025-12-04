import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from utils.database import SessionLocal, init_db, User
from backend.auth import hash_password, check_password

# Ensure DB and tables exist
init_db()

st.set_page_config(page_title="Register", page_icon="🔐")
st.title("User Registration")

with st.form("register_form"):
    full_name = st.text_input("Full name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Register")

if submitted:
    if not full_name or not email or not password:
        st.error("Please fill all fields.")
    else:
        db = SessionLocal()
        try:
            exists = db.query(User).filter_by(email=email).first()
            if exists:
                st.error("A user with this email already exists.")
            else:
                hashed = hash_password(password)
                user = User(full_name=full_name, email=email, hashed_password=hashed)
                db.add(user)
                db.commit()
                st.success("Registration successful!")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            db.rollback()
        finally:
            db.close()
