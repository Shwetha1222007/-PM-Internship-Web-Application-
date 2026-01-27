import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Test login with the email from the screenshot
email = "shwethasrinivasan368@gmail.com"
email_normalized = email.lower().strip()

print(f"Testing login for: {email}")
print(f"Normalized email: {email_normalized}")
print("=" * 80)

# Fetch user by email (exactly as the login function does)
cur.execute("SELECT * FROM users WHERE email = ?", (email_normalized,))
user = cur.fetchone()

if user:
    print(f"\n✅ User found!")
    print(f"ID: {user['id']}")
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Password hash: {user['password'][:40]}...")
    
    try:
        role = user['role']
        print(f"Role: {role}")
    except:
        print(f"Role: N/A")
    
    # Test with some common passwords
    test_passwords = [
        "shwetha",
        "Shwetha",
        "shwetha123",
        "Shwetha123",
        "password",
        "Password123",
        "TempPass123!"
    ]
    
    print(f"\n{'=' * 80}")
    print("Testing common passwords:")
    print("=" * 80)
    
    stored_password = user['password']
    
    for pwd in test_passwords:
        pwd_normalized = pwd.strip()
        
        if stored_password.startswith("$2b$"):
            try:
                if bcrypt.checkpw(pwd_normalized.encode('utf-8'), stored_password.encode('utf-8')):
                    print(f"✅ MATCH FOUND: '{pwd}'")
                    print(f"\nYou can login with:")
                    print(f"  Email: {email}")
                    print(f"  Password: {pwd}")
                    break
                else:
                    print(f"❌ No match: '{pwd}'")
            except Exception as e:
                print(f"❌ Error testing '{pwd}': {e}")
        else:
            if stored_password == pwd_normalized:
                print(f"✅ MATCH FOUND (plain text): '{pwd}'")
                break
            else:
                print(f"❌ No match: '{pwd}'")
else:
    print(f"\n❌ No user found with email: {email_normalized}")
    
    # Check if there are similar emails
    print(f"\nSearching for similar emails...")
    cur.execute("SELECT id, name, email FROM users WHERE email LIKE ?", (f"%{email.split('@')[0]}%",))
    similar = cur.fetchall()
    
    if similar:
        print(f"Found {len(similar)} similar email(s):")
        for s in similar:
            print(f"  - ID {s['id']}: {s['name']} ({s['email']})")

conn.close()
