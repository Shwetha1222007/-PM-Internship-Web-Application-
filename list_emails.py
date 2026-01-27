import sqlite3
conn=sqlite3.connect('data/internship.db')
cur=conn.cursor()
cur.execute('SELECT email FROM users')
for r in cur.fetchall():
    print(f"'{r[0]}'")
conn.close()
