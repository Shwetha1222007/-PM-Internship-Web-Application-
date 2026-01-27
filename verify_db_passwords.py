import sqlite3
import bcrypt

conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT id, name, email, password FROM users")
users = cur.fetchall()

print("DATABASE USER CHECK:")
print("-" * 50)
for u in users:
    email = u['email']
    pwd = u['password']
    print(f"ID: {u['id']} | Email: '{email}' | Pwd[:10]: {pwd[:10]}... | Len: {len(pwd)}")
    
    # Test if 'shwetha123' works for this user
    test_pw = "shwetha123"
    try:
        if pwd.startswith("$2b$"):
            match = bcrypt.checkpw(test_pw.encode('utf-8'), pwd.encode('utf-8'))
        else:
            match = (pwd == test_pw)
        print(f"  -> Matches 'shwetha123'? {match}")
    except Exception as e:
        print(f"  -> Error checking: {e}")

conn.close()
