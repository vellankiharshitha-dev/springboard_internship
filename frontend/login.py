import streamlit as st
from utils.database import SessionLocal, User
from backend.auth import check_password

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: url('https://cdn5.f-cdn.com/contestentries/1578585/21468461/5d62b49ac544b_thumb900.jpg') 
    no-repeat center fixed;
    background-size: cover;
}
.login-card {
    background: rgba(255,255,255,0.92);
    margin: 60px auto;
    padding: 30px 35px;
    width: 420px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='login-card'>", unsafe_allow_html=True)

st.title("Welcome back")
st.caption("Sign in to your account")

# ---------------- Form ----------------
with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Sign in")

if submit:
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            st.error("User not found.")
        elif not check_password(password, user.hashed_password):
            st.error("Incorrect password.")
        else:
            st.success(f"Login successful. Welcome, {user.full_name}!")

            # Store session
            st.session_state["user_name"] = user.full_name
            st.session_state["user_email"] = user.email

            st.switch_page("pages/dashboard.py")
    finally:
        db.close()

st.markdown("</div>", unsafe_allow_html=True)