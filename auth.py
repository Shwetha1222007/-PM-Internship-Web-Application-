from database import get_connection

def register_user(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name,email,phone,district,rural,social_category,password)
        VALUES (?,?,?,?,?,?,?)
    """, data)
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()
    conn.close()
    return user
