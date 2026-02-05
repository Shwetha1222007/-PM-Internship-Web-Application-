"""
Show all users in the database with their login credentials
"""
from database import get_connection

conn = get_connection()
cursor = conn.cursor()

users = cursor.execute("SELECT id, name, email, role FROM users ORDER BY role, id").fetchall()

print("\n" + "="*80)
print("ALL USERS IN DATABASE")
print("="*80)

admin_users = []
student_users = []

for user in users:
    if user['role'] == 'admin':
        admin_users.append(user)
    else:
        student_users.append(user)

if admin_users:
    print("\n📋 ADMIN USERS:")
    print("-"*80)
    for user in admin_users:
        print(f"  Name: {user['name']}")
        print(f"  Email: {user['email']}")
        print(f"  Password: admin123")
        print("-"*80)

if student_users:
    print("\n👨‍🎓 STUDENT USERS:")
    print("-"*80)
    for user in student_users:
        print(f"  Name: {user['name']}")
        print(f"  Email: {user['email']}")
        print(f"  Password: password123")
        print("-"*80)

print(f"\nTotal Users: {len(users)}")
print(f"  - Admins: {len(admin_users)}")
print(f"  - Students: {len(student_users)}")

# Also show HR users
hr_users = cursor.execute("SELECT username, company, email FROM hr_users ORDER BY company").fetchall()

if hr_users:
    print("\n👔 HR USERS:")
    print("-"*80)
    for hr in hr_users:
        print(f"  Company: {hr['company']}")
        print(f"  Username: {hr['username']}")
        print(f"  Email: {hr['email']}")
        print(f"  Password: 1234")
        print("-"*80)
    print(f"\nTotal HR Users: {len(hr_users)}")

conn.close()

print("\n✅ Use these credentials to login to the application!")
print("   URL: http://localhost:8501")
