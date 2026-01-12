import sqlite3

def get_connection():
    return sqlite3.connect("data/pm_internship.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Users table (UPDATED)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        district TEXT,
        password TEXT
    )
    """)

    # Applications table (no change)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        user_id INTEGER,
        skills TEXT,
        sector TEXT,
        company TEXT,
        experience TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
