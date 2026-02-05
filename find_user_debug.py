import sqlite3
import os

def find_user(email):
    db_path = 'data/internship.db'
    if not os.path.exists(db_path):
        print(f"File not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print(f"Searching for: {email}")
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
    user = cursor.fetchone()
    
    if user:
        print("✅ User found!")
        print(f"ID: {user['id']}")
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Role: {user['role']}")
        print(f"Password Hash: '{user['password']}'")
        print(f"Hash Length: {len(user['password'])}")
        print(f"Starts with $2b$: {user['password'].startswith('$2b$')}")
    else:
        print("❌ User NOT found in database.")
        
    conn.close()

if __name__ == "__main__":
    import sys
    email = sys.argv[1] if len(sys.argv) > 1 else "shwetha12206@gmail.com"
    find_user(email)
