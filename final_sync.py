import sqlite3
import bcrypt

conn = sqlite3.connect('data/internship.db')
cur = conn.cursor()

# Delete empty or null emails
cur.execute("DELETE FROM users WHERE email IS NULL OR email = ''")

# Set password to 'shwetha' for the main users
# Using plain text in DB so the new auth.py can auto-upgrade it ( safer test)
password = "shwetha"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

emails = ["shwetha12206@gmail.com", "shwethasrinivasan368@gmail.com"]

for email in emails:
    # Set to hash
    cur.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
    print(f"Verified {email} updated to password 'shwetha'")

# Also fix the admin just in case
admin_hashed = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
cur.execute("UPDATE users SET password = ? WHERE email = ?", (admin_hashed, "admin@internship.gov.in"))

conn.commit()
conn.close()
