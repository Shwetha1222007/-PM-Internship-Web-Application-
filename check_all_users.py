import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get all users
cur.execute("SELECT * FROM users")
users = cur.fetchall()

with open('users_report.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("ALL USERS IN DATABASE\n")
    f.write("=" * 80 + "\n")

    for user in users:
        f.write(f"\nID: {user['id']}\n")
        f.write(f"Name: {user['name']}\n")
        f.write(f"Email: {user['email']}\n")
        
        password_hash = user['password']
        is_valid = password_hash.startswith('$2b$') or password_hash.startswith('$2a$')
        
        f.write(f"Password hash (first 30 chars): {password_hash[:30]}...\n")
        f.write(f"Password length: {len(password_hash)}\n")
        f.write(f"Valid bcrypt hash: {is_valid}\n")
        
        if not is_valid:
            f.write("WARNING: This password is CORRUPTED and needs to be fixed!\n")
        
        try:
            role = user['role']
            f.write(f"Role: {role}\n")
        except:
            f.write("Role: N/A\n")
        
        f.write("-" * 80 + "\n")

    # Check for the specific email
    email_to_check = "shwethasrinivasan368@gmail.com"
    cur.execute("SELECT * FROM users WHERE email = ?", (email_to_check,))
    specific_user = cur.fetchone()

    f.write(f"\n{'=' * 80}\n")
    f.write(f"CHECKING FOR: {email_to_check}\n")
    f.write("=" * 80 + "\n")

    if specific_user:
        f.write(f"User found!\n")
        f.write(f"Name: {specific_user['name']}\n")
        password_hash = specific_user['password']
        is_valid = password_hash.startswith('$2b$') or password_hash.startswith('$2a$')
        f.write(f"Password is valid: {is_valid}\n")
        if not is_valid:
            f.write(f"Password is corrupted: {password_hash}\n")
    else:
        f.write(f"No user found with email: {email_to_check}\n")

conn.close()
print("Report written to users_report.txt")
