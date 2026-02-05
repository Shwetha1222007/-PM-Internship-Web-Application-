from database import get_connection

def verify_data_cleared():
    """Verify that data has been cleared"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("📊 Database Status Check:")
    print("-" * 50)
    
    # Check each table
    tables = {
        'users': 'Users (excluding admin)',
        'applications': 'Applications',
        'hr_users': 'HR Users',
        'companies': 'Companies',
        'company_locations': 'Company Locations',
        'waiting_list': 'Waiting List',
        'alternative_offers': 'Alternative Offers'
    }
    
    for table, label in tables.items():
        try:
            if table == 'users':
                # Count non-admin users
                cur.execute(f"SELECT COUNT(*) FROM {table} WHERE role != 'admin' OR role IS NULL")
            else:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"{label}: {count} records")
        except Exception as e:
            print(f"{label}: Error - {e}")
    
    print("-" * 50)
    
    # Check admin exists
    cur.execute("SELECT email FROM users WHERE role = 'admin'")
    admin = cur.fetchone()
    if admin:
        print(f"✅ Admin account exists: {admin[0]}")
    else:
        print("❌ Admin account missing!")
    
    conn.close()

if __name__ == "__main__":
    verify_data_cleared()
