# frontend/registration.py
import re
import streamlit as st

st.set_page_config(page_title="Create Account", page_icon="📝", layout="centered")

# Simple CSS for card look + gradient header
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(to right, #00FF87, #60EFFF); }
    .card { background: rgba(255,255,255,0.9); padding:18px; border-radius:12px; box-shadow:0 6px 18px rgba(0,0,0,0.06); }
    .hint { color: #6b7280; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

def valid_email(s: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", s or ""))

def password_issues(pw: str) -> list:
    issues = []
    if len(pw) < 8:
        issues.append("At least 8 characters.")
    if not re.search(r"[A-Z]", pw):
        issues.append("At least one uppercase letter.")
    if not re.search(r"\d", pw):
        issues.append("At least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
        issues.append("At least one special character (e.g. !@#$%).")
    return issues

# Ensure registered_users exists in session_state (keeps runtime persistence)
if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {}

st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("Create your account")
st.markdown("<div class='hint'>Quick & secure sign-up — use a real email</div>", unsafe_allow_html=True)

with st.form("reg_form"):
    full_name = st.text_input("Full name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", help="Min 8 chars, uppercase, number, special")
    confirm = st.text_input("Confirm password", type="password")
    submitted = st.form_submit_button("Create account")

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    errors = []
    if not full_name.strip():
        errors.append("Full name is required.")
    if not valid_email(email):
        errors.append("Please enter a valid email.")
    pw_issues = password_issues(password)
    if pw_issues:
        errors += pw_issues
    if password != confirm:
        errors.append("Password and confirm password do not match.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        users = st.session_state["registered_users"]
        if email in users:
            st.error("An account with this email already exists. Try logging in or use a different email.")
        else:
            # Save user in session state (replace with DB/hashing later)
            users[email] = {"full_name": full_name.strip(), "password": password}
            st.success("Account created successfully! You can now go to Login and sign in.")
            st.info("Saved to session_state (runtime only). Not persisted to disk or DB.")
            # Optionally show quick preview
            st.write("You registered:", {"email": email, "full_name": full_name})