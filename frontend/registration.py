import streamlit as st
import re
from utils.database import SessionLocal, User
from backend.auth import hash_password

# -------------------- CSS (minimal + no top space) --------------------
st.markdown("""
<style>
body {
    background: url('https://t3.ftcdn.net/jpg/02/92/90/56/360_F_292905667_yFUJNJPngYeRNlrRL4hApHWxuYyRY4kN.jpg') 
    no-repeat center fixed;
    background-size: cover;
}
.reg-card {
    background: rgba(255,255,255,0.92);
    margin: 40px auto;
    padding: 30px 35px;
    width: 420px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
.stTextInput>div>div>input {
    border-radius: 10px !important;
    background: #f1f4f9 !important;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: #3b82f6;
    color: white;
    height: 42px;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='reg-card'>", unsafe_allow_html=True)

st.title("Create Account")
st.caption("Quick, secure registration — please use a real email.")

# -------------------- VALIDATION FUNCTIONS --------------------
def valid_email(e: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", e))

def valid_password(p: str):
    if len(p) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", p):
        return False, "Add at least one uppercase letter."
    if not re.search(r"\d", p):
        return False, "Add at least one digit."
    if not re.search(r"[^\w\s]", p):
        return False, "Add at least one special character."
    return True, ""

# -------------------- FORM --------------------
with st.form("reg_form"):
    full_name = st.text_input("Full name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", help="Min 8 chars, upper, digit, special")
    confirm = st.text_input("Confirm password", type="password")
    submit = st.form_submit_button("Sign up")

# -------------------- SUBMIT LOGIC --------------------
if submit:
    if not full_name or not email or not password or not confirm:
        st.error("Please fill all fields.")
    elif not valid_email(email):
        st.error("Invalid email address.")
    elif password != confirm:
        st.error("Passwords do not match.")
    else:
        ok, msg = valid_password(password)
        if not ok:
            st.error(msg)
        else:
            db = SessionLocal()
            try:
                exists = db.query(User).filter_by(email=email).first()
                if exists:
                    st.error("Email already registered.")
                else:
                    new_user = User(
                        full_name=full_name,
                        email=email,
                        hashed_password=hash_password(password)
                    )
                    db.add(new_user)
                    db.commit()
                    st.success("Registration successful! You can now log in.")
            except Exception as e:
                db.rollback()
                st.error(f"Unexpected error: {e}")
            finally:
                db.close()

st.markdown("</div>", unsafe_allow_html=True)