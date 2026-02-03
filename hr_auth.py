import bcrypt
from database import get_connection


def hr_login(username, password):
    """
    Authenticate HR user
    Returns HR user data if successful, None otherwise
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Fetch HR user by username
    cur.execute("SELECT * FROM hr_users WHERE username = ?", (username,))
    hr_user = cur.fetchone()
    conn.close()
    
    if not hr_user:
        return None
    
    # Verify password
    stored_password = hr_user['password']
    
    # Check if password matches (bcrypt)
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        return {
            'id': hr_user['id'],
            'username': hr_user['username'],
            'company': hr_user['company'],
            'email': hr_user['email']
        }
    
    return None


def get_company_info(company_name):
    """Get company information including seat allocation"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM companies WHERE name = ?", (company_name,))
    company = cur.fetchone()
    conn.close()
    
    if company:
        return {
            'name': company['name'],
            'total_seats': company['total_seats'],
            'allocated_seats': company['allocated_seats'],
            'available_seats': company['total_seats'] - company['allocated_seats']
        }
    return None


def update_seat_allocation(company_name, increment=1):
    """Update allocated seats for a company"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE companies 
        SET allocated_seats = allocated_seats + ? 
        WHERE name = ?
    """, (increment, company_name))
    
    conn.commit()
    conn.close()
