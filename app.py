# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
from datetime import date
from database import create_tables, get_connection
from auth import register_user, login_user
from email_service import send_hr_announcement, send_update_to_candidate
from ai_engine import ai_filter_candidates

# -------------------- INITIALIZATION --------------------
create_tables()

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="PM Internship Scheme - Official Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- SESSION STATE --------------------
for key in ["page", "user", "show_popup", "popup_status"]:
    if key not in st.session_state:
        if key == "page": st.session_state[key] = "home"
        elif key == "show_popup": st.session_state[key] = False
        else: st.session_state[key] = None

# -------------------- CUSTOM CSS (DARK THEME + OLD STYLE) --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #f9ab00;
    --primary-dim: #d48f00;
    --bg-dark: #0e1117;
    --card-bg: #262730;
    --text-light: #ffffff;
    --text-muted: #a0a0a0;
    --border-color: #3d3d3d;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-light);
}

/* --- GOVT HEADER (Refined for Dark Mode) --- */
.govt-header {
    background: var(--card-bg);
    padding: 18px 60px;
    border-bottom: 2px solid var(--primary);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

.govt-logo {
    display: flex;
    align-items: center;
    gap: 20px;
}

.govt-title-main {
    font-size: 1.1rem;
    font-weight: 800;
    color: white;
    margin: 0;
    text-transform: uppercase;
}

.govt-title-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin: 2px 0 0 0;
}

