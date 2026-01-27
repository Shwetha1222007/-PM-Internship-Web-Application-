import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from auth import login_user
import sqlite3

email = "shwethasrinivasan368@gmail.com"
# The password I set in my reset script
password = "Shwetha@2026"

print(f"Testing login_user('{email}', '{password}')")
user = login_user(email, password)

if user:
    print(f"SUCCESS: Found user {user['name']} (ID: {user['id']})")
    print(f"User dict: {dict(user)}")
else:
    print("FAILED: login_user returned None")

# Let's check the DB directly again for this email
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
all_matching = cur.fetchall()
print(f"\nDirect DB check for {email}:")
print(f"Found {len(all_matching)} records.")
for u in all_matching:
    pwd = u['password']
    print(f"ID: {u['id']}, Pwd start: {pwd[:10]}..., Len: {len(pwd)}")

conn.close()
