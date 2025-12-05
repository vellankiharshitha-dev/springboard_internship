# frontend/dashboard.py
import streamlit as st
import os, json
from datetime import datetime

st.set_page_config(page_title="Dashboard", layout="wide")

# ---------- styling (same-ish gradient) ----------
st.markdown(
    """
    <style>
    .stApp {
      background: linear-gradient(135deg, #B5C7F2 0%, #E8D3FF 100%) !important;
      min-height: 100vh !important;
      padding-top: 28px;
    }
    .dash-card {
      max-width: 900px;
      margin: 18px auto;
      padding: 26px;
      background: rgba(255,255,255,0.94);
      border-radius: 14px;
      box-shadow: 0 14px 36px rgba(0,0,0,0.10);
      border: 1px solid rgba(0,0,0,0.03);
    }
    .profile-box { padding: 14px; border-radius: 10px; background: #fbfbff; }
    .small { color:#555; font-size:13px; }
    .user-item { padding:10px; border-bottom: 1px solid rgba(0,0,0,0.04); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- helper: load users (optional list display) ----------
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

# ---------- session / auth check ----------
user = st.session_state.get("user", None)

if not user:
    # not logged-in view
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.title("Dashboard")
    st.markdown("## You are not signed in")
    st.markdown("This dashboard requires you to sign in first.")
    st.markdown("- To sign in, run the login page: streamlit run frontend/login.py")
    st.markdown("- Or open the registration page to create an account: streamlit run frontend/registration.py")
    st.markdown("")
    if st.button("Open login page (instructions)"):
        st.info("Open a terminal and run: streamlit run frontend/login.py — then sign in. After sign-in you'll return here.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------- logged-in view ----------
st.markdown("<div class='dash-card'>", unsafe_allow_html=True)

# Header row: welcome + quick actions
col1, col2 = st.columns([3,1])
with col1:
    st.title(f"Welcome, {user.get('full_name','User').split()[0]} 👋")
    st.markdown(f"<div class='small'>Signed in as: <strong>{user.get('email')}</strong></div>", unsafe_allow_html=True)
with col2:
    if st.button("Log out"):
        st.session_state["user"] = None
        st.experimental_rerun()

st.divider()

# Profile / details
st.subheader("Your profile")
st.markdown("<div class='profile-box'>", unsafe_allow_html=True)
st.markdown(f"*Full name:* {user.get('full_name')}")
st.markdown(f"*Email:* {user.get('email')}")
created = user.get("created_at", None)
if created:
    st.markdown(f"*Account created:* {created}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")
st.subheader("Quick actions")
colA, colB, colC = st.columns(3)
with colA:
    if st.button("Edit profile (demo)"):
        st.info("Profile edit not implemented in this demo. We can add this next.")
with colB:
    if st.button("Change password (demo)"):
        st.info("Password change not implemented in this demo. We can add it on request.")
with colC:
    if st.button("Show my data file"):
        st.write(f"users.json location: {USERS_FILE}")

st.markdown("")
st.divider()

# Optional: show list of registered users (email masked) for demo/mentor view
st.subheader("Registered users (demo view)")
users = load_users()
if not users:
    st.info("No users found (users.json empty).")
else:
    # limited, sanitized display
    for u in users:
        # mask email for privacy a bit (show prefix first char, then ...)
        email = u.get("email","")
        if "@" in email:
            prefix, domain = email.split("@",1)
            masked = (prefix[0] + "" + prefix[-1]) if len(prefix)>2 else (prefix[0]+"")
            masked = masked + "@" + domain
        else:
            masked = email
        st.markdown(f"<div class='user-item'><strong>{u.get('full_name','-')}</strong> — <span class='small'>{masked}</span></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)