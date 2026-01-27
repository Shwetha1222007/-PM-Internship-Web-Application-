import sqlite3

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get the user
email = "shwetha12206@gmail.com"
cur.execute("SELECT * FROM users WHERE email = ?", (email,))
user = cur.fetchone()

if user:
    print("=" * 50)
    print("USER FOUND")
    print("=" * 50)
    print(f"ID: {user['id']}")
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    
    password_hash = user['password']
    print(f"Password (first 30 chars): {password_hash[:30]}...")
    print(f"Password length: {len(password_hash)}")
    print(f"Is bcrypt hash: {password_hash.startswith('$2b$')}")
    
    try:
        role = user['role']
        print(f"Role: {role}")
    except:
        print("Role: Column doesn't exist")
else:
    print("NO USER FOUND")

conn.close()
