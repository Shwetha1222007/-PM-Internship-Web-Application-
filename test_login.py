import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Test login
email = "shwetha12206@gmail.com"
test_password = "TempPass123!"

cur.execute("SELECT * FROM users WHERE email = ?", (email,))
user = cur.fetchone()

if user:
    stored_password = user['password']
    
    print(f"Testing login for: {user['name']} ({user['email']})")
    print(f"Password hash: {stored_password[:30]}...")
    print(f"Test password: {test_password}")
    
    if stored_password.startswith("$2b$"):
        if bcrypt.checkpw(test_password.encode('utf-8'), stored_password.encode('utf-8')):
            print("\n✅ LOGIN SUCCESSFUL!")
            print(f"You can now login with:")
            print(f"  Email: {email}")
            print(f"  Password: {test_password}")
        else:
            print("\n❌ LOGIN FAILED - Password does not match")
    else:
        print("\n❌ Password is not properly hashed")
else:
    print(f"❌ No user found with email: {email}")

conn.close()
