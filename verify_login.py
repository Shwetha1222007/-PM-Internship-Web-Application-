import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Test the login
email = "shwethasrinivasan368@gmail.com"
password = "Shwetha@2026"

email_normalized = email.lower().strip()
password_normalized = password.strip()

# Fetch user
cur.execute("SELECT * FROM users WHERE email = ?", (email_normalized,))
user = cur.fetchone()

if user:
    stored_password = user['password']
    
    print(f"Testing login:")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print("=" * 80)
    
    if stored_password.startswith("$2b$"):
        if bcrypt.checkpw(password_normalized.encode('utf-8'), stored_password.encode('utf-8')):
            print(f"\n✅✅✅ LOGIN SUCCESSFUL! ✅✅✅")
            print(f"\nUser Details:")
            print(f"  ID: {user['id']}")
            print(f"  Name: {user['name']}")
            print(f"  Email: {user['email']}")
            try:
                print(f"  Role: {user['role']}")
            except:
                print(f"  Role: N/A")
        else:
            print(f"\n❌ LOGIN FAILED - Password does not match")
    else:
        print(f"\n❌ Password is not properly hashed")
else:
    print(f"❌ No user found")

conn.close()
