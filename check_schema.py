import sqlite3

conn = sqlite3.connect('data/internship.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
print("Columns in 'users' table:")
for col in columns:
    print(col)

cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
schema = cursor.fetchone()
print("\nSchema for 'users' table:")
print(schema[0] if schema else "Table not found")

conn.close()
