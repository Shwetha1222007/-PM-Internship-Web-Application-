import streamlit as st
import os
import sys
from database import create_tables, get_connection
from auth import register_user, login_user
from email_service import send_hr_announcement, send_update_to_candidate, send_candidate_confirmation
from ai_engine import ai_filter_candidates
import difflib
import re

import datetime

# Import and start the background scheduler
try:
    from scheduler import start_background_scheduler
    # Start the scheduler only once
    if 'scheduler_started' not in st.session_state:
        start_background_scheduler()
        st.session_state.scheduler_started = True
except Exception as e:
    print(f"Warning: Could not start background scheduler: {e}")

# Common technical skills dictionary for spell checking
COMMON_TECHNICAL_SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "swift", "kotlin",
    "go", "rust", "scala", "perl", "r", "matlab", "sql", "html", "css", "dart",
    
    # Frameworks & Libraries
    "react", "angular", "vue", "django", "flask", "spring", "nodejs", "express", "fastapi",
    "tensorflow", "pytorch", "keras", "pandas", "numpy", "scikit-learn", "bootstrap", "jquery",
    "laravel", "rails", "asp.net", "nextjs", "gatsby", "svelte",
    
    # Databases
    "mysql", "postgresql", "mongodb", "oracle", "sqlite", "redis", "cassandra", "dynamodb",
    "mariadb", "elasticsearch", "neo4j", "firebase",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "github", "gitlab",
    "terraform", "ansible", "circleci", "travis", "heroku", "vercel", "netlify",
    
    # Tools & Technologies
    "linux", "unix", "windows", "macos", "bash", "powershell", "vim", "vscode", "intellij",
    "eclipse", "postman", "jira", "confluence", "slack", "figma", "photoshop", "illustrator",
    
    # Soft Skills
    "communication", "teamwork", "leadership", "problem-solving", "analytical", "creative",
    "time-management", "adaptability", "collaboration", "presentation", "negotiation",
    
    # Data Science & AI
    "machine-learning", "deep-learning", "data-analysis", "data-visualization", "nlp",
    "computer-vision", "statistics", "big-data", "hadoop", "spark", "tableau", "powerbi",
    
    # Web & Mobile
    "rest", "api", "graphql", "responsive-design", "ui/ux", "android", "ios", "flutter",
    "react-native", "xamarin", "cordova",
    
    # Other Technical Skills
    "agile", "scrum", "kanban", "testing", "debugging", "version-control", "ci/cd",
    "microservices", "blockchain", "cybersecurity", "networking", "cloud-computing"
]

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

