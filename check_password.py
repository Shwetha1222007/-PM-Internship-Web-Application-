import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get the user
email = "shwetha12206@gmail.com"
cur.execute("SELECT * FROM users WHERE email = ?", (email,))
user = cur.fetchone()

with open('password_debug.txt', 'w', encoding='utf-8') as f:
    if user:
        f.write("=" * 50 + "\n")
        f.write("USER FOUND\n")
        f.write("=" * 50 + "\n")
        f.write(f"ID: {user['id']}\n")
        f.write(f"Name: {user['name']}\n")
        f.write(f"Email: {user['email']}\n")
        
        password_stored = user['password']
        f.write(f"Stored password: '{password_stored}'\n")
        f.write(f"Password length: {len(password_stored)}\n")
        f.write(f"Is bcrypt hash: {password_stored.startswith('$2b$')}\n")
        f.write(f"Password repr: {repr(password_stored)}\n")
        
        # Test with common passwords
        test_passwords = ["shwetha", "Shwetha", "password", "123456", "shwetha123", "Shwetha123"]
        f.write("\nTesting common passwords:\n")
        for pwd in test_passwords:
            if password_stored == pwd:
                f.write(f"  MATCH: '{pwd}'\n")
            else:
                f.write(f"  No match: '{pwd}'\n")
    else:
        f.write("NO USER FOUND\n")

conn.close()
print("Output written to password_debug.txt")
