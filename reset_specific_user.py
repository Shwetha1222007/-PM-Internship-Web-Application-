import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# The email from the login attempt
email = "shwethasrinivasan368@gmail.com"
new_password = "Shwetha@2026"  # A secure temporary password

# Normalize email
email_normalized = email.lower().strip()

# Get all users with this email (there might be duplicates)
cur.execute("SELECT * FROM users WHERE email = ?", (email_normalized,))
users = cur.fetchall()

if users:
    print(f"Found {len(users)} user(s) with email: {email}")
    print("=" * 80)
    
    # Hash the new password
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    for user in users:
        print(f"\nUpdating user ID {user['id']}: {user['name']}")
        cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user['id']))
    
    conn.commit()
    
    print(f"\n{'=' * 80}")
    print(f"✅ Password updated for {len(users)} user(s)!")
    print(f"{'=' * 80}")
    print(f"\nYou can now login with:")
    print(f"  Email: {email}")
    print(f"  Password: {new_password}")
    print(f"\n⚠️ Please change this password after logging in!")
else:
    print(f"❌ No user found with email: {email_normalized}")

conn.close()
