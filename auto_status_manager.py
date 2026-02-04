"""
Automatic Status Manager for PM Internship Scheme
Handles automatic status transitions for candidates who don't respond within 48 hours
"""

import sqlite3
import datetime
from database import get_connection
from email_service import send_update_to_candidate
from hr_auth import update_seat_allocation, get_company_info
from ai_engine import ai_filter_candidates, get_top_candidates
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_status_manager.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def check_and_update_expired_selections():
    """
    Check for selected candidates who haven't responded within 48 hours
    and automatically move them to waiting list, then promote next candidate
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get current time
        now = datetime.datetime.now()
        
        # Find all selected candidates whose deadline has passed (48 hours)
        expired_selections = cursor.execute("""
            SELECT a.*, u.name, u.email, c.total_seats, c.allocated_seats
            FROM applications a
            JOIN users u ON a.user_id = u.id
            LEFT JOIN companies c ON a.company = c.name
            WHERE a.status = 'Selected' 
            AND a.response_deadline IS NOT NULL
            AND datetime(a.response_deadline) < datetime(?)
        """, (now.isoformat(),)).fetchall()
        
        if not expired_selections:
            logger.info("No expired selections found.")
            return
        
        logger.info(f"Found {len(expired_selections)} expired selections to process.")
        
        for expired in expired_selections:
            expired_dict = dict(expired)
            candidate_name = expired_dict['name']
            candidate_email = expired_dict['email']
            company_name = expired_dict['company']
            app_id = expired_dict['id']
            
            logger.info(f"Processing expired selection: {candidate_name} ({candidate_email}) for {company_name}")
            
            # Move candidate to Waiting List
            cursor.execute("""
                UPDATE applications 
                SET status = 'Waiting List', 
                    selected_at = NULL, 
                    response_deadline = NULL
                WHERE id = ?
            """, (app_id,))
            
            # Free up the seat
            if company_name:
                update_seat_allocation(company_name, -1)
                logger.info(f"Freed up 1 seat for {company_name}")
            
            # Send notification to candidate
            try:
                send_update_to_candidate(
                    candidate_email, 
                    "Waiting List", 
                    company_name,
                    message=f"Your selection has been moved to the waiting list as we did not receive a response within 48 hours. You may still be considered if seats become available."
                )
                logger.info(f"Sent waiting list notification to {candidate_email}")
            except Exception as e:
                logger.error(f"Failed to send email to {candidate_email}: {str(e)}")
            
            # Now try to promote the next candidate from waiting list
            promote_next_candidate(company_name, cursor, conn)
        
        conn.commit()
        conn.close()
        logger.info("Expired selections processing completed successfully.")
        
    except Exception as e:
        logger.error(f"Error in check_and_update_expired_selections: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()


def promote_next_candidate(company_name, cursor, conn):
    """
    Promote the next best candidate from Applied/Waiting List status
    """
    try:
        # Get company info to check available seats
        company_info = get_company_info(company_name)
        
        if not company_info or company_info['available_seats'] <= 0:
            logger.info(f"No available seats for {company_name}. Cannot promote candidate.")
            return
        
        # Get all pending applications (Applied or Waiting List)
        pending_apps = cursor.execute("""
            SELECT a.*, u.name, u.email, u.phone, u.district, u.rural, u.social_category
            FROM applications a
            JOIN users u ON a.user_id = u.id
            WHERE a.company = ? AND a.status IN ('Applied', 'Waiting List')
            ORDER BY 
                CASE WHEN a.status = 'Waiting List' THEN 0 ELSE 1 END,
                a.created_at ASC
        """, (company_name,)).fetchall()
        
        if not pending_apps:
            logger.info(f"No pending candidates to promote for {company_name}")
            return
        
        # Convert to list of dicts
        candidates_list = [dict(app) for app in pending_apps]
        
        # Run AI filter to get the best candidate
        requirements = {'skills': ''}
        ranked_candidates = ai_filter_candidates(candidates_list, requirements)
        
        if not ranked_candidates:
            logger.info(f"No suitable candidates found for {company_name}")
            return
        
        # Get the top candidate
        top_candidate = ranked_candidates[0]['data']
        
        # Set 48-hour deadline (changed from 24 to 48 hours)
        selected_time = datetime.datetime.now()
        deadline = selected_time + datetime.timedelta(hours=48)
        
        # Update the candidate's status to Selected
        cursor.execute("""
            UPDATE applications 
            SET status = 'Selected', 
                selected_at = ?, 
                response_deadline = ?
            WHERE id = ?
        """, (selected_time.isoformat(), deadline.isoformat(), top_candidate['id']))
        
        # Update seat allocation
        update_seat_allocation(company_name, 1)
        
        logger.info(f"Promoted candidate: {top_candidate['name']} ({top_candidate['email']}) for {company_name}")
        
        # Send notification to the newly selected candidate
        try:
            send_update_to_candidate(
                top_candidate['email'], 
                "Selected", 
                company_name,
                message=f"Congratulations! You have been selected for the internship at {company_name}. Please respond within 48 hours to confirm your acceptance."
            )
            logger.info(f"Sent selection notification to {top_candidate['email']}")
        except Exception as e:
            logger.error(f"Failed to send email to {top_candidate['email']}: {str(e)}")
        
        conn.commit()
        
    except Exception as e:
        logger.error(f"Error in promote_next_candidate for {company_name}: {str(e)}")


def run_status_check():
    """
    Main function to run the status check
    This should be called periodically (e.g., every hour)
    """
    logger.info("=" * 80)
    logger.info("Starting automatic status check...")
    check_and_update_expired_selections()
    logger.info("Automatic status check completed.")
    logger.info("=" * 80)


if __name__ == "__main__":
    # Run the status check
    run_status_check()
