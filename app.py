import streamlit as st
from database import create_tables
from auth import register_user, login_user

create_tables()

st.set_page_config(page_title="PM Internship Scheme")

if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# ---------------- LOGIN ----------------
if menu == "Login":
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.success("Login Successful!")
        else:
            st.error("Invalid credentials")

# ---------------- REGISTER ----------------
if menu == "Register":
    st.title("📝 PM Internship Registration")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    district = st.text_input("District")
    rural = st.selectbox("Rural / Aspirational", ["Yes", "No"])
    category = st.selectbox("Social Category", ["SC", "ST", "OBC", "General"])
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        register_user((name,email,phone,district,rural,category,password))
        st.success("Registration Completed! Please Login.")
