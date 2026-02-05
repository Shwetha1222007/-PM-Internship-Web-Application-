"""
Fix Admin Password - Reset to 'admin123'
"""
from database import get_connection
import bcrypt

conn = get_connection()
cursor = conn.cursor()

print("\n" + "="*80)
print("FIXING ADMIN PASSWORD")
print("="*80)

# Hash the password 'admin123'
password = "admin123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Update admin password
cursor.execute("""
    UPDATE users 
    SET password = ? 
    WHERE email = 'admin@internship.gov.in'
""", (hashed,))

conn.commit()

print(f"\n✅ Admin password updated!")
print(f"Email: admin@internship.gov.in")
print(f"Password: admin123")
print(f"New hash: {hashed[:30]}...")

# Verify it works
print("\n" + "-"*80)
print("VERIFYING LOGIN...")

# Get admin user
admin = cursor.execute("SELECT * FROM users WHERE email = ?", ('admin@internship.gov.in',)).fetchone()

if admin:
    stored_password = admin['password']
    
    # Test the password
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        print("✅ Password verification SUCCESSFUL!")
        print(f"   Admin can now login with: admin@internship.gov.in / admin123")
    else:
        print("❌ Password verification FAILED!")
else:
    print("❌ Admin user not found!")

conn.close()

print("\n" + "="*80)
print("✅ ADMIN PASSWORD FIX COMPLETE!")
print("="*80)
