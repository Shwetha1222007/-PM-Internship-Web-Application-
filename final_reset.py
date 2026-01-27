import sqlite3
import bcrypt

def final_reset():
    conn = sqlite3.connect('data/internship.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Emails to reset
    targets = [
        "shwetha12206@gmail.com",
        "shwethasrinivasan368@gmail.com",
        "andal3222@gmail.com",
        "24uam151swetha@kgkite.ac.in",
        "admin@internship.gov.in"
    ]
    
    password = "shwetha123"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    print(f"Setting password to '{password}' for all main accounts...")
    
    for email in targets:
        cur.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
        if cur.rowcount > 0:
            print(f"✅ Reset: {email}")
        else:
            print(f"❓ Not found: {email}")
    
    # Also fix the admin account just in case (using 'admin123' as per original)
    admin_email = "admin@internship.gov.in"
    admin_pass = "admin123"
    admin_hashed = bcrypt.hashpw(admin_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cur.execute("UPDATE users SET password = ? WHERE email = ?", (admin_hashed, admin_email))
    print(f"✅ Reset Admin: {admin_email} -> {admin_pass}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    final_reset()
