from database import get_connection
import bcrypt

def register_user(data):
    """
    data = (name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account)
    """
    # Normalize data
    name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account = data
    email = email.lower().strip()
    password_plain = password.strip()
    
    # Hash Password
    hashed = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'student')
        """, (name, email, phone, hashed, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account))
        conn.commit()
        return True
    except Exception as e:
        print(f"Registration Error: {e}")
        return False
    finally:
        conn.close()

def login_user(email, password):
    email = email.lower().strip()
    password_plain = password.strip()
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Fetch user by email
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    
    verified_user = None
    
    if user:
        stored_password = user['password']
        
        # Check if hashed (starts with $2b$)
        if stored_password.startswith("$2b$"):
            if bcrypt.checkpw(password_plain.encode('utf-8'), stored_password.encode('utf-8')):
                verified_user = user
        else:
            # Legacy plain text check
            if stored_password == password_plain:
                # Upgrade to hash
                new_hash = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, user['id']))
                conn.commit()
                verified_user = user

    conn.close()
    return verified_user
