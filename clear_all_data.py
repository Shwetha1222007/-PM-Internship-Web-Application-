"""
Script to clear all data from the internship management databases
This will remove all users, applications, and related data while preserving the schema
"""
import sqlite3
import os

def clear_database(db_path):
    """Clear all data from a database while preserving the schema"""
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        print(f"\n{'='*60}")
        print(f"Clearing database: {db_path}")
        print(f"{'='*60}")
        
        # Delete all data from each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            if count > 0:
                cursor.execute(f"DELETE FROM {table_name}")
                print(f"✓ Cleared {count} records from table: {table_name}")
            else:
                print(f"○ Table already empty: {table_name}")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence")
        print(f"✓ Reset auto-increment counters")
        
        conn.commit()
        conn.close()
        
        print(f"{'='*60}")
        print(f"✓ Database cleared successfully: {db_path}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"✗ Error clearing database {db_path}: {str(e)}")

def main():
    """Main function to clear all databases"""
    print("\n" + "="*60)
    print("CLEARING ALL DATA FROM INTERNSHIP MANAGEMENT SYSTEM")
    print("="*60)
    
    # Define database paths
    db_paths = [
        "data/internship.db",
        "data/pm_internship.db"
    ]
    
    # Clear each database
    for db_path in db_paths:
        clear_database(db_path)
    
    print("\n" + "="*60)
    print("ALL DATA CLEARED SUCCESSFULLY!")
    print("="*60)
    print("\nThe application is now reset to a clean state.")
    print("All users, applications, and related data have been removed.")
    print("The database schema has been preserved.")
    print("\nYou can now restart the application with a fresh slate.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
