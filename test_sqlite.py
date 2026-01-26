import sqlite3
conn = sqlite3.connect(':memory:')
conn.execute("CREATE TABLE users (email TEXT, password TEXT)")
conn.execute("INSERT INTO users VALUES (?, ?)", ("Test@Example.com", "pass"))
res = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", ("test@example.com", "pass")).fetchone()
print(f"Match: {res}")
