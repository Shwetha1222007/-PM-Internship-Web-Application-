"""
Verify database and test login after fresh creation
"""
from database import get_connection
from auth import login_user

print("\n" + "="*70)
print("VERIFYING FRESH DATABASE")
print("="*70)

conn = get_connection()
cursor = conn.cursor()

# Check admin user
admin = cursor.execute("SELECT * FROM users WHERE role = 'admin'").fetchone()

if admin:
    print(f"\n✅ Admin user found:")
    print(f"   ID: {admin['id']}")
    print(f"   Name: {admin['name']}")
    print(f"   Email: {admin['email']}")
    print(f"   Role: {admin['role']}")
    print(f"   Password hash: {admin['password'][:30]}...")
    print(f"   Is bcrypt: {admin['password'].startswith('$2b$')}")
else:
    print(f"\n❌ Admin user not found!")

# Check all users
all_users = cursor.execute("SELECT id, name, email, role FROM users").fetchall()
print(f"\n📊 Total users in database: {len(all_users)}")

conn.close()

# Test login
print("\n" + "="*70)
print("TESTING LOGIN")
print("="*70)

print("\nAttempting login with: admin@internship.gov.in / admin123")
result = login_user("admin@internship.gov.in", "admin123")

if result:
    print(f"\n✅ LOGIN SUCCESSFUL!")
    print(f"   Name: {result['name']}")
    print(f"   Email: {result['email']}")
    print(f"   Role: {result['role']}")
else:
    print(f"\n❌ LOGIN FAILED!")

print("\n" + "="*70)
