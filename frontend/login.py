# frontend/login.py
import re
import streamlit as st

# ---------------- page + css ----------------
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: #86a7b8; background: linear-gradient(90deg, rgba(134, 167, 184, 1) 32%, rgba(87, 199, 133, 1) 50%, rgba(237, 221, 83, 1) 100%); }
    .css-18e3th9 { padding-top: 1rem; padding-bottom: 1rem; }
    .login-card { background: rgba(255,255,255,0.88); border-radius:12px; padding:18px; box-shadow:0 6px 18px rgba(0,0,0,0.08); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- helpers ----------------
def valid_email(s: str) -> bool:
    if not s:
        return False
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", s) is not None

# ---------------- dashboard renderer ----------------
def render_dashboard():
    st.success(f"You're logged in — welcome, {st.session_state.get('user', {}).get('full_name','User')}!")
    st.markdown("---")
    st.header("Dashboard (demo)")
    st.write("This is a placeholder dashboard. Replace with your real dashboard code.")
    st.write("You can add charts, tables, or navigation controls here.")
    if st.button("Log out"):
        # clear session and stop
        st.session_state.pop("logged_in", None)
        st.session_state.pop("user", None)
        st.success("You have been logged out. Refresh the page if necessary.")
        st.stop()

# ---------------- if already logged in ----------------
if st.session_state.get("logged_in"):
    render_dashboard()
    st.stop()

# ---------------- login UI ----------------
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown("## Welcome back")
st.markdown("Sign in to your account")

with st.form("login_form", clear_on_submit=False):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Sign in")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- handle submit ----------------
if submitted:
    errors = []
    if not valid_email(email):
        errors.append("Please enter a valid email address.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        # re-read registered users from session_state at submit time
        users = st.session_state.get("registered_users")
        if not users:
            st.error("No registered users found. Please register first using the Create Account page.")
        else:
            user = users.get(email)
            if not user:
                st.error("No account found with that email. Please register first.")
            else:
                # Plaintext compare (demo). Replace with hashed check in production.
                if user.get("password", "") != password:
                    st.error("Incorrect password.")
                else:
                    st.success(f"Welcome back, {user.get('full_name','User')}!")
                    st.session_state["user"] = {"email": email, "full_name": user.get("full_name")}
                    st.session_state["logged_in"] = True
                    # render dashboard immediately then stop
                    render_dashboard()
                    st.stop()