"""
Verify that all data has been cleared from the databases
"""
import sqlite3
import os

def verify_database(db_path):
    """Verify that a database is empty"""
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
        print(f"Database: {db_path}")
        print(f"{'='*60}")
        
        total_records = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"  {table_name}: {count} records")
        
        conn.close()
        
        if total_records == 0:
            print(f"✓ Database is CLEAN (0 records)")
        else:
            print(f"⚠ Database contains {total_records} records")
        
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Error checking database {db_path}: {str(e)}")

def main():
    print("\n" + "="*60)
    print("VERIFYING DATABASE CLEANUP")
    print("="*60)
    
    db_paths = [
        "data/internship.db",
        "data/pm_internship.db"
    ]
    
    for db_path in db_paths:
        verify_database(db_path)
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