/* --- HERO SECTION --- */
.hero-container {
    background: radial-gradient(circle at top left, #1f2937, #111827);
    padding: 100px 40px;
    text-align: center;
    border-radius: 30px;
    margin-bottom: 50px;
    border: 1px solid var(--border-color);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

.hero-badge {
    background: rgba(249, 171, 0, 0.2);
    color: var(--primary);
    padding: 8px 18px;
    border-radius: 100px;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 20px;
    border: 1px solid var(--primary);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    margin-bottom: 20px;
    background: linear-gradient(to right, #ffffff, #aaaaaa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* --- CARDS --- */
.dash-card {
    background: var(--card-bg);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: transform 0.3s;
}

.dash-card:hover {
    transform: translateY(-5px);
    border-color: var(--primary);
}

.stat-card {
    background: var(--card-bg);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid var(--border-color);
}
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--primary);
}
.stat-label {
    font-size: 0.9rem;
    color: var(--text-muted);
    text-transform: uppercase;
}

/* --- BUTTONS --- */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    background-color: var(--primary) !important;
    color: black !important;
    border: none !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background-color: white !important;
    transform: scale(1.02);
}

/* --- POPUP --- */
.modal-overlay {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: #1a1c24;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    z-index: 10000;
    border: 3px solid var(--primary);
    box-shadow: 0 0 100px rgba(0,0,0,0.8);
    width: 90%;
    max-width: 500px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- COMPONENTS --------------------

def render_header():
    # CSS for the White Header + Navy Border
    st.markdown("""
        <style>
            /* Header Container */
            .custom-header {
                background-color: #ffffff;
                padding: 15px 30px;
                border-bottom: 4px solid #0b3c5d;
                border-radius: 8px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                position: relative;
                overflow: hidden;
            }
            
            /* Left Side: Emblem + Text */
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .header-emblem {
                width: 55px;
                height: auto;
            }
            .govt-text {
                font-family: 'Arial', sans-serif;
                color: #333;
                line-height: 1.3;
                font-size: 0.85rem;
                font-weight: 700;
                border-left: 2px solid #ddd;
                padding-left: 15px;
            }
            
            /* Center: Title */
            .header-center {
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
                text-align: center;
                color: #0b3c5d;
                font-family: 'Arial', sans-serif;
                font-weight: 800;
                font-size: 1.4rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                width: 100%;
                pointer-events: none; /* Let clicks pass through if needed */
            }
            
            /* Right Side Spacer */
            .header-right-spacer {
                width: 250px; /* Space for buttons */
            }

            /* Button Styling overrides for the header area */
            .stButton button {
                background-color: #f9ab00 !important;
                color: #000 !important;
                border: none !important;
                font-weight: bold !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
            }
            .stButton button:hover {
                background-color: #ffc107 !important;
                color: #000 !important;
            }
        </style>
        
        <!-- HTML Structure -->
        <div class="custom-header">
            <div class="header-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/800px-Emblem_of_India.svg.png" class="header-emblem">
                <div class="govt-text">
                    <div>Government of India</div>
                    <div>Ministry of Corporate Affairs</div>
                </div>
            </div>
            
            <!-- Centered Title (Visually centered relative to container) -->
            <div class="header-center">
                Pradhan Mantri Internship Scheme
            </div>
            
            <div class="header-right-spacer"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Buttons Overlay (Using negative margin to pull them up into the header)
    if st.session_state.user is None:
        # Create columns that align with the right side
        # Structure: [Spacer, Login, Register]
        c1, c2, c3 = st.columns([6, 1, 1])
        
        # We use a container with negative top margin
        with st.container():
            st.markdown("""
                <style>
                div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
                    /* Identify the specific block if possible, mostly relies on order */
                }
                </style>
                <div style="margin-top: -85px; position: relative; z-index: 999; pointer-events: auto;">
            """, unsafe_allow_html=True)
            
            with c2:
                if st.button("Login", key="hdr_btn_login"):
                    st.session_state.page = "login"
                    st.rerun()
            with c3:
                if st.button("Register", key="hdr_btn_reg"):
                    st.session_state.page = "register"
                    st.rerun()
                    
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # User Logged In Display
        st.markdown(f"""
            <div style="margin-top: -75px; float: right; position: relative; z-index: 999; margin-right: 40px; color: #0b3c5d; font-weight: bold; background: #eef; padding: 5px 15px; border-radius: 20px;">
                👤 {st.session_state.user['name']}
            </div>
            <div style="clear: both; margin-bottom: 30px;"></div>
        """, unsafe_allow_html=True)

# -------------------- PAGES --------------------

def home_page():
    render_header()
    
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">YOUTH EMPOWERMENT 2024</div>
        <div class="hero-title">Future Ready India</div>
        <p style="color: #bbb; font-size: 1.2rem; max-width: 600px; margin: 0 auto 40px;">
            Connecting the youth with top 500 companies for a brighter tomorrow. 
            Register now for 12-month paid internships.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, mid, c2 = st.columns([1, 2, 1])
    with mid:
        col_reg, col_log = st.columns(2)
        with col_reg:
            if st.button("REGISTER NOW", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        with col_log:
            if st.button("LOGIN PORTAL", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

    st.markdown("<br><h3 style='text-align: center; color: var(--primary);'>Industry Leaders</h3>", unsafe_allow_html=True)
    
    logos = [
        "https://upload.wikimedia.org/wikipedia/en/3/30/REC_Limited_logo.png",
        "https://upload.wikimedia.org/wikipedia/commons/3/3b/JSW_Group_logo.svg",
        "https://upload.wikimedia.org/wikipedia/en/b/b3/GAIL_Logo.png",
        "https://upload.wikimedia.org/wikipedia/commons/4/43/Cognizant_logo_2022.svg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/L%26T.png"
    ]
    cols = st.columns(5)
    for i, l in enumerate(logos):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card" style="padding: 10px;">
                <img src="{l}" style="max-height: 40px; filter: brightness(0) invert(1);">
            </div>
            """, unsafe_allow_html=True)

    # Stats
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="stat-card"><div class="stat-value">1 Cr</div><div class="stat-label">Internships</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-card"><div class="stat-value">500+</div><div class="stat-label">Top Companies</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-card"><div class="stat-value">₹5000</div><div class="stat-label">Stipend/Month</div></div>', unsafe_allow_html=True)


def register_page():
    render_header()
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Candidate Registration</h2>", unsafe_allow_html=True)
    
    with st.form("reg_form_dark"):
        st.markdown("#### Identity Details")
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name*")
        email = c2.text_input("Email ID*")
        
        c3, c4 = st.columns(2)
        phone = c3.text_input("Mobile*")
        password = c4.text_input("Password*", type="password")
        
        st.markdown("#### Demographics")
        c5, c6, c7 = st.columns(3)
        dob = c5.date_input("Date of Birth")
        district = c6.text_input("District")
        rural = c7.selectbox("Region", ["Urban", "Rural"])
        
        c8, c9 = st.columns(2)
        category = c8.selectbox("Category", ["General", "OBC", "SC", "ST"])
        aadhaar = c9.text_input("Aadhaar No.")
        
        st.markdown("#### Additional Info")
        address = st.text_area("Address")
        
        submit = st.form_submit_button("CREATE ACCOUNT", use_container_width=True)
        
    if submit:
        # Saving simplified for UX, mapped to DB
        register_user((name, email, phone, password, str(dob), district, rural, category, aadhaar, address, "N/A", "N/A"))
        st.session_state.page = "login"
        st.rerun()

    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def login_page():
    render_header()
    
    c1, mid, c2 = st.columns([1, 1, 1])
    with mid:
        st.markdown("<div class='dash-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h2>Login</h2>")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("LOGIN", use_container_width=True):
            user = login_user(email, password)
            if user:
                st.session_state.user = dict(user)
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials")
                
        if st.button("Back Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def dashboard_page():
    render_header()
    user = st.session_state.user
    
    # Check Status
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user['id'],))
    app = cur.fetchone()
    conn.close()

    if app and not st.session_state.show_popup:
        status_key = f"pop_dark_{app['id']}_{app['status']}"
        if app['status'] in ['Selected', 'Rejected'] and status_key not in st.session_state:
            st.session_state.show_popup = True
            st.session_state.popup_status = app['status']
            st.session_state[status_key] = True

    if st.session_state.show_popup:
        if st.session_state.popup_status == "Selected":
            show_popup_modal("Congratulations!", f"You are selected for {app['company']}!", False)
        else:
            show_popup_modal("Status Update", "Application Rejected.", True)

    s_col, m_col = st.columns([1, 2.5])
    
    with s_col:
        st.markdown(f"""
        <div class="dash-card">
            <h3 style="color: var(--primary);">My Profile</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{user['name']}</p>
            <p style="color: #aaa;">{user['email']}</p>
            <hr style="border-color: #333;">
            <p><strong>District:</strong> {user['district']}</p>
            <p><strong>Rural Status:</strong> {user['rural']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()

    with m_col:
        st.markdown("<h2>Dashboard Overview</h2>", unsafe_allow_html=True)
        
        if not app:
            st.markdown("""
            <div class="dash-card" style="text-align: center; border: 2px dashed #444;">
                <h3 style="color: #888;">No Active Applications</h3>
                <p>Apply now to start your journey.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("APPLY NOW ->", use_container_width=True):
                st.session_state.page = "apply"
                st.rerun()
        else:
            status = app['status']
            color = "#f9ab00" if status == "Applied" else ("#28a745" if status == "Selected" else "#dc3545")
            
            st.markdown(f"""
            <div class="dash-card" style="border-left: 5px solid {color};">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <h2 style="margin: 0;">{app['company']}</h2>
                        <p style="color: #aaa;">{app['sector']}</p>
                    </div>
                    <div>
                        <span style="background: {color}; color: black; padding: 5px 15px; border-radius: 10px; font-weight: bold;">
                            {status.upper()}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if status != "Applied":
                if st.button("Apply Again"):
                    st.session_state.page = "apply"
                    st.rerun()

def apply_page():
    render_header()
    user = st.session_state.user
    
    st.markdown("<div class='dash-card'>", unsafe_allow_html=True)
    st.markdown("<h2>Apply for Internship</h2>", unsafe_allow_html=True)
    
    with st.form("apply_dark"):
        c1, c2 = st.columns(2)
        sec = c1.selectbox("Sector", ["IT", "Finance", "Energy"])
        comp = c2.selectbox("Company", ["REC Limited", "JSW Steel", "GAIL India", "Cognizant"])
        
        loc = st.text_input("Location")
        skills = st.text_area("Skills")
        
        c3, c4 = st.columns(2)
        col = c3.text_input("College")
        cgpa = c4.number_input("CGPA", max_value=10.0)
        
        submit = st.form_submit_button("SUBMIT APPLICATION", use_container_width=True)
        
    if submit:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO applications (user_id, skills, sector, company, location_pref, college_name, cgpa, status) VALUES (?,?,?,?,?,?,?,?)",
                    (user['id'], skills, sec, comp, loc, col, cgpa, "Applied"))
        conn.commit()
        conn.close()
        
        send_hr_announcement(user, {'skills': skills, 'sector': sec, 'company': comp, 'college_name': col, 'cgpa': cgpa, 'languages': 'N/A'})
        st.session_state.page = "dashboard"
        st.rerun()
        
    if st.button("Cancel"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ROUTER --------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "apply":
    apply_page()
