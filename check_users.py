"""
Check database users and their passwords
"""
from database import get_connection

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
    print(f"Password (first 20 chars): {user['password'][:20]}...")
    print(f"Password length: {len(user['password'])}")
    print("-"*80)

conn.close()

print("\n✅ Check complete!")
