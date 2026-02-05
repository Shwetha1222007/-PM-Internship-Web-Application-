"""
List all users and reset their passwords to known values
"""
from database import get_connection
import bcrypt

conn = get_connection()
cursor = conn.cursor()

# Get all users
users = cursor.execute("SELECT id, name, email, role FROM users").fetchall()

print("="*70)
print("ALL USERS IN DATABASE")
print("="*70)

for user in users:
    print(f"\nID: {user['id']}")
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Role: {user['role']}")
    
    # Set password based on role
    if user['role'] == 'admin':
        new_password = "admin123"
    else:
        new_password = "password123"
    
    # Hash and update
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user['id']))
    
    print(f"Password reset to: {new_password}")
    print("-"*70)

conn.commit()
conn.close()

print("\n✅ All passwords have been reset!")
print("\nLogin credentials:")
print("  Admin: admin@internship.gov.in / admin123")
print("  Students: <their_email> / password123")
