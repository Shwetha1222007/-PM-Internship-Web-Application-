import sqlite3
import bcrypt
import os

def fix_users():
    db_path = 'data/internship.db'
    if not os.path.exists(db_path):
        print("DB not found")
        return
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    password = "1234"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    users = [
        ('shwetha srinivasan', '24uam151swetha@kgkite.ac.in'),
        ('Shwetha', 'shwetha12206@gmail.com')
    ]
    
    for name, email in users:
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            cur.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
            print(f"Updated password for {email} to '1234'")
        else:
            cur.execute("""
                INSERT INTO users (name, email, password, role) 
                VALUES (?, ?, ?, 'student')
            """, (name, email, hashed))
            print(f"Created user {email} with password '1234'")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_users()
