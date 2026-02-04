# ui_styles.py
import streamlit as st

def apply_ui():
    st.markdown("""
    <style>

    .stApp {
        background: radial-gradient(circle at top, #111 0%, #000 60%);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    /* HEADER */
    .top-header {
        background: linear-gradient(to right, #0f0f0f, #1a1a1a);
        padding: 18px 40px;
        border-radius: 12px;
        border-bottom: 3px solid #ffb703;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 35px;
        box-shadow: 0 0 30px rgba(0,0,0,0.6);
    }

    .title {
        font-size: 28px;
        font-weight: 800;
        color: #ffb703;
        text-align: center;
        flex-grow: 1;
    }

    /* INPUTS */
    div[data-baseweb="input"] input {
        background: #0f0f0f !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 14px !important;
    }

    /* BUTTON */
    div.stButton > button {
        background: #111;
        border: 1px solid #333;
        color: white;
        border-radius: 12px;
        height: 50px;
        font-size: 16px;
        width: 100%;
    }

    div.stButton > button:hover {
        background: #1c1c1c;
        border: 1px solid #ffb703;
        color: #ffb703;
    }

    /* CARDS */
    .card {
        background: #111;
        padding: 35px;
        border-radius: 18px;
        border: 1px solid #2a2a2a;
        box-shadow: 0 0 40px rgba(0,0,0,0.7);
    }

    </style>
    """, unsafe_allow_html=True)


def header():
    st.markdown("""
    <div class="top-header">
        <div>
            <b>Government of India</b><br>
            <small>Ministry of Corporate Affairs</small>
        </div>
        <div class="title">PM Internship Scheme</div>
        <div style="width:120px;"></div>
    </div>
    """, unsafe_allow_html=True)
