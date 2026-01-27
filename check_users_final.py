import sqlite3
import bcrypt

conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM users")
rows = cur.fetchall()

print(f"Total users: {len(rows)}")
for row in rows:
    print(f"ID: {row['id']}, Email: {row['email']}, Name: {row['name']}")
    pwd = row['password']
    print(f"  Password starts with: {pwd[:10]}... (Len: {len(pwd)})")
    
    # Try common passwords
    for test in ["shwetha", "12345", "admin123", "shwetha123"]:
        try:
            if pwd.startswith("$2b$"):
                match = bcrypt.checkpw(test.encode('utf-8'), pwd.encode('utf-8'))
            else:
                match = (pwd == test)
            if match:
                print(f"  ✅ Password MATCH: '{test}'")
        except:
            pass
print("-" * 30)
conn.close()
