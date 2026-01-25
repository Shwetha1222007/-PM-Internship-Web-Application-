# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import time
from datetime import date
from database import create_tables, get_connection
from auth import register_user, login_user
from email_service import send_hr_announcement, send_update_to_candidate
from ai_engine import ai_filter_candidates

# -------------------- CONFIGURATION --------------------
st.set_page_config(
    page_title="PM Internship Scheme | Govt of India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- GLOBAL CSS (DARK THEME FIXED) --------------------
st.markdown("""
<style>
    /* GLOBAL DARK THEME */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700;800&display=swap');
    
    :root {
        --primary: #ffb703; /* Updated to user's badge color */
        --secondary: #0b3c5d; 
        --bg-dark: #0e1a2b;  /* User's requested background */
        --card-bg: #16263f;  /* User's requested secondary/card */
        --text-white: #ffffff;
        --text-gray: #ccc;
        --input-bg: #203250;
    }

    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: var(--bg-dark);
        color: var(--text-white);
    }
    
    /* REMOVE DEFAULT PADDING */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
        max-width: 100% !important;
    }

    /* CUSTOM HEADER (DARK MODE) */
    .header-container {
        position: relative;
        background-color: var(--card-bg);
        padding: 15px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 3px solid var(--primary);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        border-radius: 8px;
        margin-bottom: 30px;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .emblem-img {
        height: 60px;
        width: auto;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.2));
    }
    
    .header-titles h3 {
        color: var(--text-white);
        font-weight: 800;
        font-size: 16px;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .header-titles p {
        color: var(--text-gray);
        font-size: 12px;
        margin: 4px 0 0 0;
        font-weight: 600;
    }
    
    .header-center {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
    }
    
    .main-title {
        background: linear-gradient(to right, #ffb703, #ffdd7d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 26px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Responsive Header */
    @media (max-width: 800px) {
        .header-center { position: static; transform: none; margin-top: 15px; }
        .header-container { flex-direction: column; text-align: center; }
        .header-left { flex-direction: column; }
    }

    /* BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, #d48f00 100%);
        color: #000;
        border: none;
        padding: 12px 24px;
        border-radius: 30px; /* Matching user's badge style */
        font-weight: 700;
        font-size: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 183, 3, 0.4);
        color: #000;
        border: none;
    }

    /* CARDS */
    .custom-card {
        background-color: var(--card-bg);
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #333;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        margin-bottom: 25px;
    }
    
    /* INPUT FIELDS (Streamlit Overrides) */
    div[data-baseweb="input"] {
        background-color: var(--input-bg) !important;
        border-radius: 8px !important;
        border: 1px solid #444 !important;
        color: white !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
        border-color: #444 !important;
        color: white !important;
    }
    
    h1, h2, h3 { color: white !important; }
    p, label { color: #ccc !important; }

    /* DASHBOARD */
    .stat-box {
        background: #16263f;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #3a3f55;
        transition: transform 0.2s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stat-box:hover { transform: translateY(-5px); border-color: var(--primary); }
    
    .stat-num { font-size: 2.2rem; font-weight: bold; color: var(--primary); }
    .stat-lbl { font-size: 0.9rem; color: #aaa; text-transform: uppercase; margin-top: 5px; }
    
    /* STATUS PAGE SPECIFIC */
    .status-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        text-align: center;
    }
    .status-icon { font-size: 80px; margin-bottom: 20px; }

</style>
""", unsafe_allow_html=True)


# -------------------- INITIALIZATION --------------------
create_tables()

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
if "popup_status" not in st.session_state:
    st.session_state.popup_status = None

# -------------------- COMPONENT FUNCTIONS --------------------

def render_header():
    # Use unsafe_allow_html=True is CRITICAL here
    st.markdown("""
        <div class="header-container">
            <div class="header-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" class="emblem-img">
                <div class="header-titles">
                    <h3>Government of India</h3>
                    <p>Ministry of Corporate Affairs</p>
                </div>
            </div>
            
            <div class="header-center">
                <div class="main-title">PM Internship Scheme</div>
            </div>
            
            <div style="width: 100px;"></div>
        </div>
    """, unsafe_allow_html=True)

# -------------------- ACTION HANDLER & PAGE --------------------

def render_status_page(status, candidate_name, company):
    render_header()
    
    color = "#28a745" if status == "Selected" else "#dc3545"
    icon = "✅" if status == "Selected" else "🚫"
    title = "Application Approved" if status == "Selected" else "Application Declined"
    msg = f"Candidate <strong>{candidate_name}</strong> has been successfully <strong>{status}</strong> for <strong>{company}</strong>."
    
    st.markdown(f"""
        <div class="status-container">
            <div class="custom-card" style="border-top: 5px solid {color}; max-width: 600px; margin: 0 auto;">
                <div class="status-icon">{icon}</div>
                <h1 style="color: {color} !important; margin-bottom: 15px;">{title}</h1>
                <p style="font-size: 1.2rem; color: #ddd !important; margin-bottom: 30px; line-height: 1.6;">
                    {msg}
                </p>
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; font-size: 0.9rem; color: #aaa !important;">
                    Review Action Recorded • Notification Sent to Candidate
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("RETURN TO PORTAL HOME"):
             st.query_params.clear()
             st.session_state.page = "home"
             st.rerun()

def handle_query_params():
    try:
        # Compatibility handling
        if hasattr(st, "query_params"):
            query_params = st.query_params
        else:
            query_params = st.experimental_get_query_params()

        action = query_params.get("action")
        cid = query_params.get("cid")
        comp = query_params.get("comp")
        
        if isinstance(action, list): action = action[0]
        if isinstance(cid, list): cid = cid[0]
        if isinstance(comp, list): comp = comp[0]

        if action and cid and comp:
            new_status = "Selected" if action == "accept" else "Rejected"
            
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT email, name FROM users WHERE id = ?", (cid,))
            user = cur.fetchone()
            
            if user:
                cur.execute("UPDATE applications SET status = ? WHERE user_id = ? AND company = ?", 
                           (new_status, cid, comp))
                if cur.rowcount > 0:
                    conn.commit()
                    send_update_to_candidate(user['email'], new_status, comp)
                conn.close()
                render_status_page(new_status, user['name'], comp)
                st.stop()
            else:
                 st.error("Invalid Candidate ID")
                 st.stop()
                 
    except Exception as e:
        conn.close() if 'conn' in locals() else None
        st.error(f"System Error: {e}")

handle_query_params()


# -------------------- MAIN PAGE CONTENT --------------------

def render_hero():
    # USER REQUESTED HERO SECTION
    st.markdown("""
    <style>
    .hero {
        padding: 80px 40px;
        text-align: center;
        background: linear-gradient(135deg,#0e1a2b,#16263f);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 1px solid #2d303e;
    }
    .hero h1 {
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 20px;
        color: white !important;
    }
    .hero p {
        font-size: 20px;
        color: #ccc;
        max-width: 800px;
        margin: auto;
    }
    .badge {
        background: #ffb703;
        color: black;
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 20px;
    }
    </style>

    <div class="hero">
        <span class="badge">Youth Empowerment Initiative 2025</span>
        <h1>Bridging Talent<br>with Opportunity</h1>
        <p>
            India's largest internship program connecting ambitious youth with top 500 companies.
            Experience real-world projects and build your future.
        </p>
    </div>
    """, unsafe_allow_html=True)

def home():
    render_header()
    render_hero()
    
    c1, mid, c2 = st.columns([1, 1.5, 1])
    with mid:
        col_login, col_reg = st.columns(2)
        with col_login:
            if st.button("LOGIN TO PORTAL", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        with col_reg:
            if st.button("REGISTER NOW", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1: st.markdown('<div class="stat-box"><div class="stat-num">1.25 Cr</div><div class="stat-lbl">Annual Internships</div></div>', unsafe_allow_html=True)
    with s2: st.markdown('<div class="stat-box"><div class="stat-num">500+</div><div class="stat-lbl">Partner Companies</div></div>', unsafe_allow_html=True)
    with s3: st.markdown('<div class="stat-box"><div class="stat-num">₹5,000</div><div class="stat-lbl">Monthly Stipend</div></div>', unsafe_allow_html=True)
    with s4: st.markdown('<div class="stat-box"><div class="stat-num">100%</div><div class="stat-lbl">Digital Process</div></div>', unsafe_allow_html=True)

    # Note: Images in HTML need to refer to online sources since local relative paths in st.markdown often break unless served.
    # Using logo placeholders for stability.
    st.markdown("""
        <style>
        .partner-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-top: 50px; }
        .partner-item { background: white; padding: 20px; border-radius: 12px; height: 100px; display: flex; align-items: center; justify-content: center; opacity: 0.9; }
        .partner-item img { max-height: 50px; max-width: 100%; }
        </style>
        <h2 style="text-align:center; margin-top:80px; margin-bottom: 20px; color: var(--primary) !important; text-transform: uppercase; font-size: 1.2rem; letter-spacing: 2px;">Top Industry Partners</h2>
        <div class="partner-grid">
            <div class="partner-item"><img src="https://upload.wikimedia.org/wikipedia/en/3/30/REC_Limited_logo.png" alt="REC"></div>
            <div class="partner-item"><img src="https://upload.wikimedia.org/wikipedia/commons/3/3b/JSW_Group_logo.svg" alt="JSW"></div>
            <div class="partner-item"><img src="https://upload.wikimedia.org/wikipedia/en/b/b3/GAIL_Logo.png" alt="GAIL"></div>
            <div class="partner-item"><img src="https://upload.wikimedia.org/wikipedia/commons/4/43/Cognizant_logo_2022.svg" alt="Cognizant"></div>
            <div class="partner-item"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/L%26T.png/640px-L%26T.png" alt="L&T"></div>
        </div>
    """, unsafe_allow_html=True)

def register():
    render_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: var(--primary) !important; margin-bottom: 30px;'>Candidate Registration</h2>", unsafe_allow_html=True)
        
        with st.form("reg_form"):
            st.markdown("### 1. Personal Details", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name")
            dob = c2.date_input("Date of Birth")
            
            c3, c4 = st.columns(2)
            email = c3.text_input("Email Address")
            phone = c4.text_input("Mobile Number")
            
            st.markdown("### 2. Demographics & Identity", unsafe_allow_html=True)
            c5, c6 = st.columns(2)
            aadhaar = c5.text_input("Aadhaar Number")
            category = c6.selectbox("Social Category", ["General", "OBC", "SC", "ST"])
            
            c7, c8 = st.columns(2)
            district = c7.text_input("District")
            rural = c8.selectbox("Area Type", ["Urban", "Rural"])
            
            address = st.text_area("Full Address")
            password = st.text_input("Choose Password", type="password")
            
            if st.form_submit_button("CREATE ACCOUNT", use_container_width=True):
                success = register_user((name, email, phone, password, str(dob), district, rural, category, aadhaar, address, "N/A", "N/A"))
                if success:
                    st.success("Registration Successful! Please Login.")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("Registration failed. Email might already exist.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("← Back to Home"):
            st.session_state.page = "home"
            st.rerun()

def login():
    render_header()
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color: white !important;'>Official Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888 !important;'>Access your dashboard</p>", unsafe_allow_html=True)
        
        email = st.text_input("Email ID")
        password = st.text_input("Password", type="password")
        
        if st.button("SECURE LOGIN", use_container_width=True):
            user = login_user(email, password)
            if user:
                st.session_state.user = dict(user)
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid Username or Password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Back Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def dashboard():
    render_header()
    user = st.session_state.user
    
    conn = get_connection()
    app = conn.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user['id'],)).fetchone()
    conn.close()

    if app and not st.session_state.show_popup:
        status_key = f"pop_{app['id']}_{app['status']}"
        if app['status'] in ['Selected', 'Rejected'] and status_key not in st.session_state:
            st.session_state.show_popup = True
            st.session_state.popup_status = app['status']
            st.session_state[status_key] = True

    if st.session_state.show_popup:
        msg = f"Congratulations! You have been selected by {app['company']}!" if st.session_state.popup_status == "Selected" else "Your application was not shortlisted."
        st.info(f"🔔 UPDATE: {msg}")
        if st.button("Dismiss Notification"):
            st.session_state.show_popup = False
            st.rerun()

    left, right = st.columns([1, 2.5])
    
    with left:
        st.markdown(f"""
        <div class="custom-card" style="text-align:center;">
            <div style="width: 80px; height: 80px; background: #262a36; border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 30px; border: 2px solid var(--primary);">👤</div>
            <h3 style="margin:0; color:white !important;">{user['name']}</h3>
            <p style="color:#aaa !important; font-size: 0.9rem;">{user['email']}</p>
            <hr style="border-color: #444; margin: 20px 0;">
            <div style="text-align:left; font-size:14px; color:#ccc; line-height: 1.8;">
                <p>📍 {user['address'][:40] if user['address'] else 'N/A'}</p>
                <p>🆔 {user['aadhaar']}</p>
                <p>📱 {user['phone']}</p>
                <p>🎓 Category: {user['social_category']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("LOGOUT"):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()

    with right:
        st.markdown("<h2 style='margin-top:0; color:white !important;'>Application Dashboard</h2>", unsafe_allow_html=True)
        
        if app:
            status = app['status']
            if status == "Applied":
                clr, msg = "#f9ab00", "Under Review"
            elif status == "Selected":
                clr, msg = "#28a745", "Offer Received"
            else:
                clr, msg = "#dc3545", "Not Selected"
            
            st.markdown(f"""
            <div class="custom-card" style="border-left: 5px solid {clr};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 style="margin:0; color:{clr} !important;">{app['company']}</h2>
                        <p style="margin:5px 0 0 0; color:#ddd !important; font-weight: 500;">Sector: {app['sector']}</p>
                        <p style="margin:5px 0 0 0; color:#aaa !important; font-size: 0.9rem;">Skillset: {app['skills']}</p>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:{clr}; color:{'#fff' if status != 'Applied' else '#000'}; padding:8px 16px; border-radius:20px; font-weight:bold; font-size:14px;">
                            {status.upper()}
                        </span>
                        <p style="margin:10px 0 0 0; font-size:12px; color:#666 !important;">Applied on: {app['created_at']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if status == "Selected":
                st.balloons()
                st.success("Please check your email for the offer letter and joining instructions.")
            elif status == "Rejected":
                 st.markdown("""
                 <div style='background: rgba(220, 53, 69, 0.1); border: 1px solid #dc3545; padding: 15px; border-radius: 8px; color: #ffcccc;'>
                    We encourage you to upskill and apply for other opportunities.
                 </div>
                 """, unsafe_allow_html=True)

            if status != "Applied":
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("SUBMIT NEW APPLICATION"):
                    st.session_state.page = "apply"
                    st.rerun()
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; border: 2px dashed #444; padding: 50px;">
                <h3 style="color: #888 !important;">No Active Applications</h3>
                <p style="color: #666 !important; margin-bottom: 20px;">You haven't applied to any companies yet.</p>
                <div style="color: var(--primary); font-size: 3rem; margin-bottom: 20px;">📝</div>
                <p style="color:#aaa !important;">Thousands of opportunities are waiting for you.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("START APPLICATION PROCESS", type="primary"):
                st.session_state.page = "apply"
                st.rerun()

def apply():
    render_header()
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='color:var(--primary) !important; margin-bottom: 20px;'>New Internship Application</h2>", unsafe_allow_html=True)
        
        with st.form("app_form"):
            c1, c2 = st.columns(2)
            sector = c1.selectbox("Preferred Sector", ["IT & Software", "Finance & Banking", "Manufacturing", "Energy", "Infrastructure"])
            company = c2.selectbox("Target Company", ["REC Limited", "JSW Steel", "GAIL India", "Cognizant", "Larsen & Toubro"])
            
            c3, c4 = st.columns(2)
            college = c3.text_input("College/Institute Name")
            cgpa = c4.number_input("Current CGPA", max_value=10.0, step=0.1)
            
            skills = st.text_area("Key Skills (Comma separated)")
            col_pref = st.text_input("Preferred Location")
            
            if st.form_submit_button("SUBMIT APPLICATION", use_container_width=True):
                conn = get_connection()
                conn.execute("INSERT INTO applications (user_id, skills, sector, company, location_pref, college_name, cgpa, status) VALUES (?,?,?,?,?,?,?,?)",
                            (st.session_state.user['id'], skills, sector, company, col_pref, college, cgpa, "Applied"))
                conn.commit()
                conn.close()
                
                send_hr_announcement(st.session_state.user, {
                    'skills': skills, 'sector': sector, 'company': company, 
                    'college_name': college, 'cgpa': cgpa, 'languages': 'English, Hindi'
                })
                
                st.success("Application Submitted Successfully!")
                st.session_state.page = "dashboard"
                st.rerun()
                
        if st.button("Cancel"):
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ROUTER --------------------
if st.session_state.page == "home":
    home()
elif st.session_state.page == "register":
    register()
elif st.session_state.page == "login":
    login()
elif st.session_state.page == "dashboard":
    dashboard()
elif st.session_state.page == "apply":
    apply()
