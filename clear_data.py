import sqlite3
import os
from database import get_connection, seed_admin, seed_hr_users, seed_companies, seed_company_locations

def clear_all_data():
    """Clear all data from the database and reseed default data"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("🗑️  Starting data cleanup...")
    
    # Clear all tables in reverse order of dependencies
    tables_to_clear = [
        'alternative_offers',
        'waiting_list',
        'applications',
        'users',
        'hr_users',
        'company_locations',
        'companies'
    ]
    
    for table in tables_to_clear:
        try:
            cur.execute(f"DELETE FROM {table}")
            print(f"✅ Cleared table: {table}")
        except sqlite3.OperationalError as e:
            print(f"⚠️  Error clearing {table}: {e}")
    
    # Reset auto-increment counters
    cur.execute("DELETE FROM sqlite_sequence")
    print("✅ Reset all auto-increment counters")
    
    # Reseed default data
    print("\n🌱 Reseeding default data...")
    seed_admin(cur)
    seed_hr_users(cur)
    seed_companies(cur)
    seed_company_locations(cur)
    
    conn.commit()
    conn.close()
    
    print("\n✨ Database cleared and reseeded successfully!")
    print("\n📋 Default accounts available:")
    print("   Admin: admin@internship.gov.in / admin123")
    print("   HR Users: 1208_<company>_HR / 1234")
    print("   Companies: Zoho, Infosys, TCS, Wipro, Google, Microsoft, Amazon, Flipkart")

if __name__ == "__main__":
    confirm = input("⚠️  WARNING: This will delete ALL application data. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_all_data()
    else:
        print("❌ Operation cancelled")
