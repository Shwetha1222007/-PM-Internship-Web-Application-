"""
Debug login issue - check database and test login
"""
from database import get_connection
from auth import login_user
import bcrypt

conn = get_connection()
cursor = conn.cursor()

print("\n" + "="*80)
print("DATABASE USERS CHECK")
print("="*80)

# Check all users
users = cursor.execute("SELECT id, name, email, role, password FROM users").fetchall()

print(f"\nTotal Users: {len(users)}")
print("\n" + "-"*80)

for user in users:
    print(f"\nID: {user['id']}")
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Role: {user['role']}")
    print(f"Password (first 30 chars): {user['password'][:30]}...")
    print(f"Password length: {len(user['password'])}")
    print(f"Is bcrypt hash: {user['password'].startswith('$2b$')}")
    print("-"*80)

conn.close()

# Test login with common credentials
print("\n" + "="*80)
print("TESTING LOGIN")
print("="*80)

test_credentials = [
    ("admin@internship.gov.in", "admin123"),
]

# Add any student emails found
conn = get_connection()
cursor = conn.cursor()
students = cursor.execute("SELECT email FROM users WHERE role = 'student' LIMIT 3").fetchall()
for student in students:
    test_credentials.append((student['email'], "test123"))
    test_credentials.append((student['email'], "password"))
conn.close()

for email, password in test_credentials:
    print(f"\nTesting: {email} / {password}")
    result = login_user(email, password)
    if result:
        print(f"✅ SUCCESS - Logged in as: {result['name']} ({result['role']})")
    else:
        print(f"❌ FAILED - Invalid credentials")

print("\n✅ Debug complete!")
