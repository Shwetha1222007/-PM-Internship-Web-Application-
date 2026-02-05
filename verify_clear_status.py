import sqlite3
import os

def check_db(db_path):
    print(f"\n--- Checking {db_path} ---")
    if not os.path.exists(db_path):
        print(f"File not found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables found: {tables}")
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} records")
    conn.close()

if __name__ == "__main__":
    check_db("data/internship.db")
    check_db("data/pm_internship.db")
