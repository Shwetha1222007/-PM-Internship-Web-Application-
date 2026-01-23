from database import get_connection

# -------------------------------
# Register New User
# -------------------------------
def register_user(data):
    """
    data = (name, email, phone, dob, district, rural, social_category, password)
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (name, email, phone, dob, district, rural, social_category, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# -------------------------------
# Login Existing User
# -------------------------------
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM users
        WHERE email = ? AND password = ?
    """, (email, password))

    user = cur.fetchone()
    conn.close()
    return user
