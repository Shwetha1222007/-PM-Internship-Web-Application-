"""
AI-Driven Automatic Candidate Selection System
Handles automatic filtering, ranking, and status assignment with notifications
"""

import sqlite3
import datetime
import time
from database import get_connection
from ai_engine import ai_filter_candidates
from email_service import send_update_to_candidate, send_hr_announcement
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_auto_selector.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def process_company_applications(company_name):
    """
    AI-driven processing for a specific company:
    1. Filter all 'Applied' candidates using AI
    2. Rank them by AI score
    3. Assign statuses: 1st = Selected, 2nd = Shortlisted, 3rd+ = Waiting List
    4. Send notifications in order: 3rd → 2nd → 1st
    5. Notify HR when filtering is complete
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        logger.info(f"=" * 80)
        logger.info(f"Starting AI processing for company: {company_name}")
        
        # Get all 'Applied' candidates for this company
        applied_candidates = cursor.execute("""
            SELECT a.*, u.name, u.email, u.phone, u.district, u.rural, u.social_category, u.dob
            FROM applications a
            JOIN users u ON a.user_id = u.id
            WHERE a.company = ? AND a.status = 'Applied'
            ORDER BY a.created_at ASC
        """, (company_name,)).fetchall()
        
        if not applied_candidates or len(applied_candidates) == 0:
            logger.info(f"No applied candidates found for {company_name}")
            conn.close()
            return
        
        logger.info(f"Found {len(applied_candidates)} applied candidates for {company_name}")
        
        # Convert to list of dicts for AI processing
        candidates_list = [dict(candidate) for candidate in applied_candidates]
        
        # Run AI filtering and ranking
        logger.info("Running AI filtering and ranking...")
        requirements = {'skills': ''}  # Can be customized per company
        ranked_candidates = ai_filter_candidates(candidates_list, requirements)
        
        if not ranked_candidates:
            logger.warning(f"AI filtering returned no candidates for {company_name}")
            conn.close()
            return
        
        logger.info(f"AI ranking complete. Top candidate score: {ranked_candidates[0]['score']}")
        
        # Update AI scores in database
        for ranked in ranked_candidates:
            cursor.execute("""
                UPDATE applications 
                SET ai_score = ? 
                WHERE id = ?
            """, (ranked['score'], ranked['data']['id']))
        
        conn.commit()
        
        # Assign statuses based on ranking
        notifications_to_send = []
        
        for idx, ranked in enumerate(ranked_candidates):
            candidate = ranked['data']
            rank = idx + 1
            
            if rank == 1:
                # 1st candidate → Selected with 48-hour deadline
                status = "Selected"
                selected_time = datetime.datetime.now()
                deadline = selected_time + datetime.timedelta(hours=48)
                
                cursor.execute("""
                    UPDATE applications 
                    SET status = ?, selected_at = ?, response_deadline = ?
                    WHERE id = ?
                """, (status, selected_time.isoformat(), deadline.isoformat(), candidate['id']))
                
                message = f"🎉 Congratulations! You have been SELECTED for the internship at {company_name}. You must contact the company within 48 hours to confirm your acceptance. Deadline: {deadline.strftime('%B %d, %Y at %I:%M %p')}"
                
            elif rank == 2:
                # 2nd candidate → Shortlisted
                status = "Shortlisted"
                
                cursor.execute("""
                    UPDATE applications 
                    SET status = ?
                    WHERE id = ?
                """, (status, candidate['id']))
                
                message = f"🌟 Great news! You have been SHORTLISTED for the internship at {company_name}. You are the second-ranked candidate. If the top candidate doesn't respond within 48 hours, you will be automatically promoted to Selected status."
                
            else:
                # 3rd+ candidates → Waiting List
                status = "Waiting List"
                
                cursor.execute("""
                    UPDATE applications 
                    SET status = ?
                    WHERE id = ?
                """, (status, candidate['id']))
                
                message = f"📋 Your application for {company_name} has been placed on the Waiting List. You are ranked #{rank}. You will be notified if a position becomes available."
            
            # Store notification details (will send in reverse order)
            notifications_to_send.append({
                'email': candidate['email'],
                'name': candidate['name'],
                'status': status,
                'company': company_name,
                'message': message,
                'rank': rank,
                'ai_score': ranked['score']
            })
            
            logger.info(f"Assigned status '{status}' to {candidate['name']} (Rank #{rank}, Score: {ranked['score']})")
        
        conn.commit()
        
        # Send notifications in order: 3rd → 2nd → 1st (reverse order)
        logger.info("Sending notifications to candidates (3rd → 2nd → 1st)...")
        notifications_to_send.reverse()  # Reverse to send from last to first
        
        for notification in notifications_to_send:
            try:
                send_update_to_candidate(
                    notification['email'],
                    notification['status'],
                    notification['company'],
                    message=notification['message']
                )
                logger.info(f"✅ Sent {notification['status']} notification to {notification['name']} (Rank #{notification['rank']})")
                time.sleep(2)  # Small delay between emails
            except Exception as e:
                logger.error(f"❌ Failed to send notification to {notification['email']}: {str(e)}")
        
        # Send HR notification that AI filtering is complete
        logger.info("Sending completion notification to HR...")
        try:
            # Get the top candidate for HR notification
            top_candidate = ranked_candidates[0]['data']
            send_hr_notification_complete(company_name, len(ranked_candidates), top_candidate)
            logger.info(f"✅ Sent HR notification for {company_name}")
        except Exception as e:
            logger.error(f"❌ Failed to send HR notification: {str(e)}")
        
        conn.close()
        logger.info(f"AI processing complete for {company_name}")
        logger.info(f"=" * 80)
        
    except Exception as e:
        logger.error(f"Error in process_company_applications for {company_name}: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()


def send_hr_notification_complete(company_name, total_candidates, top_candidate):
    """
    Send notification to HR that AI filtering is complete
    """
    from email_service import _send_mail, HR_EMAIL
    
    subject = f"✅ AI FILTERING COMPLETE: {company_name} - {total_candidates} Candidates Processed"
    
    html = f"""
    <html>
    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="background-color: #28a745; padding: 25px; text-align: center; color: white; border-radius: 8px 8px 0 0;">
            <h1 style="margin: 0; font-size: 22px;">🤖 AI Filtering Complete</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">PM Internship Scheme - Automated Selection System</p>
        </div>
        <div style="padding: 30px; border: 1px solid #e1e4e8; border-top: none; background-color: #ffffff;">
            <p>Dear HR Manager,</p>
            <p>The AI-driven candidate filtering process has been completed for <strong>{company_name}</strong>.</p>
            
            <h3 style="color: #28a745; border-bottom: 2px solid #28a745; padding-bottom: 8px;">Processing Summary</h3>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff; width: 40%;">Total Candidates Processed</td><td style="padding: 10px; background: #f8faff;">{total_candidates}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">Status Assignments</td><td style="padding: 10px;">1 Selected, 1 Shortlisted, {total_candidates - 2} Waiting List</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff;">Notifications Sent</td><td style="padding: 10px; background: #f8faff;">All candidates notified (3rd → 2nd → 1st)</td></tr>
            </table>
            
            <h3 style="color: #00296b; border-bottom: 2px solid #f9ab00; padding-bottom: 8px;">Top Selected Candidate</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff; width: 40%;">Name</td><td style="padding: 10px; background: #f8faff;">{top_candidate['name']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">Email</td><td style="padding: 10px;">{top_candidate['email']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff;">AI Score</td><td style="padding: 10px; background: #f8faff;"><strong>{top_candidate.get('ai_score', 'N/A')}</strong></td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">CGPA</td><td style="padding: 10px;">{top_candidate['cgpa']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff;">Skills</td><td style="padding: 10px; background: #f8faff;">{top_candidate['skills']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">Response Deadline</td><td style="padding: 10px; color: #dc3545;"><strong>48 hours from selection</strong></td></tr>
            </table>
            
            <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #ffeeba;">
                <strong>⏰ Important:</strong> The selected candidate has 48 hours to respond. If they don't respond, the shortlisted candidate will be automatically promoted.
            </div>
            
            <div style="margin-top: 35px; text-align: center;">
                <p style="font-size: 14px; color: #666;">You can review all candidates and their rankings in the HR Dashboard.</p>
            </div>
        </div>
        <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
            This is an automated system generated email from the PM Internship Portal AI Engine.
        </div>
    </body>
    </html>
    """
    
    _send_mail(HR_EMAIL, subject, html, is_html=True)


def process_all_companies():
    """
    Process all companies that have pending applications
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all companies with 'Applied' status candidates
        companies = cursor.execute("""
            SELECT DISTINCT company 
            FROM applications 
            WHERE status = 'Applied'
        """).fetchall()
        
        conn.close()
        
        if not companies:
            logger.info("No companies with pending applications found")
            return
        
        logger.info(f"Found {len(companies)} companies with pending applications")
        
        for company_row in companies:
            company_name = company_row[0]
            process_company_applications(company_name)
            time.sleep(3)  # Delay between companies
            
    except Exception as e:
        logger.error(f"Error in process_all_companies: {str(e)}")


if __name__ == "__main__":
    # Run AI processing for all companies
    logger.info("Starting AI Auto-Selector...")
    process_all_companies()
    logger.info("AI Auto-Selector completed.")
