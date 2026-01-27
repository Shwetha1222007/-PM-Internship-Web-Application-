import sqlite3
import bcrypt

def deduplicate():
    conn = sqlite3.connect('data/internship.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Get all distinct emails
    cur.execute("SELECT DISTINCT email FROM users WHERE email != ''")
    emails = [row['email'] for row in cur.fetchall()]
    
    print(f"Found {len(emails)} distinct emails.")
    
    for email in emails:
        cur.execute("SELECT * FROM users WHERE email = ? ORDER BY id DESC", (email,))
        rows = cur.fetchall()
        if len(rows) > 1:
            print(f"Deduplicating {email} ({len(rows)} entries)")
            # Keep the last one (highest ID), delete others
            primary_id = rows[0]['id']
            for row in rows[1:]:
                cur.execute("DELETE FROM users WHERE id = ?", (row['id'],))
                # Also delete related applications if any? 
                # Better and safer: reassign them to the primary ID
                cur.execute("UPDATE applications SET user_id = ? WHERE user_id = ?", (primary_id, row['id']))
    
    conn.commit()
    
    # Now try to enforce UNIQUE if it's missing (SQLite doesn't allow ALTER TABLE ADD UNIQUE)
    # So we have to recreate the table
    print("Recreating users table to enforce UNIQUE constraint...")
    
    # 1. Get current schema
    cur.execute("PRAGMA table_info(users)")
    cols = cur.fetchall()
    col_definitions = []
    col_names = []
    for col in cols:
        name = col[1]
        type_ = col[2]
        notnull = " NOT NULL" if col[3] else ""
        dflt = f" DEFAULT {col[4]}" if col[4] is not None else ""
        pk = " PRIMARY KEY" if col[5] else "" # We handle AUTOINCREMENT differently
        
        # Special handling for id
        if name == 'id':
            col_definitions.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
        elif name == 'email':
            col_definitions.append("email TEXT UNIQUE")
        else:
            col_definitions.append(f"{name} {type_}{notnull}{dflt}")
        
        col_names.append(name)

    # 2. Rename existing table
    cur.execute("ALTER TABLE users RENAME TO users_old")
    
    # 3. Create new table
    schema = f"CREATE TABLE users ({', '.join(col_definitions)})"
    cur.execute(schema)
    
    # 4. Copy data
    names = ", ".join(col_names)
    cur.execute(f"INSERT INTO users ({names}) SELECT {names} FROM users_old")
    
    # 5. Drop old table
    cur.execute("DROP TABLE users_old")
    
    conn.commit()
    conn.close()
    print("Deduplication and schema fix complete.")

if __name__ == "__main__":
    deduplicate()
