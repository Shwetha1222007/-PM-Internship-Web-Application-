"""
Test login with actual credentials
"""
import sys
sys.path.insert(0, '.')

from auth import login_user
import sqlite3

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all users
users = cursor.execute("SELECT id, name, email, role FROM users").fetchall()

print("Available users:")
for user in users:
    print(f"  - {user['email']} ({user['role']})")

conn.close()

print("\n" + "="*60)
print("TESTING LOGIN")
print("="*60)

# Test admin login
print("\n1. Testing admin login:")
print("   Email: admin@internship.gov.in")
print("   Password: admin123")
result = login_user("admin@internship.gov.in", "admin123")
if result:
    print(f"   ✅ SUCCESS - Logged in as: {result['name']}")
else:
    print(f"   ❌ FAILED")

# Test with wrong password
print("\n2. Testing with wrong password:")
print("   Email: admin@internship.gov.in")
print("   Password: wrongpassword")
result = login_user("admin@internship.gov.in", "wrongpassword")
if result:
    print(f"   ✅ SUCCESS - Logged in as: {result['name']}")
else:
    print(f"   ❌ FAILED (Expected)")

print("\n" + "="*60)
