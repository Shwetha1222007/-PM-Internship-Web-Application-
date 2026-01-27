import sqlite3
conn = sqlite3.connect('data/internship.db')
cur = conn.cursor()
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
schema = cur.fetchone()[0]
with open('schema_full.txt', 'w') as f:
    f.write(schema)
print("Schema written to schema_full.txt")
conn.close()
