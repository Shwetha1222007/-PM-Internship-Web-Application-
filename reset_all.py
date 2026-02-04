import sqlite3
import os
import bcrypt

def reset_database():
    db_path = 'data/internship.db'
    if not os.path.exists(db_path):
        print("Database file not found. Nothing to reset.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        print("Cleaning up database tables...")
        # Clear applications first due to foreign key constraints
        cur.execute("DELETE FROM applications")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='applications'")
        
        # Clear users
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='users'")
        
        print("Re-seeding Admin account...")
        admin_email = "admin@internship.gov.in"
        admin_pass = "admin123"
        hashed_password = bcrypt.hashpw(admin_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cur.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, ("Administrator", admin_email, hashed_password, "admin"))
        
        conn.commit()
        print(f"✅ Database reset complete!")
        print(f"✅ All user data removed.")
        print(f"✅ Admin account recreated: {admin_email} / {admin_pass}")
        
    except Exception as e:
        print(f"❌ Error during reset: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    reset_database()
