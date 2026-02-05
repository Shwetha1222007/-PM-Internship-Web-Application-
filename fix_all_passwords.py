"""
Fix All User Passwords
Reset admin and all HR accounts to their default passwords
"""
from database import get_connection
import bcrypt

conn = get_connection()
cursor = conn.cursor()

print("\n" + "="*80)
print("FIXING ALL USER PASSWORDS")
print("="*80)

# Fix Admin Password
print("\n1. Fixing Admin Password...")
admin_password = "admin123"
admin_hashed = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cursor.execute("""
    UPDATE users 
    SET password = ? 
    WHERE email = 'admin@internship.gov.in'
""", (admin_hashed,))

print(f"   ✅ Admin: admin@internship.gov.in / admin123")

# Fix HR Passwords
print("\n2. Fixing HR Passwords...")
hr_password = "1234"
hr_hashed = bcrypt.hashpw(hr_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Get all HR users
hr_users = cursor.execute("SELECT email FROM users WHERE role = 'hr'").fetchall()

for hr in hr_users:
    cursor.execute("""
        UPDATE users 
        SET password = ? 
        WHERE email = ?
    """, (hr_hashed, hr['email']))
    print(f"   ✅ HR: {hr['email']} / 1234")

conn.commit()

print("\n" + "="*80)
print("VERIFICATION TEST")
print("="*80)

# Test Admin Login
print("\n1. Testing Admin Login...")
admin = cursor.execute("SELECT * FROM users WHERE email = ?", ('admin@internship.gov.in',)).fetchone()
if admin and bcrypt.checkpw(admin_password.encode('utf-8'), admin['password'].encode('utf-8')):
    print("   ✅ Admin login works!")
else:
    print("   ❌ Admin login failed!")

# Test HR Login
print("\n2. Testing HR Login...")
hr_test = cursor.execute("SELECT * FROM users WHERE role = 'hr' LIMIT 1").fetchone()
if hr_test and bcrypt.checkpw(hr_password.encode('utf-8'), hr_test['password'].encode('utf-8')):
    print(f"   ✅ HR login works! (tested with {hr_test['email']})")
else:
    print("   ❌ HR login failed!")

conn.close()

print("\n" + "="*80)
print("✅ ALL PASSWORDS FIXED!")
print("="*80)
print("\nLogin Credentials:")
print("-" * 80)
print("Admin:")
print("  Email: admin@internship.gov.in")
print("  Password: admin123")
print("\nHR Accounts:")
print("  Email: 1208_<company>_HR (e.g., 1208_zoho_HR)")
print("  Password: 1234")
print("="*80)
