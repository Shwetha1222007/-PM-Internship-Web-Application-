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
        FOREIGN KEY (user_id) REFERENCES users (id)
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

    seed_admin(cur)

    conn.commit()
    conn.close()

def seed_admin(cur):
    # Check if admin exists
    cur.execute("SELECT * FROM users WHERE role = 'admin'")
    admin = cur.fetchone()
    if not admin:
        # Create admin user
        # You might want to use a more secure password in production/env vars
        cur.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, ("Administrator", "admin@internship.gov.in", "admin123", "admin"))
        print("✅ Admin user created: admin@internship.gov.in / admin123")

if __name__ == "__main__":
    create_tables()
    print("Database finalized successfully.")
