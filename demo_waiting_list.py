"""
Demo script to test the Waiting List and Location-Based Alternatives System
This creates sample applications and demonstrates the selection process
"""
import sys
from database import get_connection
from waiting_list_manager import (
    select_candidates_and_create_waiting_list,
    get_waiting_list_for_user,
    find_alternative_locations
)


def create_sample_applications():
    """Create sample applications for testing"""
    conn = get_connection()
    cur = conn.cursor()
    
    # First, create sample users
    sample_users = [
        ("Alice Kumar", "alice@example.com", "9876543210", "Rural", "SC", 8.5, 85.0),
        ("Bob Sharma", "bob@example.com", "9876543211", "Urban", "General", 9.0, 90.0),
        ("Charlie Patel", "charlie@example.com", "9876543212", "Rural", "OBC", 7.8, 78.0),
        ("Diana Singh", "diana@example.com", "9876543213", "Urban", "ST", 8.2, 82.0),
        ("Eve Reddy", "eve@example.com", "9876543214", "Rural", "General", 8.8, 88.0),
    ]
    
    print("\n" + "="*60)
    print("CREATING SAMPLE USERS AND APPLICATIONS")
    print("="*60)
    
    user_ids = []
    for name, email, phone, rural, category, cgpa, perc_12th in sample_users:
        # Check if user exists
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing = cur.fetchone()
        
        if existing:
            user_id = existing['id']
            print(f"✓ User already exists: {name} (ID: {user_id})")
        else:
            # Create user with bcrypt password
            import bcrypt
            hashed_pw = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode('utf-8')
            
            cur.execute("""
                INSERT INTO users (name, email, phone, password, rural, social_category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, phone, hashed_pw, rural, category))
            user_id = cur.lastrowid
            print(f"✓ Created user: {name} (ID: {user_id})")
        
        user_ids.append(user_id)
        
        # Create application for TCS Bangalore
        cur.execute("""
            SELECT id FROM applications 
            WHERE user_id = ? AND company = 'TCS' AND location_pref = 'Bangalore'
        """, (user_id,))
        
        existing_app = cur.fetchone()
        
        if not existing_app:
            cur.execute("""
                INSERT INTO applications 
                (user_id, skills, sector, company, location_pref, languages, perc_12th, 
                 college_name, cgpa, experience, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Applied')
            """, (
                user_id,
                "Python, JavaScript, React, Node.js",
                "IT",
                "TCS",
                "Bangalore",
                "English, Hindi",
                perc_12th,
                "ABC Engineering College",
                cgpa,
                "6 months internship at XYZ Corp"
            ))
            print(f"  → Application created for {name} to TCS Bangalore")
        else:
            print(f"  → Application already exists for {name}")
    
    conn.commit()
    conn.close()
    
    print("="*60)
    return user_ids


def demo_selection_process():
    """Demonstrate the selection and waiting list process"""
    print("\n" + "="*60)
    print("RUNNING SELECTION PROCESS FOR TCS BANGALORE")
    print("="*60)
    
    # Define requirements
    requirements = {
        'skills': 'Python, JavaScript, React',
        'min_cgpa': 7.0
    }
    
    print(f"\nRequirements:")
    print(f"  Skills: {requirements['skills']}")
    print(f"  Min CGPA: {requirements['min_cgpa']}")
    
    # Check available seats
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT available_seats, allocated_seats 
        FROM company_locations 
        WHERE company_name = 'TCS' AND location = 'Bangalore'
    """)
    location_data = cur.fetchone()
    
    if location_data:
        available = location_data['available_seats']
        allocated = location_data['allocated_seats']
        remaining = available - allocated
        print(f"\nSeat Availability:")
        print(f"  Total Seats: {available}")
        print(f"  Allocated: {allocated}")
        print(f"  Remaining: {remaining}")
    
    # Find alternative locations
    alternatives = find_alternative_locations('TCS', 'Bangalore', cur)
    print(f"\nAlternative TCS Locations:")
    for alt in alternatives:
        print(f"  • {alt['location']}: {alt['available_seats']} seats available")
    
    conn.close()
    
    # Run selection process
    print("\n" + "-"*60)
    print("PROCESSING APPLICATIONS...")
    print("-"*60)
    
    result = select_candidates_and_create_waiting_list(
        company='TCS',
        location='Bangalore',
        requirements=requirements
    )
    
    print(f"\n✅ Selection Complete!")
    print(f"  Selected Candidates: {result['selected_count']}")
    print(f"  Waiting List: {result['waiting_list_count']}")
    
    # Display selected candidates
    if result['selected']:
        print(f"\n🎉 SELECTED CANDIDATES:")
        for idx, candidate_obj in enumerate(result['selected']):
            candidate = candidate_obj['data']
            score = candidate_obj['score']
            print(f"  {idx + 1}. {candidate['name']} - Score: {score:.2f}")
    
    # Display waiting list
    if result['waiting_list']:
        print(f"\n📋 WAITING LIST:")
        for idx, candidate_obj in enumerate(result['waiting_list']):
            candidate = candidate_obj['data']
            score = candidate_obj['score']
            print(f"  {idx + 1}. {candidate['name']} - Score: {score:.2f}")
    
    print("="*60)
    
    return result


def demo_waiting_list_view(user_ids):
    """Demonstrate waiting list view for a candidate"""
    if not user_ids:
        return
    
    print("\n" + "="*60)
    print("CANDIDATE WAITING LIST VIEW")
    print("="*60)
    
    # Check waiting list for each user
    for user_id in user_ids:
        waiting_entries = get_waiting_list_for_user(user_id)
        
        if waiting_entries:
            for entry_data in waiting_entries:
                entry = entry_data['waiting_list_entry']
                alternatives = entry_data['alternatives']
                
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT name FROM users WHERE id = ?", (user_id,))
                user = cur.fetchone()
                conn.close()
                
                print(f"\n👤 Candidate: {user['name']}")
                print(f"   Company: {entry['company']}")
                print(f"   Preferred Location: {entry['preferred_location']}")
                print(f"   Waiting List Position: #{entry['rank_position']}")
                print(f"   AI Score: {entry['ai_score']:.2f}")
                print(f"   Status: {entry['status']}")
                
                if alternatives:
                    print(f"\n   🌍 Alternative Locations Available:")
                    for alt in alternatives:
                        print(f"      • {alt['alternative_location']} (Offer ID: {alt['id']})")
                else:
                    print(f"\n   ℹ️  No alternative locations currently available")
    
    print("\n" + "="*60)


def main():
    """Main demo function"""
    print("\n" + "="*70)
    print(" "*10 + "WAITING LIST & LOCATION ALTERNATIVES DEMO")
    print("="*70)
    
    # Step 1: Create sample data
    user_ids = create_sample_applications()
    
    # Step 2: Run selection process
    result = demo_selection_process()
    
    # Step 3: Show waiting list view
    demo_waiting_list_view(user_ids)
    
    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)
    print("\nNext Steps:")
    print("1. Check the database to see waiting_list and alternative_offers tables")
    print("2. Check email logs to see notifications sent to candidates")
    print("3. Run the Streamlit app to see the dashboard updates")
    print("4. Test accepting/rejecting alternative locations from the UI")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
