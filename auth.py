from database import get_connection

def register_user(data):
    """
    data = (name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account)
    """
    # Normalize data
    name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account = data
    email = email.lower().strip()
    password = password.strip()
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, password, dob, district, rural, social_category, aadhaar, address, blood_group, bank_account))
        conn.commit()
        return True
    except Exception as e:
        print(f"Registration Error: {e}")
        return False
    finally:
        conn.close()

def login_user(email, password):
    email = email.lower().strip()
    password = password.strip()
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cur.fetchone()
    conn.close()
    return user
