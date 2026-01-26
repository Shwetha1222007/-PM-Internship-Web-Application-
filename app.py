# -*- coding: utf-8 -*-
import streamlit as st
from database import create_tables, get_connection
from auth import register_user, login_user
from email_service import send_hr_announcement, send_update_to_candidate
import datetime

st.set_page_config(
    page_title="PM Internship Scheme | Government of India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- PREMIUM DARK THEME WITH ANIMATIONS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e0e0e0;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #0a0a0a;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ffb703, #fb8500);
    border-radius: 10px;
}

/* Header Container */
.header-container {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 25px 50px;
    border-radius: 20px;
    border: 2px solid transparent;
    border-image: linear-gradient(90deg, #ffb703, #fb8500, #ffb703) 1;
    box-shadow: 0 10px 40px rgba(255, 183, 3, 0.2);
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
    from {
        transform: translateY(-30px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
}

.gov-emblem {
    font-size: 48px;
    filter: drop-shadow(0 0 10px #ffb703);
}

.gov-text {
    font-size: 14px;
    font-weight: 600;
    color: #b8b8b8;
    line-height: 1.6;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(90deg, #ffb703, #fb8500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(255, 183, 3, 0.5);
    letter-spacing: 1px;
}

.tagline {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(90deg, #ffffff, #ffb703);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 60px 0 40px 0;
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Premium Card */
.premium-card {
    background: rgba(26, 26, 26, 0.95);
    backdrop-filter: blur(10px);
    padding: 50px;
    border-radius: 25px;
    border: 1px solid #333;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(255, 183, 3, 0.1);
    margin: 30px auto;
    max-width: 600px;
    animation: cardFloat 0.8s ease-out;
    position: relative;
    overflow: hidden;
}

.premium-card::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #ffb703, #fb8500, #ffb703);
    border-radius: 25px;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.premium-card:hover::before {
    opacity: 0.3;
}

@keyframes cardFloat {
    from {
        transform: translateY(30px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.card-title {
    font-size: 28px;
    font-weight: 700;
    color: #ffb703;
    margin-bottom: 30px;
    text-align: center;
}

/* Styled Inputs */
div[data-baseweb="input"] input,
textarea,
.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stNumberInput input {
    background: #1a1a1a !important;
    color: #ffffff !important;
    border: 2px solid #2a2a2a !important;
    border-radius: 15px !important;
    padding: 16px !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}

/* Clean Selectbox Styling */
div[data-testid="stSelectbox"] > label {
    color: #ffb703 !important;
}

li[role="option"]:hover {
    background: #2a2a2a !important;
    color: #ffb703 !important;
}

div[data-baseweb="input"] input:focus,
div[data-baseweb="select"] > div:focus,
textarea:focus {
    border-color: #ffb703 !important;
    box-shadow: 0 0 20px rgba(255, 183, 3, 0.3) !important;
    background: #1a1a1a !important;
}

/* Premium Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
    color: #ffffff;
    border: 2px solid #ffb703;
    border-radius: 15px;
    padding: 16px 32px;
    font-size: 17px;
    font-weight: 700;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    text-transform: uppercase;
    letter-spacing: 1px;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #ffb703 0%, #fb8500 100%);
    color: #000000;
    border-color: #ffb703;
    box-shadow: 0 8px 30px rgba(255, 183, 3, 0.5);
    transform: translateY(-3px);
}

div.stButton > button:active {
    transform: translateY(-1px);
}

/* Success/Error Messages */
.stAlert {
    border-radius: 15px;
    border-left: 5px solid #ffb703;
    animation: slideInRight 0.5s ease-out;
}

@keyframes slideInRight {
    from {
        transform: translateX(30px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* Info Section */
.info-section {
    background: rgba(255, 183, 3, 0.1);
    border-left: 4px solid #ffb703;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
}

/* Feature Grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 25px;
    margin: 40px 0;
}

.feature-card {
    background: rgba(26, 26, 26, 0.8);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #2a2a2a;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.feature-card:hover {
    transform: translateY(-10px);
    border-color: #ffb703;
    box-shadow: 0 15px 40px rgba(255, 183, 3, 0.2);
}

.feature-icon {
    font-size: 48px;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffb703;
    margin-bottom: 10px;
}

.feature-desc {
    font-size: 14px;
    color: #b8b8b8;
    line-height: 1.6;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    margin: 30px 0;
}

.stat-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #333;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(255, 183, 3, 0.3);
}

.stat-number {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #ffb703, #fb8500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 16px;
    color: #b8b8b8;
    margin-top: 10px;
}

/* Loading Animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading {
    animation: pulse 2s ease-in-out infinite;
}

/* Form Labels */
label {
    color: #b8b8b8 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
}

/* Image Animation */
.stImage img {
    animation: imageFloat 1.2s ease-out;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

@keyframes imageFloat {
    from {
        transform: translateY(40px) scale(0.9);
        opacity: 0;
    }
    to {
        transform: translateY(0) scale(1);
        opacity: 1;
    }
}

/* Profile Popup Modal */
.profile-popup {
    position: fixed;
    top: 80px;
    right: 30px;
    width: 300px;
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 0;
    border-radius: 20px;
    border: 2px solid #ffb703;
    box-shadow: 0 15px 50px rgba(255, 183, 3, 0.3);
    z-index: 1000;
    animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
    from {
        transform: translateX(100px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.profile-popup-header {
    background: linear-gradient(135deg, #ffb703, #fb8500);
    padding: 30px 25px;
    border-radius: 18px 18px 0 0;
    text-align: center;
}

.profile-avatar {
    width: 80px;
    height: 80px;
    background: #000;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    font-weight: 700;
    color: #ffb703;
    margin: 0 auto 15px;
    border: 3px solid #000;
}

.profile-name {
    font-size: 20px;
    font-weight: 700;
    color: #000;
    text-align: center;
    margin-bottom: 5px;
}

.profile-email {
    font-size: 12px;
    color: #2d2d2d;
    text-align: center;
    word-break: break-all;
}

.profile-popup-body {
    padding: 20px 25px;
}

.profile-info {
    font-size: 14px;
    color: #e0e0e0;
    margin: 12px 0;
    padding: 10px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.profile-info-icon {
    color: #ffb703;
}

/* Info Boxes (for home page) */
.info-boxes {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    max-width: 600px;
    margin: 40px auto;
}

.info-box {
    background: rgba(26, 26, 26, 0.8);
    padding: 30px;
    border-radius: 15px;
    border: 1px solid #2a2a2a;
    text-align: center;
    transition: all 0.3s ease;
}

.info-box:hover {
    transform: translateY(-5px);
    border-color: #ffb703;
    box-shadow: 0 10px 30px rgba(255, 183, 3, 0.2);
}

.info-box-title {
    font-size: 24px;
    font-weight: 700;
    color: #ffb703;
    margin-bottom: 10px;
}

.info-box-desc {
    font-size: 14px;
    color: #b8b8b8;
    line-height: 1.6;
}

/* Program Description */
.program-desc {
    max-width: 800px;
    margin: 40px auto;
    padding: 30px;
    background: rgba(26, 26, 26, 0.6);
    border-radius: 15px;
    text-align: left;
    line-height: 1.8;
    font-size: 15px;
    color: #c8c8c8;
}

/* Application Detail Card */
.app-detail-card {
    background: rgba(26, 26, 26, 0.95);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #333;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.app-detail-header {
    font-size: 22px;
    font-weight: 700;
    color: #ffb703;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #2a2a2a;
}

.app-detail-row {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 15px;
    margin: 15px 0;
    padding: 12px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
}

.app-detail-label {
    font-weight: 700;
    color: #ffb703;
    font-size: 14px;
}

.app-detail-value {
    color: #e0e0e0;
    font-size: 14px;
}

/* Additional Dark Theme Fixes */
.stDateInput > div > div > input {
    background: #1a1a1a !important;
    color: #ffffff !important;
    border: 2px solid #2a2a2a !important;
}

/* Calendar Popup */
div[data-baseweb="calendar"] {
    background: #1a1a1a !important;
    border: 2px solid #2a2a2a !important;
}

div[data-baseweb="calendar"] button {
    background: #1a1a1a !important;
    color: #ffffff !important;
}

div[data-baseweb="calendar"] button:hover {
    background: #2a2a2a !important;
    color: #ffb703 !important;
}

/* Number Input */
.stNumberInput input {
    background: #1a1a1a !important;
    color: #ffffff !important;
}

/* Remove white backgrounds from all streamlit components */
.stMarkdown, .stText, .element-container {
    color: #e0e0e0 !important;
}

/* Success/Error boxes dark theme */
.stSuccess, .stError, .stWarning, .stInfo {
    background: rgba(26, 26, 26, 0.8) !important;
    color: #ffffff !important;
}

/* Welcome Message */
.welcome-msg {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
}

.user-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ffb703, #fb8500);
    color: #000;
    padding: 8px 20px;
    border-radius: 25px;
    font-weight: 700;
    margin-left: 10px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 30px;
    color: #666;
    font-size: 14px;
    margin-top: 60px;
    border-top: 1px solid #2a2a2a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- INIT ----------------
create_tables()



# ---------------- HEADER ----------------
def render_header():
    st.markdown("""
    <div class="header-container">
        <div class="header-left">
            <div class="gov-emblem">🇮🇳</div>
            <div class="gov-text">
                <b>Government of India</b><br>
                Ministry of Corporate Affairs
            </div>
        </div>
        <div class="main-title">PM Internship Scheme</div>
        <div style="width: 100px;"></div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- QUERY PARAMS HANDLER ----------------
def handle_query_params():
    """
    Handles HR actions (Accept/Reject) via URL query parameters.
    Expected format: /?action=accept&cid=123&comp=Google
    """
    try:
        # Get query parameters
        qp = st.query_params
        action = qp.get("action")
        user_id = qp.get("cid")
        company = qp.get("comp")

        if action and user_id and company:
            # Validate action
            if action not in ["accept", "reject"]:
                return

            render_header()
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">HR Administrative Action</div>', unsafe_allow_html=True)
            
            conn = get_connection()
            
            # Verify user exists
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if not user:
                st.error("❌ User not found.")
                conn.close()
                st.stop()

            # Determine new status
            new_status = "Selected" if action == "accept" else "Rejected"
            status_color = "#28a745" if new_status == "Selected" else "#dc3545"

            # Update Application in DB
            # Note: Matching by user_id and company since generic link structure was requested
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE applications 
                SET status = ? 
                WHERE user_id = ? AND company = ?
            """, (new_status, user_id, company))
            
            if cursor.rowcount > 0:
                conn.commit()
                st.markdown(f"""
                <div style="background: {status_color}; padding: 20px; border-radius: 10px; text-align: center; color: white; margin-bottom: 20px;">
                    <h2>Action: {new_status.upper()}</h2>
                    <p>Candidate: <b>{user['name']}</b></p>
                    <p>Company: <b>{company}</b></p>
                </div>
                """, unsafe_allow_html=True)

                # Send Email to Candidate
                with st.spinner(f"Sending notification email to {user['email']}..."):
                    try:
                        send_update_to_candidate(user['email'], new_status, company)
                        st.success(f"✅ Notification email successfully sent to candidate.")
                    except Exception as e:
                        st.error(f"⚠️ Database updated, but failed to send email: {e}")
                
            else:
                st.warning(f"⚠️ No active application found for {user['name']} at {company}.")
            
            conn.close()
            
            if st.button("Home"):
                st.query_params.clear()
                st.session_state.page = "home"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop() # Stop further execution to show only this result
            
    except Exception as e:
        st.error(f"System Error: {e}")

# Call handler at startup
handle_query_params()

if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- HOME ----------------
def home():
    render_header()
    
    st.markdown('<div class="tagline">🚀 Bridging Talent with Opportunity</div>', unsafe_allow_html=True)
    
    # Hero Image - Natural student discussion
    # Dynamic Information Section to replace image space
    st.markdown("""
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 40px; animation: fadeIn 1.2s ease-out;">
        <div class="stat-card" style="flex: 1; max-width: 300px; border-top: 4px solid #ffb703;">
            <div style="font-size: 24px; margin-bottom: 10px;">🌟</div>
            <div style="font-weight: 700; color: #ffb703; margin-bottom: 10px;">Viksit Bharat 2047</div>
            <div style="font-size: 14px; color: #b8b8b8;">Empowering the youth to lead India towards becoming a developed nation by 2047.</div>
        </div>
        <div class="stat-card" style="flex: 1; max-width: 300px; border-top: 4px solid #ffb703;">
            <div style="font-size: 24px; margin-bottom: 10px;">💼</div>
            <div style="font-weight: 700; color: #ffb703; margin-bottom: 10px;">Direct Exposure</div>
            <div style="font-size: 14px; color: #b8b8b8;">Gain hands-on experience in top Indian corporates and global MNCs operating in India.</div>
        </div>
        <div class="stat-card" style="flex: 1; max-width: 300px; border-top: 4px solid #ffb703;">
            <div style="font-size: 24px; margin-bottom: 10px;">📈</div>
            <div style="font-weight: 700; color: #ffb703; margin-bottom: 10px;">Skill Development</div>
            <div style="font-size: 14px; color: #b8b8b8;">Bridge the gap between academic learning and industry requirements.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Program Description
    st.markdown("""
    <div class="program-desc">
        The PM Internship Scheme is a visionary program launched to provide professional 
        exposure to the youth of India. By partnering with the top 500 companies, the 
        government ensures that candidates receive hands-on training in real-world 
        environments.
    </div>
    """, unsafe_allow_html=True)
    
    # Info Boxes
    st.markdown("""
        <div class="info-box">
            <div class="info-box-title">₹ 5,000</div>
            <div class="info-box-desc">Monthly Stipend via DBT</div>
        </div>
        <div class="info-box">
            <div class="info-box-title">12 Months</div>
            <div class="info-box-desc">Duration of Internship</div>
        </div>
        <div class="info-box">
            <div class="info-box-title">Certifications</div>
            <div class="info-box-desc">Industry Recognized Badges</div>
        </div>
        <div class="info-box">
            <div class="info-box-title">Top 500</div>
            <div class="info-box-desc">Partner Companies</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 LOGIN", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        with col2:
            if st.button("📝 REGISTER", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2026 Government of India | Ministry of Corporate Affairs</p>
        <p>Empowering Youth Through Quality Internships</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- REGISTER ----------------
def register():
    render_header()
    
    # Informational Text to replace image space
    st.markdown("""
    <div style="text-align: center; max-width: 700px; margin: 0 auto 40px auto; animation: slideDown 0.5s ease-out;">
        <h2 style="color: #ffb703; font-weight: 800; font-size: 32px; margin-bottom: 15px;">Join the Future of Corporate India</h2>
        <p style="color: #e0e0e0; font-size: 16px; line-height: 1.6;">
            By creating an account, you take the first step towards a prestigious 12-month internship 
            with India's leading companies. Gain professional skills, earn a monthly stipend, 
            and build a career that matters.
        </p>
        <div style="display: flex; gap: 15px; justify-content: center; margin-top: 25px;">
            <div style="background: rgba(255, 183, 3, 0.1); padding: 10px 20px; border-radius: 10px; border: 1px solid rgba(255, 183, 3, 0.3);">
                <span style="color: #ffb703; font-weight: 700;">1. Register</span>
            </div>
            <div style="background: rgba(255, 183, 3, 0.1); padding: 10px 20px; border-radius: 10px; border: 1px solid rgba(255, 183, 3, 0.2);">
                <span style="color: #b8b8b8;">2. Apply</span>
            </div>
            <div style="background: rgba(255, 183, 3, 0.1); padding: 10px 20px; border-radius: 10px; border: 1px solid rgba(255, 183, 3, 0.2);">
                <span style="color: #b8b8b8;">3. Get Hired</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 Create Your Account</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Enter your full name")
        phone = st.text_input("Phone Number", placeholder="+91 XXXXXXXXXX")
        dob = st.date_input("Date of Birth", min_value=datetime.date(1990, 1, 1))
        district = st.text_input("District", placeholder="Your district")
    
    with col2:
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Create a strong password")
        social_category = st.selectbox("Social Category", ["General", "OBC", "MBC", "SC", "ST", "EWS"])
        rural = st.selectbox("Area Type", ["Urban", "Rural"])
    
    aadhaar = st.text_input("Aadhaar Number", placeholder="XXXX-XXXX-XXXX")
    address = st.text_area("Address", placeholder="Enter your complete address")
    
    col1, col2 = st.columns(2)
    with col1:
        blood_group = st.selectbox("Blood Group", ["Select Blood Group", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    with col2:
        bank_account = st.text_input("Bank Account Number", placeholder="11-digit account number", max_chars=11)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ CREATE ACCOUNT", use_container_width=True):
        if not name or not email or not password or blood_group == "Select Blood Group":
            st.error("⚠️ Please fill in all required fields!")
        elif bank_account and len(bank_account) != 11:
            st.error("⚠️ Bank Account Number must be exactly 11 digits!")
        else:
            if register_user((name, email, phone, password, str(dob), district, rural, 
                            social_category, aadhaar, address, blood_group, bank_account)):
                st.success("✅ Registration Successful! Please login to continue.")
                st.balloons()
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("❌ Registration failed. Email may already exist.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIN ----------------
def login():
    render_header()
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔐 Welcome Back</div>', unsafe_allow_html=True)
    
    email = st.text_input("Email Address", placeholder="your.email@example.com")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 LOGIN", use_container_width=True):
        if not email or not password:
            st.error("⚠️ Please enter both email and password!")
        else:
            user = login_user(email, password)
            if user:
                st.session_state.user = dict(user)
                st.success(f"✅ Welcome back, {user['name']}!")
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
def dashboard():
    render_header()
    
    user = st.session_state.user
    
    # Profile Popup Toggle
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False
    
    # Profile popup when clicked
    if st.session_state.show_profile:
        initials = ''.join([word[0].upper() for word in user['name'].split()[:2]])
        st.markdown(f"""
        <div class="profile-popup">
            <div class="profile-popup-header">
                <div class="profile-avatar">{initials}</div>
                <div class="profile-name">{user['name']}</div>
                <div class="profile-email">{user['email']}</div>
            </div>
            <div class="profile-popup-body">
                <div class="profile-info">
                    <span class="profile-info-icon">📞</span>
                    <span>{user['phone'] or 'Not provided'}</span>
                </div>
                <div class="profile-info">
                    <span class="profile-info-icon">📍</span>
                    <span>{user['district'] or 'Not provided'}</span>
                </div>
                <div class="profile-info">
                    <span class="profile-info-icon">🩸</span>
                    <span>{user['blood_group'] or 'Not provided'}</span>
                </div>
                <div class="profile-info">
                    <span class="profile-info-icon">🎂</span>
                    <span>{user['dob'] or 'Not provided'}</span>
                </div>
                <div class="profile-info">
                    <span class="profile-info-icon">🆔</span>
                    <span>{user['aadhaar'] or 'Not provided'}</span>
                </div>
                <div class="profile-info">
                    <span class="profile-info-icon">🏠</span>
                    <span style="font-size: 12px;">{user['address'] or 'Not provided'}</span>
                </div>
                 <div class="profile-info">
                    <span class="profile-info-icon">🏦</span>
                    <span>{user['bank_account'] or 'Not provided'}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Welcome Section
    st.markdown(f"""
    <div class="welcome-msg">
        Welcome back, {user['name']}! 👋
        <span class="user-badge">VERIFIED</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats Dashboard
    conn = get_connection()
    
    # Get application count
    app_count = conn.execute("SELECT COUNT(*) FROM applications WHERE user_id = ?", 
                            (user['id'],)).fetchone()[0]
    
    # Get recent applications
    applications = conn.execute("""
        SELECT * FROM applications WHERE user_id = ? ORDER BY created_at DESC LIMIT 10
    """, (user['id'],)).fetchall()
    
    conn.close()
    
    # Statistics Cards
    st.markdown(f"""
    <div class="dashboard-grid">
        <div class="stat-card">
            <div class="stat-number">{app_count}</div>
            <div class="stat-label">Applications Submitted</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len([a for a in applications if a['status'] == 'Applied'])}</div>
            <div class="stat-label">Pending Review</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">100+</div>
            <div class="stat-label">Companies Available</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Quick Actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 APPLY FOR INTERNSHIP", use_container_width=True):
            st.session_state.page = "apply"
            st.session_state.show_profile = False
            st.rerun()
    
    with col2:
        if st.button("📊 MY APPLICATIONS", use_container_width=True):
            st.session_state.page = "view_applications"
            st.session_state.show_profile = False
            st.rerun()
    
    with col3:
        # Profile button with toggle
        profile_label = "❌ CLOSE" if st.session_state.show_profile else "👤 PROFILE"
        if st.button(profile_label, use_container_width=True):
            st.session_state.show_profile = not st.session_state.show_profile
            st.rerun()
    
    with col4:
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            st.session_state.show_profile = False
            st.rerun()
    
    # Recent Applications
    if applications:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 📑 Recent Applications")
        
        for app in applications:
            status_color = "#4CAF50" if app['status'] == 'Applied' else "#FF9800"
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 18px; font-weight: 700; color: #ffb703;">
                                {app['sector']} Internship
                            </div>
                            <div style="font-size: 14px; color: #b8b8b8; margin-top: 5px;">
                                Applied on: {app['created_at']}
                            </div>
                        </div>
                        <div style="background: {status_color}; color: white; padding: 8px 20px; border-radius: 20px; font-weight: 700;">
                            {app['status']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Dynamic status message check
                if app['status'] == 'Selected':
                    st.success("🎉 You have been selected!")
                elif app['status'] == 'Rejected':
                    st.error("❌ Application not matched.")
                
                if st.button("View Details", key=f"view_{app['id']}", use_container_width=True):
                    st.session_state.selected_app_id = app['id']
                    st.session_state.page = "application_detail"
                    st.rerun()
    else:
        st.info("📝 No applications yet. Start by applying for an internship!")

# ---------------- APPLY ----------------
def apply():
    render_header()
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Internship Application Form</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-section">
        <b>ℹ️ Application Instructions</b><br>
        Fill in all details carefully. Your application will be reviewed by our AI engine and matched with suitable opportunities.
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Information
    st.markdown("### 👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        sector_options = [
            "Select Sector",
            "Information Technology & Software",
            "Banking, Finance & Insurance",
            "Energy, Oil & Gas",
            "Manufacturing & Heavy Industry",
            "Consumer Goods & Pharmaceuticals",
            "Other Major Corporates"
        ]
        sector = st.selectbox("Preferred Sector", sector_options, key="sector_select")
        
        location_pref = st.text_input("Preferred Location", placeholder="City or State (e.g., Bangalore, Mumbai)")
        college_name = st.text_input("College/University Name")
    
    with col2:
        company_options = [
            "Select Company",
            # IT
            "Tata Consultancy Services (TCS)", "Infosys Ltd.", "Wipro Ltd.", "HCL Technologies Ltd.", 
            "Tech Mahindra Ltd.", "Cognizant Technology Solutions India Pvt. Ltd.", 
            "Google IT Services India Pvt. Ltd.", "Microsoft India (R&D) Pvt. Ltd.", "IBM India Pvt. Ltd.",
            # Finance
            "HDFC Bank Ltd.", "ICICI Bank Ltd.", "Axis Bank Ltd.", "IndusInd Bank Ltd.", 
            "Bajaj Finance Ltd.", "SBI Cards & Payment Services Ltd.", 
            "ICICI Lombard General Insurance Co.", "Max Life Insurance Company Ltd.",
            # Energy
            "Reliance Industries Ltd.", "Oil and Natural Gas Corporation (ONGC)", 
            "Indian Oil Corporation Ltd. (IOCL)", "GAIL (India) Ltd.", "Bharat Petroleum Corporation Ltd. (BPCL)", 
            "Hindustan Petroleum Corporation Ltd.", "Adani Total Gas Ltd.",
            # Manufacturing
            "Tata Steel Ltd.", "Larsen & Toubro Ltd.", "Mahindra & Mahindra Ltd.", 
            "Jindal Steel & Power Ltd.", "NTPC Ltd.", "Hindalco Industries Ltd.",
            # Pharma/Consumer
            "Hindustan Unilever Ltd.", "Serum Institute of India Pvt. Ltd.", "Zydus Lifesciences Ltd.", 
            "Glenmark Pharmaceuticals Ltd.", "Reckitt Benckiser (India) Pvt. Ltd.",
            # Others
            "Reliance Jio Infocomm Ltd.", "Power Grid Corporation of India Ltd.", 
            "Maruti Suzuki India Ltd.", "Vedanta Ltd.", "Samsung India Electronics Pvt. Ltd."
        ]
        company = st.selectbox("Target Company", company_options, key="company_select")
            
        languages = st.text_input("Languages Known", placeholder="English, Hindi, etc.")
        cgpa_str = st.text_input("CGPA (0-10)", placeholder="e.g., 8.5")
    
    # Education & Skills
    st.markdown("### 📚 Education & Skills")
    col1, col2 = st.columns(2)
    with col1:
        perc_12th_str = st.text_input("12th Grade Percentage", placeholder="e.g., 85.5")
    with col2:
        has_experience = st.radio("Do you have prior experience?", ["No", "Yes"], horizontal=True)
        if has_experience == "Yes":
            exp_years = st.number_input("Years of Experience", min_value=0.5, step=0.5, format="%.1f")
            experience = f"{exp_years} Years"
        else:
            experience = "None"
    
    skills = st.text_area("Technical Skills & Competencies", 
                         placeholder="List your skills, technologies, tools, etc.",
                         height=120)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 SUBMIT APPLICATION", use_container_width=True):
        if not skills or sector == "Select Sector" or company == "Select Company":
            st.error("⚠️ Please fill in all required fields!")
        else:
            # Convert percentage strings to floats
            try:
                cgpa = float(cgpa_str) if cgpa_str else 0.0
                perc_12th = float(perc_12th_str) if perc_12th_str else 0.0
            except ValueError:
                st.error("⚠️ Please enter valid numbers for CGPA and Percentage!")
                return
            
            conn = get_connection()
            conn.execute("""
                INSERT INTO applications 
                (user_id, skills, sector, company, location_pref, languages, perc_12th, college_name, cgpa, experience, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (st.session_state.user['id'], skills, sector, company, location_pref, 
                  languages, perc_12th, college_name, cgpa, experience, "Applied"))
            conn.commit()
            conn.close()
            
            # Email sending with comprehensive error handling
            try:
                # Prepare data dictionary exactly as expected by strictly typed email service
                app_data = {
                    'skills': skills,
                    'sector': sector,
                    'company': company or 'General Pool', # Ensure company is never empty for the link
                    'college_name': college_name or 'Not provided',
                    'cgpa': cgpa,
                    'languages': languages or 'Not provided',
                    'experience': experience
                }
                
                # Show spinner while sending
                with st.spinner("Submitting application and notifying HR..."):
                     send_hr_announcement(st.session_state.user, app_data)
                     
            except Exception as e:
                print(f"Email Error (non-critical): {e}")
                # Continue with application submission even if email fails
            
            st.success("✅ Application Submitted Successfully!")
            st.balloons()
            st.session_state.page = "dashboard"
            st.session_state.show_profile = False
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.session_state.show_profile = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- VIEW APPLICATIONS ----------------
def view_applications():
    render_header()
    
    user = st.session_state.user
    
    st.markdown("### 📊 My Applications")
    st.markdown("<br>", unsafe_allow_html=True)
    
    conn = get_connection()
    applications = conn.execute("""
        SELECT * FROM applications WHERE user_id = ? ORDER BY created_at DESC
    """, (user['id'],)).fetchall()
    conn.close()
    
    if applications:
        for app in applications:
            status_color = "#4CAF50" if app['status'] == 'Applied' else "#FF9800"
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 20px; font-weight: 700; color: #ffb703;">
                                {app['sector']} Internship
                            </div>
                            <div style="font-size: 14px; color: #b8b8b8; margin-top: 8px;">
                                📅 Applied: {app['created_at']}<br>
                                🏢 Company: {app['company'] or 'Any'}<br>
                                📍 Location: {app['location_pref'] or 'Any'}
                            </div>
                        </div>
                        <div style="background: {status_color}; color: white; padding: 10px 25px; border-radius: 25px; font-weight: 700; font-size: 16px;">
                            {app['status']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("View Details", key=f"detail_{app['id']}", use_container_width=True):
                    st.session_state.selected_app_id = app['id']
                    st.session_state.page = "application_detail"
                    st.rerun()
    else:
        st.info("📝 No applications yet. Start by applying for an internship!")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# ---------------- APPLICATION DETAIL ----------------
def application_detail():
    render_header()
    
    if 'selected_app_id' not in st.session_state:
        st.session_state.page = "dashboard"
        st.rerun()
        return
    
    conn = get_connection()
    app = conn.execute("""
        SELECT * FROM applications WHERE id = ?
    """, (st.session_state.selected_app_id,)).fetchone()
    conn.close()
    
    if not app:
        st.error("Application not found!")
        st.session_state.page = "dashboard"
        st.rerun()
        return
    
    status_color = "#4CAF50" if app['status'] == 'Applied' else "#FF9800"
    
    st.markdown(f"""
    <div class="app-detail-card">
        <div class="app-detail-header">
            📋 Application Details
            <span style="float: right; background: {status_color}; color: white; padding: 8px 20px; border-radius: 20px; font-size: 16px;">
                {app['status']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Application Information
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("#### 📌 Basic Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">Application ID:</div>
            <div class="app-detail-value">#{app['id']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Sector:</div>
            <div class="app-detail-value">{app['sector']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Preferred Company:</div>
            <div class="app-detail-value">{app['company'] or 'Any Company'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">Applied On:</div>
            <div class="app-detail-value">{app['created_at']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Location Preference:</div>
            <div class="app-detail-value">{app['location_pref'] or 'Any Location'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Status:</div>
            <div class="app-detail-value">{app['status']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎓 Education & Qualifications")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">College/University:</div>
            <div class="app-detail-value">{app['college_name'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">CGPA:</div>
            <div class="app-detail-value">{app['cgpa'] if app['cgpa'] else 'Not provided'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">12th Grade %:</div>
            <div class="app-detail-value">{app['perc_12th'] if app['perc_12th'] else 'Not provided'}%</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Languages Known:</div>
            <div class="app-detail-value">{app['languages'] or 'Not provided'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💼 Skills & Experience")
    
    st.markdown(f"""
    <div class="app-detail-row">
        <div class="app-detail-label">Technical Skills:</div>
        <div class="app-detail-value">{app['skills'] or 'Not provided'}</div>
    </div>
    <div class="app-detail-row">
        <div class="app-detail-label">Prior Experience:</div>
        <div class="app-detail-value">{app['experience'] or 'No prior experience'}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to All Applications"):
            st.session_state.page = "view_applications"
            st.rerun()
    with col2:
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

# ---------------- ROUTER ----------------
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
elif st.session_state.page == "view_applications":
    view_applications()
elif st.session_state.page == "application_detail":
    application_detail()
