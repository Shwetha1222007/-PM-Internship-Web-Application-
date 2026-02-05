"""
Reset admin password and verify it works
"""
from database import get_connection
import bcrypt

conn = get_connection()
cursor = conn.cursor()

# Reset admin password
new_password = "admin123"
hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Update admin user
cursor.execute("""
    UPDATE users 
    SET password = ? 
    WHERE email = 'admin@internship.gov.in'
""", (hashed,))

rows_affected = cursor.rowcount
conn.commit()

print(f"✅ Admin password reset complete!")
print(f"   Rows affected: {rows_affected}")
print(f"   Email: admin@internship.gov.in")
print(f"   Password: {new_password}")

# Verify the update
admin = cursor.execute("SELECT * FROM users WHERE email = 'admin@internship.gov.in'").fetchone()
if admin:
    print(f"\n✅ Admin user verified:")
    print(f"   Name: {admin['name']}")
    print(f"   Email: {admin['email']}")
    print(f"   Role: {admin['role']}")
    print(f"   Password hash: {admin['password'][:30]}...")
    
    # Test the password
    if bcrypt.checkpw(new_password.encode('utf-8'), admin['password'].encode('utf-8')):
        print(f"\n✅ Password verification successful!")
    else:
        print(f"\n❌ Password verification failed!")
else:
    print(f"\n❌ Admin user not found!")

conn.close()

# Now test login
print("\n" + "="*60)
print("Testing login function...")
print("="*60)

from auth import login_user

result = login_user("admin@internship.gov.in", "admin123")
if result:
    print(f"✅ Login successful!")
    print(f"   Name: {result['name']}")
    print(f"   Role: {result['role']}")
else:
    print(f"❌ Login failed!")
