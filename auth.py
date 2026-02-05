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
    
    print(f"[LOGIN DEBUG] Attempting login for: {email}")
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Fetch user by email
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    
    if not user:
        print(f"[LOGIN DEBUG] User not found: {email}")
        conn.close()
        return None
    
    print(f"[LOGIN DEBUG] User found: {user['name']} (ID: {user['id']}, Role: {user.get('role', 'N/A')})")
    
    verified_user = None
    stored_password = user['password']
    
    print(f"[LOGIN DEBUG] Password hash starts with: {stored_password[:20]}...")
    print(f"[LOGIN DEBUG] Is bcrypt hash: {stored_password.startswith('$2b$')}")
    
    try:
        # Try bcrypt verification first
        if bcrypt.checkpw(password_plain.encode('utf-8'), stored_password.encode('utf-8')):
            print(f"[LOGIN DEBUG] ✅ Bcrypt verification successful")
            verified_user = user
        else:
            print(f"[LOGIN DEBUG] Bcrypt verification failed, trying plain text")
            # Fallback to plain text check (for legacy or specifically set passwords)
            if stored_password == password_plain:
                print(f"[LOGIN DEBUG] ✅ Plain text match successful, upgrading to hash")
                # Upgrade to hash automatically
                new_hash = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, user['id']))
                conn.commit()
                verified_user = user
            else:
                print(f"[LOGIN DEBUG] ❌ Plain text match failed")
    except Exception as e:
        print(f"[LOGIN DEBUG] Exception during bcrypt check: {e}")
        # If bcrypt.checkpw fails (e.g. invalid salt), fallback to plain text check
        if stored_password == password_plain:
            print(f"[LOGIN DEBUG] ✅ Plain text match successful (after exception), upgrading to hash")
            new_hash = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, user['id']))
            conn.commit()
            verified_user = user
        else:
            print(f"[LOGIN DEBUG] ❌ Plain text match failed (after exception)")

    conn.close()
    
    if verified_user:
        print(f"[LOGIN DEBUG] ✅ Login successful for: {email}")
    else:
        print(f"[LOGIN DEBUG] ❌ Login failed for: {email}")
    
    return verified_user
