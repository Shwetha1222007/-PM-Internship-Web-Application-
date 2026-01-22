import streamlit as st
from datetime import date
from database import create_tables, get_connection
from auth import register_user, login_user
from email_service import send_hr_email, send_candidate_email

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="PM Internship Scheme", layout="wide")
create_tables()

# -------------------- SESSION STATE --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------- CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #fcfdfe;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* --- HERO SECTION --- */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 60px 40px;
    border-radius: 24px;
    margin-bottom: 40px;
    color: white;
    box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.3);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    top: -50px;
    right: -50px;
    width: 200px;
    height: 200px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    filter: blur(40px);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 1rem;
    background: linear-gradient(to right, #ffffff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 1.25rem;
    color: #cbd5e1;
    max-width: 600px;
    margin-bottom: 2rem;
}

/* --- CARDS --- */
.card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
    height: 100%;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
}

.company-card {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: #475569;
    height: 100px;
    font-size: 1.2rem;
}

/* --- BUTTONS --- */
.stButton>button {
    background: linear-gradient(to right, #2563eb, #3b82f6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    transition: all 0.2s ease;
    width: 100%;
}

.stButton>button:hover {
    background: linear-gradient(to right, #1d4ed8, #2563eb);
    transform: scale(1.02);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3);
}

.stButton>button:active {
    transform: scale(0.98);
}

/* --- HEADERS --- */
h1, h2, h3 {
    color: #0f172a;
    font-weight: 700;
}

/* --- ALERTS & STATUS --- */
.stSuccess {
    background-color: #f0fdf4;
    border-left-color: #22c55e;
}

.stInfo {
    background-color: #eff6ff;
    border-left-color: #3b82f6;
}

/* --- LOGO GRID --- */
.logo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- ELIGIBILITY LOGIC --------------------
def check_eligibility(dob, employed, studying, income, govt_job):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    if age < 21 or age > 24:
        return False, "Age must be between 21 and 24"
    if employed == "Yes":
        return False, "Employed full time"
    if studying == "Yes":
        return False, "Studying full time"
    if income == "Above 8 Lakhs":
        return False, "Income above 8 Lakhs"
    if govt_job == "Yes":
        return False, "Govt job in family"

    return True, "Eligible"

# -------------------- HR ACTION HANDLER --------------------
params = st.query_params
if "action" in params and "cid" in params:
    action = params["action"]
    cid = params["cid"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.email, a.company
        FROM users u
        JOIN applications a ON u.id = a.user_id
        WHERE u.id = ?
    """, (cid,))
    result = cur.fetchone()

    if result:
        email, company = result
        if action == "accept":
            cur.execute("UPDATE applications SET status='Selected' WHERE user_id=?", (cid,))
            send_candidate_email(email, "Selected", company)
        elif action == "reject":
            cur.execute("UPDATE applications SET status='Rejected' WHERE user_id=?", (cid,))

    conn.commit()
    conn.close()

# -------------------- HOME PAGE --------------------
def home_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Future Ready India</div>
        <div class="hero-sub">
            The PM Internship Scheme connects India's brightest youth with top industry leaders. 
            AI-powered allocation ensuring fair and transparent opportunities for everyone.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("""
        ### 🇮🇳 About the Scheme
        - Real industry exposure  
        - Monthly assistance  
        - Top Indian companies  
        - Transparent AI-based allocation  
        """)

        colA, colB = st.columns(2)
        with colA:
            if st.button("📝 Youth Registration"):
                st.session_state.page = "register"
                st.rerun()
        with colB:
            if st.button("🔐 Login"):
                st.session_state.page = "login"
                st.rerun()

    with col2:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/4140/4140048.png",
            use_column_width=True
        )

    st.markdown("### 🏢 Top Industry Partners")
    cols = st.columns(5)
    companies = ["REC", "JSW", "GAIL", "Cognizant", "L&T"]
    for i in range(5):
        with cols[i]:
            st.markdown(f"<div class='card company-card'>{companies[i]}</div>", unsafe_allow_html=True)

# -------------------- REGISTRATION --------------------
def register_page():
    st.markdown("## 📝 PM Internship Registration")

    with st.form("registration_form"):

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")

        # 👉 IDHU THAAN CORRECT PLACE 👇
        min_dob = date.today().replace(year=date.today().year - 24)
        max_dob = date.today().replace(year=date.today().year - 21)

        dob = st.date_input(
            "Date of Birth",
            min_value=min_dob,
            max_value=max_dob
        )

        submit = st.form_submit_button("Submit Registration")

    if submit:
        st.success("Done")


# -------------------- LOGIN --------------------
def login_page():
    st.markdown("## 🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------------------- DASHBOARD --------------------
def dashboard_page():
    st.markdown("## 📊 Candidate Dashboard")
    st.success(f"Welcome {st.session_state.user[1]}")
    st.write("Candidate ID:", st.session_state.user[0])

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT company, status FROM applications WHERE user_id=?", (st.session_state.user[0],))
    row = cur.fetchone()
    conn.close()

    if row:
        st.info(f"Company: {row[0]}")
        st.success(f"Status: {row[1]}")
    else:
        st.warning("No internship applied yet")

    if st.button("📝 Apply Internship"):
        st.session_state.page = "apply"
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.page = "home"
        st.rerun()

# -------------------- APPLY --------------------
def apply_page():
    st.markdown("## 📝 Apply for Internship")

    with st.form("apply_form"):
        skills = st.text_input("Skills")
        sector = st.selectbox("Sector", ["IT", "Manufacturing"])
        company = st.text_input("Company")
        submit = st.form_submit_button("Submit")

    if submit:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO applications (user_id, skills, sector, company, status)
            VALUES (?, ?, ?, ?, ?)
        """, (st.session_state.user[0], skills, sector, company, "Applied"))
        conn.commit()
        conn.close()

        send_hr_email(
            candidate_name=st.session_state.user[1],
            company=company,
            skills=skills,
            candidate_id=st.session_state.user[0]
        )

        st.success("Application submitted")
        st.session_state.page = "dashboard"
        st.rerun()

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


st.markdown("""
<style>
.section {
    margin-top: 40px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #0b3c5d;
    margin-bottom: 15px;
}

.section-text {
    font-size: 16px;
    color: #333;
    line-height: 1.7;
}

.logo-card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.logo-card img {
    height: 60px;
}
</style>
""", unsafe_allow_html=True)
