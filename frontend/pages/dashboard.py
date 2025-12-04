import streamlit as st

st.set_page_config(page_title="Dashboard")

if "user_name" not in st.session_state:
    st.error("You are not logged in!")
    st.stop()

st.title("Welcome to Your Dashboard 👋")
st.success(f"Hello {st.session_state['user_name']}! You are logged in as {st.session_state['user_email']}.")

if st.button("Log out"):
    st.session_state.clear()
    st.switch_page("login.py")