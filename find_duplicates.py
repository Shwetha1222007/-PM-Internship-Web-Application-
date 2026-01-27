import sqlite3

# Connect to database
conn = sqlite3.connect('data/internship.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Find all duplicate emails
cur.execute("""
    SELECT email, COUNT(*) as count 
    FROM users 
    WHERE email != '' 
    GROUP BY email 
    HAVING COUNT(*) > 1
    ORDER BY count DESC
""")

duplicates = cur.fetchall()

print("=" * 80)
print("DUPLICATE EMAILS IN DATABASE")
print("=" * 80)

if duplicates:
    print(f"\nFound {len(duplicates)} email(s) with duplicates:\n")
    
    for dup in duplicates:
        email = dup['email']
        count = dup['count']
        
        print(f"\nEmail: {email} ({count} entries)")
        print("-" * 80)
        
        # Get all users with this email
        cur.execute("SELECT * FROM users WHERE email = ? ORDER BY id", (email,))
        users = cur.fetchall()
        
        for i, user in enumerate(users):
            print(f"  [{i+1}] ID: {user['id']}, Name: {user['name']}, Created: {user.get('created_at', 'N/A')}")
        
        # Keep the first one, mark others for deletion
        if len(users) > 1:
            keep_id = users[0]['id']
            delete_ids = [u['id'] for u in users[1:]]
            
            print(f"\n  ✅ Will keep: ID {keep_id}")
            print(f"  ❌ Will delete: IDs {delete_ids}")
else:
    print("\n✅ No duplicate emails found!")

conn.close()

print(f"\n{'=' * 80}")
print("NOTE: This script only SHOWS duplicates. Run cleanup script to remove them.")
print("=" * 80)