# ---------------- SPELL CHECKER HELPER ----------------
def check_spelling_and_suggest(skills_text):
    """
    Check for spelling mistakes in technical skills and suggest corrections.
    Returns: (has_errors, suggestions_dict)
    """
    if not skills_text or not skills_text.strip():
        return False, {}
    
    # Split skills by common delimiters
    skill_items = re.split(r'[,;\n]+', skills_text.lower())
    skill_items = [s.strip() for s in skill_items if s.strip()]
    
    suggestions = {}
    has_errors = False
    
    for skill in skill_items:
        # Clean the skill (remove extra spaces, special chars for comparison)
        clean_skill = re.sub(r'[^\w\s\-+/#.]', '', skill).strip()
        
        # Skip very short items or numbers
        if len(clean_skill) < 2 or clean_skill.isdigit():
            continue
        
        # Check if skill exists in our dictionary (exact match)
        if clean_skill not in COMMON_TECHNICAL_SKILLS:
            # Find close matches using difflib
            close_matches = difflib.get_close_matches(
                clean_skill, 
                COMMON_TECHNICAL_SKILLS, 
                n=3,  # Get top 3 matches
                cutoff=0.6  # 60% similarity threshold
            )
            
            if close_matches:
                suggestions[skill] = close_matches
                has_errors = True
    
    return has_errors, suggestions

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
    New format: /?action=accept&aid=123
    Old format fallback: /?action=accept&cid=123&comp=Google
    """
    try:
        # Get query parameters
        qp = st.query_params
        action = qp.get("action")
        app_id = qp.get("aid")
        
        # Fallback to old parameters if aid is missing
        user_id = qp.get("cid")
        company = qp.get("comp")

        if action and (app_id or (user_id and company)):
            # Validate action
            if action not in ["accept", "reject"]:
                return

            render_header()
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">HR Administrative Action</div>', unsafe_allow_html=True)
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Fetch application and user data
            if app_id:
                app = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,)).fetchone()
                if not app:
                    st.error("❌ Application not found.")
                    conn.close()
                    st.stop()
                user = conn.execute("SELECT * FROM users WHERE id = ?", (app['user_id'],)).fetchone()
                target_company = app['company']
            else:
                user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
                app = conn.execute("SELECT * FROM applications WHERE user_id = ? AND company = ?", (user_id, company)).fetchone()
                target_company = company

            if not user or not app:
                st.error("❌ User or Application not found.")
                conn.close()
                st.stop()

            # Determine new status
            new_status = "Selected" if action == "accept" else "Rejected"
            status_color = "#28a745" if new_status == "Selected" else "#dc3545"

            # Update Application in DB
            cursor.execute("""
                UPDATE applications 
                SET status = ? 
                WHERE id = ?
            """, (new_status, app['id']))
            
            if cursor.rowcount > 0:
                conn.commit()
                st.markdown(f"""
                <div style="background: {status_color}; padding: 20px; border-radius: 10px; text-align: center; color: white; margin-bottom: 20px;">
                    <h2>Action: {new_status.upper()}</h2>
                    <p>Candidate: <b>{user['name']}</b></p>
                    <p>Company: <b>{target_company}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show candidate details to HR for verification
                st.markdown("### 📋 Candidate Profile Details")
                st.markdown(f"""
                <div class="premium-card" style="padding: 20px; background: rgba(255,255,255,0.05);">
                    <p><b>Name:</b> {user['name']}</p>
                    <p><b>Email:</b> {user['email']}</p>
                    <p><b>Academic CGPA:</b> {app['cgpa']}</p>
                    <p><b>Skills:</b> {app['skills']}</p>
                    <p><b>College:</b> {app['college_name']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Send Email to Candidate
                with st.spinner(f"Sending notification email to {user['email']}..."):
                    try:
                        send_update_to_candidate(user['email'], new_status, target_company)
                        st.success(f"✅ Notification email successfully sent to candidate.")
                    except Exception as e:
                        st.error(f"⚠️ Database updated, but failed to send email: {e}")
                
            else:
                st.warning(f"⚠️ Failed to update application status.")
            
            conn.close()
            
            if st.button("Home"):
                st.query_params.clear()
                st.session_state.page = "home"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
            
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

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Additional login options
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🏢 EMPLOYER / ADMIN LOGIN", use_container_width=True):
            st.session_state.page = "admin_login"
            st.rerun()
    with col_b:
        if st.button("👔 HR LOGIN", use_container_width=True):
            st.session_state.page = "hr_login"
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
    
    # Age eligibility notice
    st.markdown("""
    <div style="background: rgba(255, 183, 3, 0.15); padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #ffb703;">
        <strong style="color: #ffb703;">📋 Eligibility Criteria:</strong>
        <p style="color: #e0e0e0; margin: 5px 0 0 0; font-size: 14px;">
            Only candidates aged <strong>21 to 24 years</strong> are eligible for this internship program.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate age range for date picker
    import datetime
    today = datetime.date.today()
    # For 21 years: born between today - 24 years and today - 21 years
    max_dob = datetime.date(today.year - 21, today.month, today.day)  # Must be at least 21
    min_dob = datetime.date(today.year - 24, today.month, today.day)  # Must be at most 24
    
    with st.form("registration_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="Enter your full name")
            phone = st.text_input("Phone Number", placeholder="+91 XXXXXXXXXX")
            dob = st.date_input(
                "Date of Birth (Age: 21-24 years)", 
                min_value=min_dob,
                max_value=max_dob,
                help=f"You must be between 21 and 24 years old. Valid dates: {min_dob.strftime('%d-%m-%Y')} to {max_dob.strftime('%d-%m-%Y')}"
            )
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
        submit_btn = st.form_submit_button("✨ CREATE ACCOUNT", use_container_width=True)
        
        if submit_btn:
            # Validate required fields
            if not name or not email or not password or blood_group == "Select Blood Group":
                st.error("⚠️ Please fill in all required fields!")
            elif bank_account and len(bank_account) != 11:
                st.error("⚠️ Bank Account Number must be exactly 11 digits!")
            else:
                # Calculate age from DOB
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                
                # Validate age (21-24 years)
                if age < 21:
                    st.error(f"❌ You must be at least 21 years old to register. Your current age: {age} years")
                elif age > 24:
                    st.error(f"❌ You must be at most 24 years old to register. Your current age: {age} years")
                else:
                    # Age is valid, proceed with registration
                    if register_user((name, email, phone, password, str(dob), district, rural, 
                                    social_category, aadhaar, address, blood_group, bank_account)):
                        st.success(f"✅ Registration Successful! (Age: {age} years) Please login to continue.")
                        st.balloons()
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("❌ Registration failed. Email may already exist or there was a database error.")
    
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
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        login_btn = st.form_submit_button("🚀 LOGIN", use_container_width=True)
        
        if login_btn:
            if not email or not password:
                st.error("⚠️ Please enter both email and password!")
            else:
                user = login_user(email, password)
                if user:
                    st.session_state.user = dict(user)
                    st.success(f"✅ Welcome back, {st.session_state.user['name']}!")
                    role = st.session_state.user.get('role', 'student')
                    if role == 'admin':
                        st.session_state.page = "employer_dashboard"
                    else:
                        st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_home_login"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ADMIN LOGIN ----------------
def admin_login():
    render_header()
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏢 Admin / Employer Login</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-section" style="background: rgba(255, 183, 3, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <b>ℹ️ Admin Access</b><br>
        This portal is for administrators and employers to manage internship applications.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        email = st.text_input("Admin Email Address", placeholder="admin@internship.gov.in")
        password = st.text_input("Password", type="password", placeholder="Enter admin password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        login_btn = st.form_submit_button("🚀 LOGIN AS ADMIN", use_container_width=True)
        
        if login_btn:
            if not email or not password:
                st.error("⚠️ Please enter both email and password!")
            else:
                user = login_user(email, password)
                if user:
                    # Convert sqlite3.Row to dictionary
                    user_dict = dict(user)
                    # Check if user has admin role
                    if user_dict.get('role') == 'admin':
                        st.session_state.user = user_dict
                        st.success(f"✅ Welcome, {st.session_state.user['name']}!")
                        st.session_state.page = "employer_dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Access Denied: This account does not have admin privileges.")
                else:
                    st.error("❌ Invalid credentials. Please try again.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show default admin credentials hint
    with st.expander("🔑 Default Admin Credentials"):
        st.code("Email: admin@internship.gov.in\nPassword: admin123")
        st.info("Use these credentials to access the admin dashboard.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_home_admin_login"):
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
                <div class="profile-info">
                    <span class="profile-info-icon">🏷️</span>
                    <span>{user['social_category'] or 'Not provided'}</span>
                </div>
                 <div class="profile-info">
                    <span class="profile-info-icon">🏞️</span>
                    <span>{user['rural'] or 'Not provided'}</span>
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
            # Better status colors
            if app['status'] == 'Selected':
                status_color = "#28a745" # Green
            elif app['status'] == 'Rejected':
                status_color = "#dc3545" # Red
            else:
                status_color = "#ffb703" # Yellow/Orange for Applied/Pending
            
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
        
        # Location preference with "Any Location" option
        location_choice = st.radio("Location Preference", ["Any Location", "Specific Location"], horizontal=True, key="location_choice")
        if location_choice == "Specific Location":
            location_pref = st.text_input("Enter Preferred Location", placeholder="City or State (e.g., Bangalore, Mumbai)", key="location_input")
        else:
            location_pref = "Any Location"
        
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
            # Validate skills input - check for invalid characters and patterns
            import re
            
            # Remove whitespace and check if it's only numbers
            skills_trimmed = skills.strip().replace(" ", "").replace("\n", "").replace(",", "").replace(".", "")
            if skills_trimmed.isdigit():
                st.error("⚠️ Invalid input! Technical skills cannot be only numbers. Please enter valid skills like 'Python, Java, Communication Skills' etc.")
                st.stop()
            
            # Check if input contains at least some letters (must have actual skill names)
            if not re.search(r'[a-zA-Z]{2,}', skills):
                st.error("⚠️ Invalid input! Please enter valid technical skills with proper names (e.g., Python, Java, Communication).")
                st.stop()
            
            # Allow letters, numbers, spaces, commas, periods, hyphens, plus signs, parentheses, slashes, ampersands, and newlines
            valid_skills_pattern = r'^[a-zA-Z0-9\s,.\-+()/&\n]+$'
            if not re.match(valid_skills_pattern, skills):
                st.error("⚠️ Invalid characters detected! Please use only letters, numbers, and common punctuation (comma, period, hyphen, etc.).")
                st.stop()
            
            # ============ SPELL CHECKING ============
            has_spelling_errors, spelling_suggestions = check_spelling_and_suggest(skills)
            
            if has_spelling_errors:
                st.error("⚠️ **Spelling errors detected in your technical skills!**")
                st.markdown("### 📝 Spelling Corrections Needed")
                st.markdown("Please review and correct the following spelling mistakes before submitting:")
                
                # Display suggestions in a nice format
                for misspelled, suggestions in spelling_suggestions.items():
                    st.markdown(f"""
                    <div style="background: rgba(220, 53, 69, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #dc3545;">
                        <div style="color: #dc3545; font-weight: 700; margin-bottom: 8px;">
                            ❌ Possible misspelling: <span style="background: rgba(220, 53, 69, 0.2); padding: 4px 8px; border-radius: 5px;">{misspelled}</span>
                        </div>
                        <div style="color: #28a745; font-weight: 600; margin-top: 8px;">
                            ✅ Did you mean: {', '.join([f'<span style="background: rgba(40, 167, 69, 0.2); padding: 4px 8px; border-radius: 5px; margin: 0 4px;">{s}</span>' for s in suggestions])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.warning("💡 **Tip:** Please correct the spelling errors in the Technical Skills field above and try submitting again.")
                st.info("ℹ️ If you believe your skill is spelled correctly and is not in our dictionary, you may ignore this suggestion. However, please double-check for typos.")
                st.stop()
            
            # Convert percentage strings to floats
            try:
                cgpa = float(cgpa_str) if cgpa_str else 0.0
                perc_12th = float(perc_12th_str) if perc_12th_str else 0.0
            except ValueError:
                st.error("⚠️ Please enter valid numbers for CGPA and Percentage!")
                return
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO applications 
                (user_id, skills, sector, company, location_pref, languages, perc_12th, college_name, cgpa, experience, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (st.session_state.user['id'], skills, sector, company, location_pref, 
                  languages, perc_12th, college_name, cgpa, experience, "Applied"))
            app_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Email sending with comprehensive error handling
            try:
                # Prepare data dictionary exactly as expected by strictly typed email service
                app_data = {
                    'app_id': app_id, # Added app_id for precise tracking
                    'skills': skills,
                    'sector': sector,
                    'company': company or 'General Pool',
                    'college_name': college_name or 'Not provided',
                    'cgpa': cgpa,
                    'languages': languages or 'Not provided',
                    'experience': experience
                }
                
                # Show spinner while sending
                with st.spinner("Submitting application and notifying HR..."):
                     # Notify HR
                     send_hr_announcement(st.session_state.user, app_data)
                     # Notify Candidate (The User)
                     send_candidate_confirmation(st.session_state.user, app_data)
                     
            except Exception as e:
                st.warning(f"⚠️ Application stored in database, but there was an issue sending notification emails: {e}")
                # We still continue because the application is saved in DB
            
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
            if app['status'] == 'Selected':
                status_color = "#28a745"
            elif app['status'] == 'Rejected':
                status_color = "#dc3545"
            elif app['status'] == 'Waiting List':
                status_color = "#ffc107"
            else:
                status_color = "#ffb703"
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Calculate deadline info for selected candidates
                deadline_html = ""
                if app['status'] == 'Selected' and app['response_deadline']:
                    try:
                        deadline = datetime.datetime.fromisoformat(app['response_deadline'])
                        now = datetime.datetime.now()
                        time_left = deadline - now
                        
                        if time_left.total_seconds() > 0:
                            hours_left = int(time_left.total_seconds() // 3600)
                            minutes_left = int((time_left.total_seconds() % 3600) // 60)
                            
                            # Color based on time remaining
                            if hours_left > 24:
                                timer_color = "#28a745"
                                timer_icon = "✅"
                            elif hours_left > 12:
                                timer_color = "#ffc107"
                                timer_icon = "⚠️"
                            else:
                                timer_color = "#dc3545"
                                timer_icon = "⏰"
                            
                            deadline_html = f"""
                            <div style="margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 8px; border-left: 3px solid {timer_color};">
                                <div style="font-size: 12px; color: #888; margin-bottom: 5px;">{timer_icon} Offer Deadline</div>
                                <div style="font-size: 14px; font-weight: 700; color: {timer_color};">
                                    {hours_left}h {minutes_left}m remaining
                                </div>
                                <div style="font-size: 11px; color: #b8b8b8; margin-top: 3px;">
                                    Expires: {deadline.strftime('%b %d, %Y at %I:%M %p')}
                                </div>
                            </div>
                            """
                        else:
                            deadline_html = f"""
                            <div style="margin-top: 10px; padding: 10px; background: rgba(220, 53, 69, 0.2); border-radius: 8px; border-left: 3px solid #dc3545;">
                                <div style="font-size: 12px; color: #dc3545; font-weight: 700;">⏰ Offer Expired</div>
                                <div style="font-size: 11px; color: #b8b8b8; margin-top: 3px;">
                                    Will be moved to waiting list soon
                                </div>
                            </div>
                            """
                    except:
                        pass
                
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <div style="font-size: 20px; font-weight: 700; color: #ffb703;">
                                {app['sector']} Internship
                            </div>
                            <div style="font-size: 14px; color: #b8b8b8; margin-top: 8px;">
                                📅 Applied: {app['created_at']}<br>
                                🏢 Company: {app['company'] or 'Any'}<br>
                                📍 Location: {app['location_pref'] or 'Any'}
                            </div>
                            {deadline_html}
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
    # Fetch application with full user details
    app = conn.execute("""
        SELECT a.*, u.name, u.email, u.phone, u.dob, u.district, u.rural, 
               u.social_category, u.aadhaar, u.address, u.blood_group, u.bank_account
        FROM applications a
        JOIN users u ON a.user_id = u.id
        WHERE a.id = ?
    """, (st.session_state.selected_app_id,)).fetchone()
    conn.close()
    
    if not app:
        st.error("Application not found!")
        st.session_state.page = "dashboard"
        st.rerun()
        return
    
    app_dict = dict(app)
    
    if app_dict['status'] == 'Selected':
        status_color = "#28a745"
    elif app_dict['status'] == 'Rejected':
        status_color = "#dc3545"
    elif app_dict['status'] == 'Waiting List':
        status_color = "#ffc107"
    else:
        status_color = "#ffb703"
    
    st.markdown(f"""
    <div class="app-detail-card">
        <div class="app-detail-header">
            📋 Application Details
            <span style="float: right; background: {status_color}; color: white; padding: 8px 20px; border-radius: 20px; font-size: 16px;">
                {app_dict['status']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show offer expiration for selected candidates
    if app_dict['status'] == 'Selected' and app_dict['response_deadline']:
        try:
            deadline = datetime.datetime.fromisoformat(app_dict['response_deadline'])
            now = datetime.datetime.now()
            time_left = deadline - now
            
            if time_left.total_seconds() > 0:
                hours_left = int(time_left.total_seconds() // 3600)
                minutes_left = int((time_left.total_seconds() % 3600) // 60)
                
                # Color based on time remaining
                if hours_left > 24:
                    timer_color = "#28a745"  # Green
                    timer_icon = "✅"
                elif hours_left > 12:
                    timer_color = "#ffc107"  # Yellow
                    timer_icon = "⚠️"
                else:
                    timer_color = "#dc3545"  # Red
                    timer_icon = "⏰"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(255, 183, 3, 0.1)); 
                            padding: 25px; border-radius: 15px; margin: 20px 0; 
                            border-left: 5px solid {timer_color}; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <div style="font-size: 18px; font-weight: 700; color: #ffb703; margin-bottom: 10px;">
                                {timer_icon} Internship Offer Deadline
                            </div>
                            <div style="font-size: 14px; color: #b8b8b8; margin-bottom: 15px;">
                                You must respond to this offer before the deadline expires
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;">
                                    <div style="font-size: 12px; color: #888; margin-bottom: 5px;">Offer Ends On</div>
                                    <div style="font-size: 16px; font-weight: 700; color: #fff;">
                                        📅 {deadline.strftime('%B %d, %Y')}
                                    </div>
                                    <div style="font-size: 14px; color: #ffb703; margin-top: 5px;">
                                        🕐 {deadline.strftime('%I:%M %p')}
                                    </div>
                                </div>
                                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;">
                                    <div style="font-size: 12px; color: #888; margin-bottom: 5px;">Time Remaining</div>
                                    <div style="font-size: 28px; font-weight: 800; color: {timer_color};">
                                        {hours_left}h {minutes_left}m
                                    </div>
                                    <div style="font-size: 12px; color: #888; margin-top: 5px;">
                                        ({time_left.days} days remaining)
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Deadline has passed
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(220, 53, 69, 0.2), rgba(220, 53, 69, 0.1)); 
                            padding: 25px; border-radius: 15px; margin: 20px 0; 
                            border-left: 5px solid #dc3545; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <div style="font-size: 18px; font-weight: 700; color: #dc3545; margin-bottom: 10px;">
                        ⏰ Offer Deadline Expired
                    </div>
                    <div style="font-size: 14px; color: #b8b8b8;">
                        The offer deadline was: <strong>{deadline.strftime('%B %d, %Y at %I:%M %p')}</strong>
                    </div>
                    <div style="font-size: 14px; color: #dc3545; margin-top: 10px;">
                        This application will be moved to the waiting list in the next automatic check.
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            pass  # If there's any error parsing the deadline, just don't show it
    
    # Application Information
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("#### 📌 Basic Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">Application ID:</div>
            <div class="app-detail-value">#{app_dict['id']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Sector:</div>
            <div class="app-detail-value">{app_dict['sector']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Preferred Company:</div>
            <div class="app-detail-value">{app_dict['company'] or 'Any Company'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">Applied On:</div>
            <div class="app-detail-value">{app_dict['created_at']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Location Preference:</div>
            <div class="app-detail-value">{app_dict['location_pref'] or 'Any Location'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Status:</div>
            <div class="app-detail-value">{app_dict['status']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 👤 Personal Details")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">Full Name:</div>
            <div class="app-detail-value">{app_dict['name']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Email:</div>
            <div class="app-detail-value">{app_dict['email']}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Phone:</div>
            <div class="app-detail-value">{app_dict['phone'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Date of Birth:</div>
            <div class="app-detail-value">{app_dict['dob'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Blood Group:</div>
            <div class="app-detail-value">{app_dict['blood_group'] or 'Not provided'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">District:</div>
            <div class="app-detail-value">{app_dict['district'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Area Type:</div>
            <div class="app-detail-value">{app_dict['rural'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Social Category:</div>
            <div class="app-detail-value">{app_dict['social_category'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Aadhaar Number:</div>
            <div class="app-detail-value">{app_dict['aadhaar'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Bank Account:</div>
            <div class="app-detail-value">{app_dict['bank_account'] or 'Not provided'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Address in full width
    st.markdown(f"""
    <div class="app-detail-row">
        <div class="app-detail-label">Address:</div>
        <div class="app-detail-value">{app_dict['address'] or 'Not provided'}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎓 Education & Qualifications")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">College/University:</div>
            <div class="app-detail-value">{app_dict['college_name'] or 'Not provided'}</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">CGPA:</div>
            <div class="app-detail-value">{app_dict['cgpa'] if app_dict['cgpa'] else 'Not provided'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="app-detail-row">
            <div class="app-detail-label">12th Grade %:</div>
            <div class="app-detail-value">{app_dict['perc_12th'] if app_dict['perc_12th'] else 'Not provided'}%</div>
        </div>
        <div class="app-detail-row">
            <div class="app-detail-label">Languages Known:</div>
            <div class="app-detail-value">{app_dict['languages'] or 'Not provided'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💼 Skills & Experience")
    
    st.markdown(f"""
    <div class="app-detail-row">
        <div class="app-detail-label">Technical Skills:</div>
        <div class="app-detail-value">{app_dict['skills'] or 'Not provided'}</div>
    </div>
    <div class="app-detail-row">
        <div class="app-detail-label">Prior Experience:</div>
        <div class="app-detail-value">{app_dict['experience'] or 'No prior experience'}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.user.get('role') == 'admin':
             if st.button("← Back to Admin Dashboard"):
                st.session_state.page = "employer_dashboard"
                st.rerun()
        else:
            if st.button("← Back to All Applications"):
                st.session_state.page = "view_applications"
                st.rerun()
    with col2:
        if st.session_state.user.get('role') != 'admin':
            if st.button("← Back to Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()

# ---------------- EMPLOYER DASHBOARD ----------------
def employer_dashboard():
    # Security Check - Only Admin can access
    if not st.session_state.user or st.session_state.user.get('role') != 'admin':
        st.session_state.page = "admin_login"
        st.rerun()
        return

    render_header()

    
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏢 Admin Dashboard - View & Monitor</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255, 183, 3, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <b>ℹ️ Admin View:</b> Monitor all applications, view candidate details, and track company-wise statistics.
    </div>
    """, unsafe_allow_html=True)
    
    # Company Selection
    company_options = [
        "All Companies",
        "Tata Consultancy Services (TCS)", "Infosys Ltd.", "Wipro Ltd.", "HCL Technologies Ltd.", 
        "Tech Mahindra Ltd.", "Reliance Industries Ltd.", "HDFC Bank Ltd.", "ICICI Bank Ltd.", "Mahindra & Mahindra Ltd."
    ]
    
    
    selected_company = st.selectbox("Select Company to View", company_options)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    conn = get_connection()
    
    # Get overall statistics
    total_applications = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    total_candidates = conn.execute("SELECT COUNT(*) FROM users WHERE role != 'admin'").fetchone()[0]
    total_selected = conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'Selected'").fetchone()[0]
    total_pending = conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'Applied'").fetchone()[0]
    
    # Company-wise statistics
    company_stats = conn.execute("""
        SELECT company, COUNT(*) as app_count, 
               SUM(CASE WHEN status = 'Selected' THEN 1 ELSE 0 END) as selected_count,
               SUM(CASE WHEN status = 'Applied' THEN 1 ELSE 0 END) as pending_count
        FROM applications 
        WHERE company IS NOT NULL AND company != ''
        GROUP BY company 
        ORDER BY app_count DESC
    """).fetchall()
    
    # Display Overall Statistics
    st.markdown("### 📊 Overall Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📝 Total Applications", total_applications)
    col2.metric("👥 Total Candidates", total_candidates)
    col3.metric("✅ Selected", total_selected)
    col4.metric("⏳ Pending", total_pending)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Company-wise Application Statistics
    st.markdown("### 🏢 Company-wise Application Statistics")
    if company_stats:
        st.markdown("""
        <div style="background: rgba(255, 183, 3, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <b>ℹ️ Overview:</b> This shows how many applications each company has received.
        </div>
        """, unsafe_allow_html=True)
        
        # Create a nice table view
        for comp_stat in company_stats:
            comp_stat_dict = dict(comp_stat)
            st.markdown(f"""
            <div class="stat-card" style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 2;">
                        <div style="font-size: 18px; font-weight: 700; color: #ffb703;">
                            🏢 {comp_stat_dict['company']}
                        </div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: #fff;">
                            {comp_stat_dict['app_count']}
                        </div>
                        <div style="font-size: 12px; color: #b8b8b8;">Total Applications</div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <div style="font-size: 20px; font-weight: 700; color: #28a745;">
                            {comp_stat_dict['selected_count']}
                        </div>
                        <div style="font-size: 12px; color: #b8b8b8;">Selected</div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <div style="font-size: 20px; font-weight: 700; color: #ffb703;">
                            {comp_stat_dict['pending_count']}
                        </div>
                        <div style="font-size: 12px; color: #b8b8b8;">Pending</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No applications received yet.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # AI Processing Control Panel
    st.markdown("### 🤖 AI Selection Control Panel")
    st.markdown("""
    <div style="background: rgba(255, 183, 3, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <b>ℹ️ AI Auto-Selector:</b> Manually trigger the AI to process all pending applications. 
        The AI will rank candidates and assign statuses: 1st = Selected (48hr deadline), 2nd = Shortlisted, 3rd+ = Waiting List.
        Notifications will be sent in order: 3rd → 2nd → 1st, and HR will be notified when complete.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🚀 Run AI Selection Process for All Companies", use_container_width=True, type="primary"):
            from ai_auto_selector import process_all_companies
            with st.spinner("🤖 AI is processing applications... This may take a few moments."):
                try:
                    process_all_companies()
                    st.success("✅ AI processing complete! All companies have been processed. Candidates have been ranked and notified.")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error during AI processing: {str(e)}")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(40, 167, 69, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
            <div style="font-size: 12px; color: #28a745; font-weight: 600;">AUTO-RUN</div>
            <div style="font-size: 10px; color: #b8b8b8; margin-top: 5px;">Every 30 min</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Fetch applicants with full personal details
    if selected_company == "All Companies":
        query = """
            SELECT a.*, u.name, u.email, u.phone, u.dob, u.district, u.rural, 
                   u.social_category, u.aadhaar, u.address, u.blood_group, u.bank_account
            FROM applications a 
            JOIN users u ON a.user_id = u.id 
            ORDER BY a.created_at DESC
        """
        applicants = conn.execute(query).fetchall()
    else:
        query = """
            SELECT a.*, u.name, u.email, u.phone, u.dob, u.district, u.rural, 
                   u.social_category, u.aadhaar, u.address, u.blood_group, u.bank_account
            FROM applications a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.company = ?
            ORDER BY a.created_at DESC
        """
        applicants = conn.execute(query, (selected_company,)).fetchall()
    conn.close()
    
    candidates_list = [dict(row) for row in applicants]
    
    # Statistics for selected company/all
    total_apps = len(candidates_list)
    pending_apps = len([a for a in candidates_list if a['status'] == 'Applied'])
    selected_apps = len([a for a in candidates_list if a['status'] == 'Selected'])
    
    st.markdown(f"### 📋 Applications for: **{selected_company}**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applications", total_apps)
    col2.metric("Pending Review", pending_apps)
    col3.metric("Selected", selected_apps)


    # View Applications Section
    st.markdown("### �️ View All Applications")
    
    
    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search by Candidate ID, Name or Email", placeholder="Type to search...")
    with col2:
        filter_status = st.selectbox("Filter Status", ["All", "Applied", "Selected", "Rejected"])

    # Filter Logic
    filtered_list = candidates_list
    if filter_status != "All":
        filtered_list = [a for a in filtered_list if a['status'] == filter_status]
    
    if search_query:
        query = search_query.lower()
        filtered_list = [a for a in filtered_list if 
                        query in str(a['user_id']).lower() or 
                        query in a['name'].lower() or 
                        query in a['email'].lower()]
    
    if filtered_list:
        # Table Header - simplified for view-only
        h1, h2, h3, h4, h5, h6 = st.columns([0.5, 1.5, 2, 1.5, 1, 1])
        h1.markdown("**ID**")
        h2.markdown("**Name**")
        h3.markdown("**Email**")
        h4.markdown("**Company**")
        h5.markdown("**Status**")
        h6.markdown("**Action**")
        st.divider()
        
        # Rendering actual rows - view only
        for app in filtered_list:
            with st.container():
                c1, c2, c3, c4, c5, c6 = st.columns([0.5, 1.5, 2, 1.5, 1, 1])
                c1.write(f"#{app['user_id']}")
                
                # Make name clickable
                with c2:
                    if st.button(f"👤 {app['name']}", key=f"name_{app['id']}", help="Click to view full details", use_container_width=True):
                        st.session_state.selected_app_id = app['id']
                        st.session_state.page = "application_detail"
                        st.rerun()
                
                c3.write(app['email'])
                c4.write(app['company'] or 'Any')
                
                status_color = "orange"
                if app['status'] == 'Selected': status_color = "green"
                if app['status'] == 'Rejected': status_color = "red"
                if app['status'] == 'Waiting List': status_color = "yellow"
                c5.markdown(f":{status_color}[{app['status']}]")
                
                with c6:
                    if st.button("👁️ View", key=f"view_{app['id']}", help="View Details", use_container_width=True):
                        st.session_state.selected_app_id = app['id']
                        st.session_state.page = "application_detail"
                        st.rerun()
                st.markdown("---")
    else:
        st.info("ℹ️ No applications found matching your criteria.")
    
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            st.success("✅ Logged out successfully!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- HR LOGIN ----------------
def hr_login_page():
    from hr_auth import hr_login
    
    render_header()
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏢 HR Portal Login</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; color: #b8b8b8;">
        <p>Welcome to the HR Dashboard. Please login with your company credentials.</p>
        <p style="font-size: 12px; color: #666;">Format: 1208_companyname_HR</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("hr_login_form"):
        username = st.text_input("HR Username", placeholder="1208_zoho_HR")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        login_btn = st.form_submit_button("🚀 LOGIN AS HR", use_container_width=True)
        
        if login_btn:
            if not username or not password:
                st.error("⚠️ Please enter both username and password!")
            else:
                hr_user = hr_login(username, password)
                if hr_user:
                    st.session_state.hr_user = hr_user
                    st.success(f"✅ Welcome, {hr_user['company']} HR!")
                    st.session_state.page = "hr_dashboard"
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_home_hr_login"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- HR DASHBOARD ----------------
def hr_dashboard():
    from hr_auth import get_company_info, update_seat_allocation
    from ai_engine import ai_filter_candidates, get_top_candidates
    import datetime
    
    # Check if HR is logged in
    if 'hr_user' not in st.session_state or not st.session_state.hr_user:
        st.warning("⚠️ Please login as HR first")
        st.session_state.page = "hr_login"
        st.rerun()
        return
    
    hr_user = st.session_state.hr_user
    company_name = hr_user['company']
    
    render_header()
    
    # Header with company info
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 30px; border-radius: 20px; margin-bottom: 30px; 
                border: 2px solid #ffb703; box-shadow: 0 10px 40px rgba(255, 183, 3, 0.2);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="color: #ffb703; margin: 0; font-size: 32px;">🏢 {company_name} - HR Dashboard</h1>
                <p style="color: #b8b8b8; margin: 10px 0 0 0;">Welcome, {hr_user['username']}</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 14px; color: #666;">Logged in as HR</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get company info
    company_info = get_company_info(company_name)
    
    if company_info:
        # Display seat allocation info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card" style="border-top: 4px solid #28a745;">
                <div class="stat-number">{company_info['total_seats']}</div>
                <div class="stat-label">Total Seats</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card" style="border-top: 4px solid #dc3545;">
                <div class="stat-number">{company_info['allocated_seats']}</div>
                <div class="stat-label">Allocated Seats</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card" style="border-top: 4px solid #ffb703;">
                <div class="stat-number">{company_info['available_seats']}</div>
                <div class="stat-label">Available Seats</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different sections
    tab0, tab1, tab2, tab3, tab4 = st.tabs(["⏳ Review Required", "📋 All Applications", "🤖 AI Filtered Candidates", "✅ Selected", "⏰ Response Tracking"])
    
    # Get all applications for this company
    conn = get_connection()
    from waiting_list_manager import select_candidates_and_create_waiting_list, handle_hr_decision

    # Tab 0: Review Required (New Flow)
    with tab0:
        st.markdown("### ⏳ Top Candidates Pending Your Approval")
        st.info("ℹ️ These candidates have been ranked #1 by the AI. Please review and Approve or Decline.")
        
        pending_review = conn.execute("""
            SELECT a.*, u.name, u.email, u.phone, u.district, u.rural, u.social_category
            FROM applications a
            JOIN users u ON a.user_id = u.id
            WHERE a.company = ? AND a.status = 'Review Pending'
            ORDER BY a.ai_score DESC
        """, (company_name,)).fetchall()
        
        if not pending_review:
            st.success("✨ All pending reviews are complete!")
        else:
            for app in pending_review:
                st.markdown(f"""
                <div class="app-detail-card" style="border-left: 5px solid #ffb703; background: rgba(255, 183, 3, 0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h3 style="margin: 0; color: #fff;">{app['name']}</h3>
                            <p style="color: #b8b8b8; margin: 5px 0;">{app['email']} | {app['district']}</p>
                            <p><b>AI Score:</b> <span style="color: #ffb703; font-weight: bold;">{app['ai_score']}</span></p>
                            <p><b>Skills:</b> {app['skills']}</p>
                            <p><b>College:</b> {app['college_name']} | <b>CGPA:</b> {app['cgpa']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"✅ Approve {app['name']}", key=f"hr_approve_{app['id']}", use_container_width=True):
                        success, msg = handle_hr_decision(app['id'], hr_user['username'], 'Accept')
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                
                with col2:
                    # Logic for Rejection with Mandatory Reason
                    if f"show_reject_reason_{app['id']}" not in st.session_state:
                        if st.button(f"❌ Decline Profile", key=f"hr_pre_reject_{app['id']}", use_container_width=True):
                            st.session_state[f"show_reject_reason_{app['id']}"] = True
                            st.rerun()
                    
                    if st.session_state.get(f"show_reject_reason_{app['id']}"):
                        reason = st.text_area("Reason for Rejection (Required for Admin Audit)", key=f"reason_text_{app['id']}", placeholder="e.g., Skills do not match project specifics...")
                        if st.button("Submit Rejection & Promote Backup", key=f"hr_submit_reject_{app['id']}", use_container_width=True, type="primary"):
                            if not reason:
                                st.error("⚠️ You MUST provide a reason to reject a top candidate.")
                            else:
                                success, msg = handle_hr_decision(app['id'], hr_user['username'], 'Reject', reason)
                                if success:
                                    st.session_state[f"show_reject_reason_{app['id']}"] = False
                                    st.warning(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                        if st.button("Cancel", key=f"cancel_reject_{app['id']}"):
                            st.session_state[f"show_reject_reason_{app['id']}"] = False
                            st.rerun()

    # Tab 1: All Applications
    with tab1:
        st.markdown("### 📋 All Applications for " + company_name)
        
        applications = conn.execute("""
            SELECT a.*, u.name, u.email, u.phone, u.district, u.rural, u.social_category
            FROM applications a
            JOIN users u ON a.user_id = u.id
            WHERE a.company = ?
            ORDER BY a.created_at DESC
        """, (company_name,)).fetchall()
        
        if not applications:
            st.info("ℹ️ No applications received yet.")
        else:
            st.success(f"📊 Total Applications: **{len(applications)}**")
            
            for app in applications:
                status_color = {
                    'Applied': '#ffc107',
                    'Review Pending': '#ffb703',
                    'Shortlisted': '#17a2b8',
                    'Selected': '#28a745',
                    'Rejected': '#dc3545',
                    'Waiting List': '#ff9800'
                }.get(app['status'], '#666')
                
                st.markdown(f"""
                <div class="app-detail-card" style="border-left: 5px solid {status_color};">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h3 style="margin: 0; color: #fff;">{app['name']}</h3>
                            <p style="color: #b8b8b8; margin: 5px 0;">{app['email']} | Status: <b>{app['status']}</b></p>
                            <p style="font-size: 13px;"><b>Skills:</b> {app['skills']}</p>
                        </div>
                        <div style="text-align: right;">
                             <div style="background: {status_color}; color: white; padding: 5px 12px; border-radius: 5px; font-size: 11px; font-weight: bold;">
                                AI Score: {app['ai_score'] or 'N/A'}
                             </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Tab 2: AI Filtered Candidates
    with tab2:
        st.markdown("### 🤖 Automated AI Selection System")
        st.info("ℹ️ Click the button below to automatically rank all 'Applied' candidates and trigger the selection workflow.")
        
        if st.button("🚀 Run AI Selection & Ranking Process", use_container_width=True, type="primary"):
            with st.spinner("AI is ranking candidates and preparing notifications..."):
                # Define generic requirements for now
                requirements = {'skills': ''} # Could be pulled from company job desc
                result = select_candidates_and_create_waiting_list(company_name, "Chennai", requirements) # Example location
                st.success(f"✅ Process Complete! {result['review_pending']} candidates moved to Review, {result['shortlisted']} Shortlisted, {result['waiting_list']} on Waiting List.")
                st.rerun()

        st.markdown("---")
        # Get only "Applied" status applications for preview
        pending_apps = conn.execute("""
            SELECT a.*, u.name, u.email, u.phone, u.district, u.rural, u.social_category
            FROM applications a
            JOIN users u ON a.user_id = u.id
            WHERE a.company = ? AND a.status = 'Applied'
        """, (company_name,)).fetchall()
        
        if pending_apps:
            st.markdown("#### 🔍 Candidate Preview (AI Rankings)")
            # Convert to list of dicts
            candidates_list = [dict(app) for app in pending_apps]
            all_ranked = ai_filter_candidates(candidates_list, {'skills': ''})
            
            for rank, item in enumerate(all_ranked, 1):
                cand = item['data']
                score = item['score']
                st.markdown(f"**#{rank} {cand['name']}** - AI Score: `{score}`")
        else:
            st.write("No 'Applied' candidates left to process.")
            
            # Waiting List
            if waiting_list:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown("### ⏳ Waiting List")
                st.info(f"📊 {len(waiting_list)} candidates in waiting list")
                
                for rank, item in enumerate(waiting_list, available_seats + 1):
                    cand = item['data']
                    score = item['score']
                    
                    st.markdown(f"""
                    <div class="app-detail-card" style="border-left: 5px solid #666; opacity: 0.7;">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <h4 style="margin: 0; color: #ccc;">#{rank} {cand['name']}</h4>
                                <p style="color: #888; margin: 5px 0; font-size: 13px;">{cand['email']}</p>
                                <p style="font-size: 13px;"><b>Skills:</b> {cand['skills']} | <b>CGPA:</b> {cand['cgpa']}</p>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 20px; font-weight: 700; color: #666;">{score}</div>
                                <div style="font-size: 11px; color: #555;">Score</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Tab 3: Selected Candidates
    with tab3:
        st.markdown("### ✅ Selected Candidates")
        
        selected = conn.execute("""
            SELECT a.*, u.name, u.email, u.phone
            FROM applications a
            JOIN users u ON a.user_id = u.id
            WHERE a.company = ? AND a.status = 'Selected'
            ORDER BY a.selected_at DESC
        """, (company_name,)).fetchall()
        
        if not selected:
            st.info("ℹ️ No candidates selected yet.")
        else:
            for sel in selected:
                st.markdown(f"""
                <div class="app-detail-card" style="border-left: 5px solid #28a745;">
                    <h3 style="color: #28a745; margin: 0;">{sel['name']}</h3>
                    <p style="color: #b8b8b8; margin: 5px 0;">{sel['email']} | {sel['phone']}</p>
                    <p><b>Skills:</b> {sel['skills']}</p>
                    <p><b>Selected At:</b> {sel['selected_at']}</p>
                    <p><b>Response Deadline:</b> {sel['response_deadline']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Tab 4: Response Tracking
    with tab4:
        st.markdown("### ⏰ 48-Hour Response Tracking")
        st.info("ℹ️ Candidates must respond within 48 hours of selection, or the offer will be automatically moved to waiting list and the next candidate will be selected.")
        
        selected_with_deadline = conn.execute("""
            SELECT a.*, u.name, u.email, u.phone
            FROM applications a
            JOIN users u ON a.user_id = u.id
            WHERE a.company = ? AND a.status = 'Selected' AND a.response_deadline IS NOT NULL
            ORDER BY a.response_deadline ASC
        """, (company_name,)).fetchall()
        
        if not selected_with_deadline:
            st.info("ℹ️ No active offers with deadlines.")
        else:
            now = datetime.datetime.now()
            
            for sel in selected_with_deadline:
                deadline = datetime.datetime.fromisoformat(sel['response_deadline'])
                time_left = deadline - now
                
                if time_left.total_seconds() > 0:
                    hours_left = int(time_left.total_seconds() // 3600)
                    minutes_left = int((time_left.total_seconds() % 3600) // 60)
                    status_color = "#28a745" if hours_left > 12 else "#ffc107" if hours_left > 6 else "#dc3545"
                    
                    st.markdown(f"""
                    <div class="app-detail-card" style="border-left: 5px solid {status_color};">
                        <h3 style="color: #fff; margin: 0;">{sel['name']}</h3>
                        <p style="color: #b8b8b8; margin: 5px 0;">{sel['email']}</p>
                        <p><b>Time Remaining:</b> <span style="color: {status_color}; font-weight: 700; font-size: 18px;">{hours_left}h {minutes_left}m</span></p>
                        <p style="font-size: 12px; color: #666;">Deadline: {sel['response_deadline']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Deadline passed - will be auto-processed
                    st.markdown(f"""
                    <div class="app-detail-card" style="border-left: 5px solid #dc3545; background: rgba(220, 53, 69, 0.1);">
                        <h3 style="color: #dc3545; margin: 0;">⏰ EXPIRED: {sel['name']}</h3>
                        <p style="color: #b8b8b8; margin: 5px 0;">{sel['email']}</p>
                        <p style="color: #dc3545;"><b>Candidate did not respond within 48 hours</b></p>
                        <p style="color: #ffb703; font-size: 12px;">This will be automatically moved to waiting list and the next candidate will be selected in the next hourly check.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Optional manual override
                    if st.button(f"🗑️ Manually Process Now for {sel['name']}", key=f"revoke_{sel['id']}"):
                        conn.execute("UPDATE applications SET status = 'Waiting List', selected_at = NULL, response_deadline = NULL WHERE id = ?", (sel['id'],))
                        update_seat_allocation(company_name, -1)  # Free up the seat
                        conn.commit()
                        st.success("Moved to waiting list and seat freed up!")
                        st.rerun()
    
    conn.close()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=False):
        st.session_state.hr_user = None
        st.session_state.page = "home"
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
elif st.session_state.page == "admin_login":
    admin_login()
elif st.session_state.page == "employer_dashboard":
    employer_dashboard()
elif st.session_state.page == "hr_login":
    hr_login_page()
elif st.session_state.page == "hr_dashboard":
    hr_dashboard()
