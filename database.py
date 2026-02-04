import sqlite3
import os

def get_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = sqlite3.connect('data/internship.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # --- USERS TABLE ---
    # Fields: id, name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account, created_at
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT,
        dob TEXT,
        district TEXT,
        rural TEXT,
        social_category TEXT,
        aadhaar TEXT,
        address TEXT,
        blood_group TEXT,
        bank_account TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --- APPLICATIONS TABLE ---
    # Added all requested fields
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skills TEXT,
        sector TEXT,
        company TEXT,
        location_pref TEXT,
        languages TEXT,
        perc_12th REAL,
        college_name TEXT,
        cgpa REAL,
        experience TEXT,
        status TEXT DEFAULT 'Applied',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        selected_at TIMESTAMP,
        response_deadline TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    # --- HR USERS TABLE ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hr_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        company TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # --- COMPANIES TABLE ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        total_seats INTEGER DEFAULT 1,
        allocated_seats INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --- SCHEMA EVOLUTION (Adding missing columns if they don't exist) ---
    def add_column_if_missing(table, column, definition):
        try:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
            print(f"✅ Added column {column} to {table}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"⚠️ Error adding column {column} to {table}: {e}")

    # Evolution for USERS
    add_column_if_missing('users', 'aadhaar', 'TEXT')
    add_column_if_missing('users', 'address', 'TEXT')
    add_column_if_missing('users', 'blood_group', 'TEXT')
    add_column_if_missing('users', 'bank_account', 'TEXT')
    add_column_if_missing('users', 'role', "TEXT DEFAULT 'student'")

    # Evolution for APPLICATIONS
    add_column_if_missing('applications', 'languages', 'TEXT')
    add_column_if_missing('applications', 'perc_12th', 'REAL')
    add_column_if_missing('applications', 'college_name', 'TEXT')
    add_column_if_missing('applications', 'cgpa', 'REAL')
    add_column_if_missing('applications', 'experience', 'TEXT')
    add_column_if_missing('applications', 'created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    add_column_if_missing('applications', 'selected_at', 'TIMESTAMP')
    add_column_if_missing('applications', 'response_deadline', 'TIMESTAMP')

    seed_admin(cur)
    seed_hr_users(cur)
    seed_companies(cur)

    conn.commit()
    conn.close()



def seed_admin(cur):
    import bcrypt
    
    # Check if admin exists
    cur.execute("SELECT * FROM users WHERE role = 'admin'")
    admin = cur.fetchone()
    
    # Static hashed password for 'admin123'
    # Generated with bcrypt.hashpw(b"admin123", bcrypt.gensalt())
    hashed_password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode('utf-8')
    
    if not admin:
        # Create admin user
        cur.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, ("Administrator", "admin@internship.gov.in", hashed_password, "admin"))
        print("✅ Admin user created: admin@internship.gov.in / admin123")
    else:
        # Update admin password to hashed version if it looks like plain text
        stored_password = admin['password']
        if not stored_password.startswith("$2b$"):
             cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, admin['id']))
             print("✅ Admin password upgraded to hash.")


def seed_hr_users(cur):
    """Seed HR users for different companies"""
    import bcrypt
    
    # HR users: username format: 1208_companyname_HR, password: 1234
    hr_accounts = [
        ("1208_zoho_HR", "1234", "Zoho", "hr@zoho.com"),
        ("1208_infosys_HR", "1234", "Infosys", "hr@infosys.com"),
        ("1208_tcs_HR", "1234", "TCS", "hr@tcs.com"),
        ("1208_wipro_HR", "1234", "Wipro", "hr@wipro.com"),
        ("1208_google_HR", "1234", "Google", "hr@google.com"),
    ]
    
    for username, password, company, email in hr_accounts:
        # Check if HR user already exists
        cur.execute("SELECT * FROM hr_users WHERE username = ?", (username,))
        existing = cur.fetchone()
        
        if not existing:
            # Hash the password
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cur.execute("""
                INSERT INTO hr_users (username, password, company, email)
                VALUES (?, ?, ?, ?)
            """, (username, hashed_pw, company, email))
            print(f"✅ HR user created: {username} / {password} for {company}")


def seed_companies(cur):
    """Seed companies with seat allocation"""
    companies = [
        ("Zoho", 1),
        ("Infosys", 5),
        ("TCS", 10),
        ("Wipro", 3),
        ("Google", 2),
        ("Microsoft", 1),
        ("Amazon", 5),
        ("Flipkart", 3),
    ]
    
    for company_name, seats in companies:
        cur.execute("SELECT * FROM companies WHERE name = ?", (company_name,))
        existing = cur.fetchone()
        
        if not existing:
            cur.execute("""
                INSERT INTO companies (name, total_seats, allocated_seats)
                VALUES (?, ?, 0)
            """, (company_name, seats))
            print(f"✅ Company created: {company_name} with {seats} seats")


if __name__ == "__main__":
    create_tables()
    print("Database finalized successfully.")
