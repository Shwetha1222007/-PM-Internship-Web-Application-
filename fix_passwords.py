import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get all users with potentially corrupted passwords
cur.execute("SELECT * FROM users")
users = cur.fetchall()

print("Checking all users for password issues...")
print("=" * 60)

fixed_count = 0
for user in users:
    password_hash = user['password']
    
    # Check if password is NOT a valid bcrypt hash
    if not password_hash.startswith('$2b$') and not password_hash.startswith('$2a$'):
        print(f"\n❌ Found corrupted password for user: {user['name']} ({user['email']})")
        print(f"   Current password: {password_hash[:30]}...")
        print(f"   This password cannot be used for login.")
        print(f"   User needs to reset their password.")
        
        # For now, let's set a temporary password
        temp_password = "TempPass123!"
        hashed = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user['id']))
        fixed_count += 1
        
        print(f"   ✅ Password reset to temporary: {temp_password}")
        print(f"   User can now login with this temporary password.")
    else:
        print(f"✅ User {user['name']} ({user['email']}) has valid password hash")

if fixed_count > 0:
    conn.commit()
    print(f"\n{'=' * 60}")
    print(f"✅ Fixed {fixed_count} user(s) with corrupted passwords")
    print(f"   Temporary password for all fixed users: TempPass123!")
else:
    print(f"\n{'=' * 60}")
    print("✅ All users have valid password hashes")

conn.close()
