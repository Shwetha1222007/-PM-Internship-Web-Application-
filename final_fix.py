import sqlite3
import bcrypt

conn = sqlite3.connect('data/internship.db')
cur = conn.cursor()

# Set password for shwetha12206@gmail.com
email = "shwetha12206@gmail.com"
password = "shwetha"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Ensure this user exists
cur.execute("SELECT id FROM users WHERE email = ?", (email,))
exists = cur.fetchone()

if exists:
    cur.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
    print(f"Updated password for {email}")
else:
    # Get details from the other shwetha account if it exists
    cur.execute("SELECT * FROM users WHERE name = 'shwetha' LIMIT 1")
    other = cur.fetchone()
    if other:
        # Clone it with the new email
        cols = [d[0] for d in cur.description]
        data = list(other)
        email_idx = cols.index('email')
        pwd_idx = cols.index('password')
        id_idx = cols.index('id')
        
        data[email_idx] = email
        data[pwd_idx] = hashed
        
        # Build insert
        placeholders = ", ".join(["?"] * (len(cols) - 1))
        col_names = ", ".join([c for c in cols if c != 'id'])
        insert_data = [data[i] for i in range(len(cols)) if i != id_idx]
        
        cur.execute(f"INSERT INTO users ({col_names}) VALUES ({placeholders})", insert_data)
        print(f"Created new user {email} based on existing shwetha user.")
    else:
        # Create from scratch
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", 
                    ("Shwetha", email, hashed, "student"))
        print(f"Created new user {email} from scratch.")

# Also ensure admin is correct
admin_email = "admin@internship.gov.in"
admin_pass = "admin123"
admin_hashed = bcrypt.hashpw(admin_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
cur.execute("UPDATE users SET password = ? WHERE email = ?", (admin_hashed, admin_email))
print("Admin password confirmed.")

conn.commit()
conn.close()
