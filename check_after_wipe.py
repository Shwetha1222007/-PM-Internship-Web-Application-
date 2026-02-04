import sqlite3
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
email = "shwetha12206@gmail.com"
cur.execute("SELECT * FROM users WHERE email = ?", (email,))
user = cur.fetchone()
if user:
    print(f"User FOUND: {user['email']}")
    print(f"Password starts with: {user['password'][:10]}")
else:
    print(f"User NOT FOUND: {email}")
conn.close()
