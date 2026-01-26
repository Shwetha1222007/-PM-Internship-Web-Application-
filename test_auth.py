from auth import register_user, login_user
from database import create_tables

create_tables()
data = ("Test User", "test@example.com", "1234567890", "password123", "1995-01-01", "Test District", "Urban", "General", "1234-1234-1234", "Test Address", "O+", "12345678901")
res = register_user(data)
print(f"Registration: {res}")

user = login_user("test@example.com", "password123")
print(f"Login: {user}")
if user:
    print(f"User ID: {user['id']}")
else:
    print("Login Failed")
