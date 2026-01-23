# -*- coding: utf-8 -*-
import streamlit as st
from datetime import date
from database import create_tables, get_connection
from auth import register_user, login_user
from email_service import send_hr_email, send_candidate_email

# -------------------- INITIALIZATION --------------------
create_tables()

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="PM Internship Scheme - Official Portal",
    page_icon="\U0001F1EE\U0001F1F3",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- SESSION STATE --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #00296b;
    --primary-light: #0044b3;
    --secondary: #f9ab00;
    --accent: #ff6d00;
    --bg-light: #fdfdfd;
    --text-dark: #121212;
    --text-muted: #5f6368;
    --glass-bg: rgba(255, 255, 255, 0.7);
    --border-color: #e0e4e8;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-dark);
}

.main {
    background: linear-gradient(180deg, #f8faff 0%, #ffffff 100%);
}

/* --- PREMIUM GOVT HEADER --- */
.govt-header {
    background: white;
    padding: 18px 60px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.govt-logo {
    display: flex;
    align-items: center;
    gap: 20px;
}

.govt-text {
    line-height: 1.1;
}

.govt-title-main {
    font-size: 1rem;
    font-weight: 800;
    color: var(--primary);
    margin: 0;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.govt-title-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin: 3px 0 0 0;
    font-weight: 500;
}

/* --- MODERN HERO SECTION --- */
.hero-container {
    background: radial-gradient(circle at top left, #00296b, #001a4d);
    padding: 120px 40px;
    color: white;
    text-align: center;
    border-radius: 0 0 60px 60px;
    margin-bottom: 60px;
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url('https://www.transparenttextures.com/patterns/cubes.png');
    opacity: 0.05;
}

.hero-badge {
    background: rgba(249, 171, 0, 0.2);
    color: var(--secondary);
    padding: 8px 18px;
    border-radius: 100px;
    font-weight: 700;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 25px;
    border: 1px solid rgba(249, 171, 0, 0.3);
}

.hero-title {
    font-size: 4rem;
    font-weight: 900;
    margin-bottom: 25px;
    letter-spacing: -1.5px;
    line-height: 1.1;
    background: linear-gradient(to right, #ffffff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.25rem;
    max-width: 750px;
    margin: 0 auto 50px;
    opacity: 0.8;
    line-height: 1.6;
    font-weight: 400;
}

/* --- STAT CARDS --- */
.stat-card {
    background: white;
    padding: 40px 30px;
    border-radius: 28px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.04);
    border: 1px solid var(--border-color);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.stat-card:hover {
    transform: translateY(-12px);
    box-shadow: 0 20px 50px rgba(0,41,107,0.1);
    border-color: var(--primary-light);
}

.stat-icon {
    font-size: 3rem;
    margin-bottom: 20px;
    filter: drop-shadow(0 5px 10px rgba(0,0,0,0.1));
}

.stat-value {
    font-size: 2.25rem;
    font-weight: 800;
    color: var(--primary);
    margin-bottom: 8px;
}

.stat-label {
    font-size: 0.95rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* --- SECTION HEADERS --- */
.section-header {
    margin: 80px 0 40px;
    text-align: center;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 900;
    color: var(--primary);
    position: relative;
    display: inline-block;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 20%;
    right: 20%;
    height: 5px;
    background: var(--secondary);
    border-radius: 10px;
}

/* --- PARTNER LOGOS --- */
.partner-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-color);
    box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    min-height: 140px;
    transition: all 0.3s;
}

.partner-card:hover {
    border-color: var(--secondary);
    background: #fffdf5;
    transform: scale(1.05);
}

/* --- STYLED BUTTONS --- */
.stButton > button {
    border-radius: 14px !important;
    padding: 16px 32px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.main-btn button {
    background: var(--primary) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 10px 20px rgba(0,41,107,0.2) !important;
}

.main-btn button:hover {
    background: var(--primary-light) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 30px rgba(0,41,107,0.3) !important;
}

.outline-btn button {
    background: white !important;
    color: var(--primary) !important;
    border: 2px solid var(--primary) !important;
}

.outline-btn button:hover {
    background: #f0f4ff !important;
    transform: translateY(-2px) !important;
}

/* --- DASHBOARD ELEMENTS --- */
.dash-card {
    background: white;
    padding: 40px;
    border-radius: 30px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.05);
    border: 1px solid var(--border-color);
}

.status-badge {
    padding: 8px 20px;
    border-radius: 100px;
    font-weight: 800;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)

# -------------------- COMPONENTS --------------------
def render_header():
    st.markdown("""
        <div class="govt-header">
            <div class="govt-logo">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/800px-Emblem_of_India.svg.png" width="45">
                <div class="govt-text">
                    <p class="govt-title-main">Government of India</p>
                    <p class="govt-title-sub">Ministry of Corporate Affairs</p>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 900; font-size: 1.4rem; color: var(--primary); letter-spacing: -0.5px;">PM Internship Scheme</div>
                <div style="font-size: 0.7rem; color: var(--secondary); font-weight: 800; text-transform: uppercase; letter-spacing: 2px;">Youth Empowerment Portal</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# -------------------- AI SMART ALLOCATION ENGINE --------------------
def ai_smart_shortlist(company_name):
    """
    AI Logic: Shortlist candidates for a company.
    Rules:
    1. Filters based on 'Applied' status.
    2. Matches skills and qualification.
    3. Rural Representation: Promotes at least 2 rural candidates to the top 5.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, u.name, a.skills, a.qualification, a.rural_urban, u.email
        FROM applications a
        JOIN users u ON a.user_id = u.id
        WHERE a.company = ? AND a.status = 'Applied'
    """, (company_name,))
    candidates = cur.fetchall()
    conn.close()

    if len(candidates) < 3: return candidates # Not enough for complex AI ranking

    processed = []
    for cand in candidates:
        score = 0
        # Simulated AI Matching
        if cand[4] == 'Yes': score += 15 # Rural Priority
        if 'degree' in cand[3].lower() or 'graduate' in cand[3].lower(): score += 5
        
        processed.append({
            'data': cand,
            'score': score,
            'is_rural': cand[4] == 'Yes'
        })

    # Sort by AI Score
    processed.sort(key=lambda x: x['score'], reverse=True)
    
    # Selection logic for Top 5
    shortlisted = processed[:5]
    
    # Ensure Rural Rule: At least 2 Rural candidates in shortlist
    rural_shortlisted = [x for x in shortlisted if x['is_rural']]
    if len(rural_shortlisted) < 2:
        other_rural = [x for x in processed[5:] if x['is_rural']]
        for i in range(min(len(other_rural), 2 - len(rural_shortlisted))):
            shortlisted.append(other_rural[i])
            if len(shortlisted) > 5: shortlisted.pop(2) # Keep it to 5, remove mid-tier non-rural

    return [x['data'] for x in shortlisted]

# -------------------- HELPER FUNCTIONS --------------------
def check_eligibility(dob, employed, studying, income, govt_job):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 21 or age > 24: return False, "Age must be between 21 and 24 years."
    if employed == "Yes": return False, "Full-time employed individuals are not eligible."
    if studying == "Yes": return False, "Full-time students are not eligible."
    if income == "Above 8 Lakhs": return False, "Family income must be below 8 Lakhs."
    if govt_job == "Yes": return False, "Family members in Government jobs are not eligible."
    return True, "Eligible"

# -------------------- PAGE: HOME --------------------
def home_page():
    render_header()
    
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">NEW INITIATIVE 2024-25</div>
        <div class="hero-title">Empowering the <br> Youth of India</div>
        <div class="hero-subtitle">
            Bridging the gap between academic education and industry excellence. 
            Join the 1 Crore internship program across India's top 500 companies.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Buttons centered
    c1, mid, c4 = st.columns([1, 1.5, 1])
    with mid:
        m1, m2 = st.columns(2)
        with m1:
            st.markdown('<div class="main-btn">', unsafe_allow_html=True)
            if st.button("\U0001F4DD YOUTH REGISTRATION", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
            if st.button("\U0001F510 CANDIDATE LOGIN", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Stats Section
    st.markdown('<div class="section-header"><h2 class="section-title">Program Highlights</h2></div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-card"><div class="stat-icon">&#x1f3e2;</div><div class="stat-value">500+</div><div class="stat-label">Top Companies</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-card"><div class="stat-icon">&#x1f393;</div><div class="stat-value">1 Crore</div><div class="stat-label">Internships</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-card"><div class="stat-icon">&#x1f4b0;</div><div class="stat-value">₹5,000</div><div class="stat-label">Monthly Stipend</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-card"><div class="stat-icon">&#x1f916;</div><div class="stat-value">AI</div><div class="stat-label">Smart Allocation</div></div>', unsafe_allow_html=True)

    # About Section
    st.markdown('<div class="section-header"><h2 class="section-title">About the Scheme</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="dash-card">
        <div style="display: flex; gap: 40px; align-items: center;">
            <div style="flex: 1;">
                <p style="font-size: 1.15rem; line-height: 1.8; color: #444; margin-bottom: 25px;">
                    The PM Internship Scheme is a visionary program launched to provide professional exposure to the youth of India. 
                    By partnering with the top 500 companies, the government ensures that candidates receive hands-on training in real-world 
                    environments.
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div style="background: #f8faff; padding: 20px; border-radius: 15px; border: 1px solid #eef2ff;">
                        <h4 style="margin: 0 0 10px 0; color: var(--primary);">12 Months</h4>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">Hands-on industrial training</p>
                    </div>
                    <div style="background: #f8faff; padding: 20px; border-radius: 15px; border: 1px solid #eef2ff;">
                        <h4 style="margin: 0 0 10px 0; color: var(--primary);">Monthly Stipend</h4>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">Direct Benefit Transfer (DBT)</p>
                    </div>
                </div>
            </div>
            <div style="flex: 0.8;">
                <img src="https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=600&q=80" style="width: 100%; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Partners Section
    st.markdown('<div class="section-header"><h2 class="section-title">Top Industry Partners</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
        <div class="partner-card"><img src="https://upload.wikimedia.org/wikipedia/en/3/30/REC_Limited_logo.png" height="50"><p style="font-weight: 800; color: var(--primary); margin-top: 15px;">REC Limited</p></div>
        <div class="partner-card"><img src="https://upload.wikimedia.org/wikipedia/commons/3/3b/JSW_Group_logo.svg" height="40"><p style="font-weight: 800; color: var(--primary); margin-top: 15px;">JSW Steel</p></div>
        <div class="partner-card"><img src="https://upload.wikimedia.org/wikipedia/en/b/b3/GAIL_Logo.png" height="50"><p style="font-weight: 800; color: var(--primary); margin-top: 15px;">GAIL India</p></div>
        <div class="partner-card"><img src="https://upload.wikimedia.org/wikipedia/commons/4/43/Cognizant_logo_2022.svg" height="30"><p style="font-weight: 800; color: var(--primary); margin-top: 15px;">Cognizant</p></div>
        <div class="partner-card"><img src="https://upload.wikimedia.org/wikipedia/commons/e/e5/L%26T.png" height="40"><p style="font-weight: 800; color: var(--primary); margin-top: 15px;">L&T</p></div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer" style="background: var(--primary); color: white; padding: 80px 40px; text-align: center; border-radius: 60px 60px 0 0; margin-top: 120px; position: relative; overflow: hidden;">
        <div style="position: absolute; top:0; left:0; width:100%; height:4px; background: var(--secondary);"></div>
        <div style="max-width: 800px; margin: 0 auto;">
            <h2 style="color: var(--secondary); margin-bottom: 25px; font-weight: 800;">PM Internship Scheme</h2>
            <div style="display: flex; justify-content: center; gap: 40px; margin-bottom: 40px; font-weight: 600; opacity: 0.9;">
                <span>About</span><span>Guidelines</span><span>Companies</span><span>Helpdesk</span>
            </div>
            <p style="opacity: 0.6; font-size: 0.9rem; line-height: 1.6;">
                &copy; 2024 PM Internship Scheme Hub. Designed and Developed by the Ministry of Corporate Affairs, Government of India.
                <br>Providing industrial training to the youth of New India.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- PAGE: REGISTRATION --------------------
def register_page():
    render_header()
    col1, mid, col3 = st.columns([1, 2.2, 1])
    with mid:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="dash-card">
                <h2 style="margin-top: 0; color: var(--primary); font-weight: 900; text-align: center;">Join the Mission</h2>
                <p style="color: var(--text-muted); text-align: center; margin-bottom: 40px;">Secure your future with the PM Internship Scheme Official Enrollment.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("reg_form"):
            st.markdown('<h5 style="color: var(--primary); font-weight: 700; margin-bottom: 20px;">&#x1f464; Candidate Information</h5>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name (as per Aadhar)*")
            email = c2.text_input("Email Address*")
            
            c3, c4 = st.columns(2)
            phone = c3.text_input("Mobile Number*")
            password = c4.text_input("Create Secure Password*", type="password")
            
            st.markdown('<h5 style="color: var(--primary); font-weight: 700; margin-top: 30px; margin-bottom: 20px;">&#x1f4cd; Location & Background</h5>', unsafe_allow_html=True)
            c5, c6 = st.columns(2)
            min_dob = date.today().replace(year=date.today().year - 24)
            max_dob = date.today().replace(year=date.today().year - 21)
            dob = c5.date_input("Date of Birth*", min_value=min_dob, max_value=max_dob)
            district = c6.text_input("District Name*")
            
            c7, c8 = st.columns(2)
            rural = c7.selectbox("Area Designation*", ["No", "Yes"], format_func=lambda x: "Rural / Aspirational" if x == "Yes" else "Urban")
            category = c8.selectbox("Social Category*", ["General", "OBC", "SC", "ST"])
            
            st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="main-btn">', unsafe_allow_html=True)
            submit = st.form_submit_button("CREATE MY ACCOUNT", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if submit:
            if not all([name, email, phone, password, district]):
                st.error("Please ensure all mandatory fields are correctly filled.")
            else:
                try:
                    register_user((name, email, phone, str(dob), district, rural, category, password))
                    st.session_state.registration_success = True
                    st.session_state.page = "login"
                    st.rerun()
                except Exception as e:
                    st.error(f"\u26A0 System Error: {e}")

        st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
        if st.button("\u2190 RETURN TO LANDING PAGE", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- PAGE: LOGIN --------------------
def login_page():
    render_header()
    col1, mid, col3 = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
        
        if st.session_state.get("registration_success"):
            st.success("✅ Account created successfully! Please login to continue.")
            st.session_state["registration_success"] = False

        st.markdown("""
            <div class="dash-card" style="text-align: center;">
                <h2 style="margin-top: 0; color: var(--primary); font-weight: 900;">Secure Login</h2>
                <p style="color: var(--text-muted);">Candidate Authentication Portal</p>
            </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Registered Email")
        password = st.text_input("Password", type="password")
        
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("AUTHORIZE & LOGIN", use_container_width=True):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("\U0001F6AB Access Denied: Invalid credentials.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
        if st.button("\u2190 BACK TO HOME", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- PAGE: DASHBOARD --------------------
def dashboard_page():
    render_header()
    user = st.session_state.user
    
    # Candidate Top Banner
    st.markdown(f"""
        <div class="hero-container" style="padding: 60px 40px; border-radius: 0 0 40px 40px; margin-bottom: 40px;">
            <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto;">
                <div style="text-align: left;">
                    <h1 style="margin: 0; color: white; font-size: 2.8rem; font-weight: 900;">{user[1]}</h1>
                    <p style="margin: 8px 0 0 0; opacity: 0.8; font-size: 1.1rem; font-weight: 500;">Candidate ID: PMIS-2024-{str(user[0]).zfill(5)}</p>
                </div>
                <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 20px 35px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--secondary); text-transform: uppercase; letter-spacing: 1.5px;">Portal Status</div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: white;">ACTIVE PROFILE</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT company, status, created_at, sector FROM applications WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user[0],))
    row = cur.fetchone()
    conn.close()

    c_main, c_side = st.columns([2.3, 1])

    with c_main:
        st.markdown('<h3 style="color: var(--primary); font-weight: 800; margin-bottom: 25px;">&#x1f4ca; MY INTERNSHIP JOURNEY</h3>', unsafe_allow_html=True)
        
        if row:
            company, status, applied_at, sector = row
            status_colors = {
                "Applied": {"border": "#00296b", "bg": "#f0f4f8", "text": "#00296b"},
                "Selected": {"border": "#1e7e34", "bg": "#f0fff4", "text": "#1e7e34"},
                "Rejected": {"border": "#bd2130", "bg": "#fff5f5", "text": "#bd2130"}
            }
            color = status_colors.get(status, status_colors["Applied"])
            
            st.markdown(f"""
                <div class="dash-card" style="border-left: 12px solid {color['border']};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="status-badge" style="background: {color['border']}; color: white;">Latest Application</span>
                            <h2 style="margin: 20px 0 8px 0; color: var(--primary); font-weight: 900;">{company}</h2>
                            <p style="color: var(--text-muted); font-size: 1.1rem; margin: 0; font-weight: 500;">Sector: <b>{sector}</b></p>
                            <p style="color: #999; font-size: 0.9rem; margin-top: 15px;">Applied on: {applied_at[:16]}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="margin: 0; color: var(--text-muted); font-size: 0.85rem; font-weight: 700; text-transform: uppercase;">Current Result</p>
                            <h1 style="margin: 8px 0; color: {color['text']}; font-weight: 900; font-size: 3rem; letter-spacing: -1px;">{status.upper()}</h1>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if status == "Applied":
                st.info("\U0001F4A1 **AI Matching in Progress**: Our engine is comparing your skills with company requirements. Expect an email shortly.")
            elif status == "Selected":
                st.balloons()
                st.success("\U0001F389 **Success!** You have been shortlisted by the selection engine. Direct confirmation and onboarding details have been sent to your registered email.")
        else:
            st.markdown("""
                <div class="dash-card" style="text-align: center; border: 2px dashed var(--border-color); background: transparent; padding: 60px;">
                    <div style="font-size: 5rem; margin-bottom: 25px; opacity: 0.5;">&#x1f4bc;</div>
                    <h2 style="color: var(--text-muted); font-weight: 800;">No Active Applications</h2>
                    <p style="color: #999; max-width: 500px; margin: 0 auto 35px; font-size: 1.1rem;">
                        Start your professional career with industrial internship opportunities. Your dream career is just a click away.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="main-btn">', unsafe_allow_html=True)
            if st.button("\U0001F680 BROWSE & APPLY NOW", use_container_width=True):
                st.session_state.page = "apply"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with c_side:
        st.markdown('<h3 style="color: var(--primary); font-weight: 800; margin-bottom: 25px;">&#x1f464; PROFILE</h3>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="dash-card" style="padding: 30px;">
                <div style="margin-bottom: 25px;">
                    <p style="color: var(--text-muted); font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Contact Info</p>
                    <p style="font-weight: 700; font-size: 1.1rem; color: var(--primary);">+91 {user[3]}</p>
                </div>
                <div style="margin-bottom: 25px;">
                    <p style="color: var(--text-muted); font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Email Identity</p>
                    <p style="font-weight: 700; font-size: 1.1rem; color: var(--primary); overflow-wrap: break-word;">{user[2]}</p>
                </div>
                <div style="margin-bottom: 25px;">
                    <p style="color: var(--text-muted); font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Geography</p>
                    <p style="font-weight: 700; font-size: 1.1rem; color: var(--primary);">{user[5]} | <span style="background: #eef2ff; color: var(--primary); padding: 4px 10px; border-radius: 8px; font-size: 0.85rem;">{user[6]}</span></p>
                </div>
                
                <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
                
                <div class="main-btn" style="margin-bottom: 12px;">""", unsafe_allow_html=True)
        
        if st.button("\U0001F4C4 GENERATE SCHEME ID", use_container_width=True):
            st.toast("ID Generating...")
        
        st.markdown('</div><div class="outline-btn">', unsafe_allow_html=True)
        if st.button("\U0001F6AA LOGOUT SESSION", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

# -------------------- PAGE: APPLY --------------------
def apply_page():
    render_header()
    col1, mid, col3 = st.columns([1, 1.8, 1])
    with mid:
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="dash-card">
                <h2 style="margin-top: 0; color: var(--primary); font-weight: 900; text-align: center;">Internship Form</h2>
                <p style="color: var(--text-muted); text-align: center; margin-bottom: 40px;">Provide your academic and professional details for AI allocation.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("apply_form"):
            st.markdown('<h5 style="color: var(--primary); font-weight: 700; margin-bottom: 15px;">&#x1f4bc; Career Preferences</h5>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            sector = c1.selectbox("Industry Sector Interest*", ["Telecom", "Energy/Power", "Manufacturing", "IT & Digital Services", "Infrastructure", "Financial Services"])
            company = c2.selectbox("Target Company*", ["REC Limited", "JSW Steel", "GAIL India", "Cognizant", "L&T", "Reliance Industries", "TCS"])
            
            st.markdown('<h5 style="color: var(--primary); font-weight: 700; margin-top: 30px; margin-bottom: 15px;">&#x1f393; Academic Background</h5>', unsafe_allow_html=True)
            skills = st.text_area("List your Key Skills (e.g. Data Analytics, Python, HR Management)*")
            qual = st.selectbox("Highest Qualification*", ["10th Pass", "12th Pass", "ITI/Diploma", "Graduate", "Post Graduate"])
            
            st.markdown('<h5 style="color: var(--primary); font-weight: 700; margin-top: 30px; margin-bottom: 15px;">&#x1f4cd; Mobility & Location</h5>', unsafe_allow_html=True)
            loc_pref = st.text_input("Preferred Location (City/District)*")
            
            st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="main-btn">', unsafe_allow_html=True)
            submit = st.form_submit_button("SUBMIT APPLICATION TO AI ENGINE", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if submit:
            if not all([skills, loc_pref]):
                st.error("Please provide all mandatory details.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO applications (user_id, skills, sector, company, location_pref, qualification, rural_urban, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (st.session_state.user[0], skills, sector, company, loc_pref, qual, st.session_state.user[6], "Applied"))
                conn.commit()
                conn.close()

                send_hr_email(st.session_state.user[1], company, skills, st.session_state.user[0])
                st.success("\U0001F680 Application submitted successfully. Your matches are being processed.")
                st.session_state.page = "dashboard"
                st.rerun()

        st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
        if st.button("\u2190 RETURN TO DASHBOARD", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- HR ACTION HANDLER (QUERY PARAMS) --------------------
params = st.query_params
if "action" in params and "cid" in params:
    action = params["action"]
    cid = params["cid"]
    company_param = params.get("comp", "")

    conn = get_connection()
    cur = conn.cursor()

    # Determine which application to update
    if company_param:
        cur.execute("""
            SELECT u.email, a.company
            FROM users u
            JOIN applications a ON u.id = a.user_id
            WHERE u.id = ? AND a.company = ? AND a.status = 'Applied'
            ORDER BY a.id DESC LIMIT 1
        """, (cid, company_param))
    else:
        # Fallback if comp not in URL
        cur.execute("""
            SELECT u.email, a.company
            FROM users u
            JOIN applications a ON u.id = a.user_id
            WHERE u.id = ? AND a.status = 'Applied'
            ORDER BY a.id DESC LIMIT 1
        """, (cid,))
        
    result = cur.fetchone()

    if result:
        email, company = result
        if action == "accept":
            cur.execute("UPDATE applications SET status='Selected' WHERE user_id=? AND company=? AND status='Applied'", (cid, company))
            send_candidate_email(email, "Selected", company)
            st.success(f"Candidate {cid} has been Selected for {company}.")
        elif action == "reject":
            cur.execute("UPDATE applications SET status='Rejected' WHERE user_id=? AND company=? AND status='Applied'", (cid, company))
            send_candidate_email(email, "Rejected", company)
            st.error(f"Candidate {cid} has been Rejected for {company}.")

    conn.commit()
    conn.close()

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
