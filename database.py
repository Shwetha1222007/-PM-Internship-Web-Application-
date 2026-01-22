import sqlite3

def get_connection():
    conn = sqlite3.connect('data/internship.db')
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        district TEXT,
        rural TEXT,
        social_category TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skills TEXT,
        sector TEXT,
        company TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
