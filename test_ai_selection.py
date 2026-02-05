"""
Test Script for AI-Driven Automatic Selection System
Run this to test the AI processing with current database
"""

from ai_auto_selector import process_all_companies
from database import get_connection
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def show_current_status():
    """Display current application status before and after AI processing"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("CURRENT APPLICATION STATUS")
    print("="*80)
    
    # Get status breakdown
    status_counts = cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM applications
        GROUP BY status
    """).fetchall()
    
    print("\nStatus Breakdown:")
    for row in status_counts:
        print(f"  {row[0]}: {row[1]} applications")
    
    # Get company breakdown
    company_counts = cursor.execute("""
        SELECT company, 
               COUNT(*) as total,
               SUM(CASE WHEN status = 'Applied' THEN 1 ELSE 0 END) as applied,
               SUM(CASE WHEN status = 'Selected' THEN 1 ELSE 0 END) as selected,
               SUM(CASE WHEN status = 'Shortlisted' THEN 1 ELSE 0 END) as shortlisted,
               SUM(CASE WHEN status = 'Waiting List' THEN 1 ELSE 0 END) as waiting
        FROM applications
        WHERE company IS NOT NULL
        GROUP BY company
    """).fetchall()
    
    print("\nCompany Breakdown:")
    for row in company_counts:
        print(f"\n  {row[0]}:")
        print(f"    Total: {row[1]} | Applied: {row[2]} | Selected: {row[3]} | Shortlisted: {row[4]} | Waiting: {row[5]}")
    
    conn.close()
    print("="*80 + "\n")

def main():
    """Main test function"""
    print("\n🤖 AI-DRIVEN AUTOMATIC SELECTION SYSTEM - TEST SCRIPT")
    print("="*80)
    
    # Show current status
    show_current_status()
    
    # Ask for confirmation
    response = input("\n🚀 Do you want to run AI processing now? (yes/no): ")
    
    if response.lower() == 'yes':
        print("\n🤖 Starting AI processing...")
        print("="*80)
        
        try:
            process_all_companies()
            print("\n✅ AI processing completed successfully!")
            
            # Show updated status
            print("\n📊 Updated Status:")
            show_current_status()
            
            print("\n✨ Summary:")
            print("  - All 'Applied' candidates have been ranked by AI")
            print("  - 1st ranked candidates assigned 'Selected' status with 48-hour deadline")
            print("  - 2nd ranked candidates assigned 'Shortlisted' status")
            print("  - 3rd+ ranked candidates assigned 'Waiting List' status")
            print("  - Notifications sent in order: 3rd → 2nd → 1st")
            print("  - HR notified of completion")
            
        except Exception as e:
            logger.error(f"Error during AI processing: {str(e)}")
            print(f"\n❌ Error: {str(e)}")
    else:
        print("\n❌ AI processing cancelled")

if __name__ == "__main__":
    main()
