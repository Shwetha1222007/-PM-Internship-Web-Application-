import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get the user
email = "shwetha12206@gmail.com"
cur.execute("SELECT * FROM users WHERE email = ?", (email,))
user = cur.fetchone()

if user:
    print(f"User found: {user['name']}")
    print(f"Email: {user['email']}")
    password_hash = user['password']
    print(f"Password hash: {password_hash}")
    print(f"Password length: {len(password_hash)}")
    print(f"Password starts with $2b$: {password_hash.startswith('$2b$')}")
    
    # Check if role column exists
    try:
        role = user['role']
        print(f"Role: {role}")
    except:
        print("Role: Column doesn't exist")
else:
    print(f"No user found with email: {email}")

# List all users
print("\n=== All Users ===")
cur.execute("SELECT * FROM users")
all_users = cur.fetchall()
for u in all_users:
    try:
        role = u['role']
    except:
        role = 'N/A'
    print(f"ID: {u['id']}, Name: {u['name']}, Email: {u['email']}, Role: {role}")

conn.close()
