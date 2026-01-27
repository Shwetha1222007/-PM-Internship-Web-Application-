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
    print(f"Found user: {user['name']} ({user['email']})")
    print(f"Current password hash: {user['password'][:30]}...")
    
    # Ask for new password
    new_password = input("\nEnter new password for this user: ")
    
    # Hash the new password
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Update the password
    cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user['id']))
    conn.commit()
    
    print(f"\n✅ Password updated successfully!")
    print(f"New password hash: {hashed[:30]}...")
    print(f"\nYou can now login with:")
    print(f"  Email: {email}")
    print(f"  Password: {new_password}")
else:
    print(f"❌ No user found with email: {email}")

conn.close()
