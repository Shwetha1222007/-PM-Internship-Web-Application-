import sqlite3
import bcrypt

conn = sqlite3.connect('data/internship.db')
cur = conn.cursor()

email = "shwetha12206@gmail.com"
password = "12345"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cur.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
conn.commit()
print(f"Password for {email} set to '12345'")
conn.close()
