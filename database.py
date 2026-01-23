import sqlite3
import os

def get_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = sqlite3.connect('data/internship.db', check_same_thread=False)
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # --- USERS TABLE ---
    # Fields: id, name, email, phone, dob, district, rural, social_category, password, created_at
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        dob TEXT,
        district TEXT,
        rural TEXT,
        social_category TEXT,
        password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --- APPLICATIONS TABLE ---
    # Fields: id, user_id, skills, sector, company, location_pref, qualification, rural_urban, status, created_at
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skills TEXT,
        sector TEXT,
        company TEXT,
        location_pref TEXT,
        qualification TEXT,
        rural_urban TEXT,
        status TEXT DEFAULT 'Applied',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ROBUST MIGRATION: Ensure all columns exist individually
    def add_col(table, col, definition):
        try:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {definition}")
            print(f"✅ Added column {col} to {table}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                pass # Column already exists
            else:
                print(f"⚠️ Error adding column {col} to {table}: {e}")

    # Check for missing columns in existing tables
    add_col('applications', 'location_pref', 'TEXT')
    add_col('applications', 'qualification', 'TEXT')
    add_col('applications', 'rural_urban', 'TEXT')
    add_col('applications', 'status', "TEXT DEFAULT 'Applied'")
    # SQLite ALTER TABLE cannot add CURRENT_TIMESTAMP as default. We use a constant for the migr.
    add_col('applications', 'created_at', "TIMESTAMP DEFAULT '2024-01-22 00:00:00'")
    
    add_col('users', 'dob', 'TEXT')
    add_col('users', 'created_at', "TIMESTAMP DEFAULT '2024-01-22 00:00:00'")

    conn.commit()
    conn.close()
