import sqlite3
import bcrypt

conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

emails = ["shwethasrinivasan368@gmail.com", "shwetha12206@gmail.com"]

for email in emails:
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()

    if user:
        pwd = user['password']
        print(f"User: {email}")
        
        test_pw = "shwetha123"
        result = bcrypt.checkpw(test_pw.encode('utf-8'), pwd.encode('utf-8'))
        print(f"Match 'shwetha123': {result}")
    else:
        print(f"User {email} not found")

conn.close()
