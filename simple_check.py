import sqlite3
import os

# Connect to database
db_path = 'data/internship.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all users
users = cursor.execute("SELECT id, name, email, role, password FROM users").fetchall()

print(f"Total users: {len(users)}\n")

for user in users:
    print(f"ID: {user[0]}")
    print(f"Name: {user[1]}")
    print(f"Email: {user[2]}")
    print(f"Role: {user[3]}")
    print(f"Password starts with: {user[4][:20]}...")
    print(f"Password length: {len(user[4])}")
    print("-" * 50)

conn.close()
