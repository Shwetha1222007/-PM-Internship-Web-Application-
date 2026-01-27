import sqlite3
import bcrypt

conn = sqlite3.connect('data/internship.db')
cur = conn.cursor()

# Set password to 'shwetha' for these users
password = "shwetha"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

emails = ["shwetha12206@gmail.com", "shwethasrinivasan368@gmail.com"]

for email in emails:
    cur.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
    print(f"Updated {email} to password 'shwetha'")

conn.commit()
conn.close()
