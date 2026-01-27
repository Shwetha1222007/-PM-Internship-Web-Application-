import sqlite3
conn = sqlite3.connect('data/internship.db')
cur = conn.cursor()
cur.execute("SELECT password FROM users WHERE email='shwetha12206@gmail.com'")
pwd = cur.fetchone()[0]
print(f"Prefix: {pwd[:5]}")
conn.close()
