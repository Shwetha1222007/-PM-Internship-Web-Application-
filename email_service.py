import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Professional configuration
SENDER_EMAIL = "shwetha12206@gmail.com"
APP_PASSWORD = "lgsgrnkiqskjclky"
HR_EMAIL = "shwetha12206@gmail.com"
HR_ADMIN_EMAIL = "admin@internship.gov.in" # Target for HR rejection audits

# UPDATE THIS TO YOUR DEPLOYED URL (e.g., https://your-app.streamlit.app)
BASE_URL = "http://localhost:8501" 

def send_hr_announcement(candidate_profile, application_data, same_qualification=False):
    """
    Sends a simple notification to HR that new candidates are available for review.
    """
    subject = f"NEW APPLICATIONS: PM Internship Scheme Review Required"
    
    html = f"""
    <html>
    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="background-color: #00296b; padding: 25px; text-align: center; color: white; border-radius: 8px 8px 0 0;">
            <h1 style="margin: 0; font-size: 22px;">PM Internship Scheme - HR Alert</h1>
        </div>
        <div style="padding: 30px; border: 1px solid #e1e4e8; border-top: none; background-color: #ffffff;">
            <p>Dear Hiring Manager,</p>
            <p>New candidates have been identified for your review at <strong>{application_data['company']}</strong>.</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #dee2e6;">
                <p style="margin: 0;"><strong>Notification:</strong> {len(application_data) if isinstance(application_data, list) else "1"} New candidate(s) are pending review in your dashboard.</p>
            </div>

            <p>Please login to the <strong>HR Dashboard</strong> to view full candidate profiles, including technical skills, academic performance, and personal details.</p>
            
            <div style="margin-top: 30px; text-align: center;">
                <a href="{BASE_URL}" style="background-color: #00296b; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">OPEN HR DASHBOARD</a>
            </div>
            
            <p style="margin-top: 25px; font-size: 13px; color: #666;"><em>Note: To ensure fair selection, candidate details are now primarily disclosed via the secure portal dashboard.</em></p>
        </div>
        <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
            This is an automated system generated email from the Ministry of Corporate Affairs.
        </div>
    </body>
    </html>
    """
    _send_mail(HR_EMAIL, subject, html, is_html=True)
    _send_mail(HR_EMAIL, subject, html, is_html=True)

def send_admin_rejection_audit(hr_name, candidate_name, company, reason):
    """
    Notifies Admin when HR rejects a top candidate.
    """
    subject = f"🛑 HR REJECTION AUDIT: {company}"
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background-color: #dc3545; padding: 20px; text-align: center; color: white;">
            <h2 style="margin: 0;">Selection Committee Audit - Rejection Log</h2>
        </div>
        <div style="padding: 30px; border: 1px solid #e1e4e8; border-top: none;">
            <p>Dear Administrator,</p>
            <p>Hiring Manager <strong>{hr_name}</strong> has rejected a top-ranked candidate. As per policy, the valid reason has been recorded below:</p>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr><td style="padding: 10px; font-weight: bold; border: 1px solid #ddd;">Company</td><td style="padding: 10px; border: 1px solid #ddd;">{company}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; border: 1px solid #ddd;">Rejected Candidate</td><td style="padding: 10px; border: 1px solid #ddd;">{candidate_name}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; border: 1px solid #ddd;">Reason for Rejection</td><td style="padding: 10px; border: 1px solid #ddd; background: #fff8f8; color: #c00;">{reason}</td></tr>
            </table>
            
            <p style="color: #666; font-size: 13px;"><em>Note: The 2nd place shortlisted candidate has been automatically promoted to 'Selected' status for this position.</em></p>
        </div>
    </body>
    </html>
    """
    _send_mail(HR_ADMIN_EMAIL, subject, html, is_html=True)

def send_update_to_candidate(email, status, company, message=None):
    """
    Professional update for candidate.
    """
    subject = f"OFFICIAL NOTIFICATION: Internship Application Update - {company}"
    
    # Determine status colors
    if status == "Selected":
        status_bg = "#d4edda"
        status_color = "#155724"
    elif status == "Shortlisted":
        status_bg = "#cce5ff"
        status_color = "#004085"
    elif status == "Waiting List":
        status_bg = "#fff3cd"
        status_color = "#856404"
    else:
        status_bg = "#f8d7da"
        status_color = "#721c24"
    
    # Default messages based on status
    if message is None:
        if status == "Selected":
            message = "Congratulations! You have been officially SELECTED for the position. Your details have been finalized in our system. Please check your dashboard for onboarding instructions."
        elif status == "Shortlisted":
            message = "Great news! You have been SHORTLISTED for the next stage of the selection process. Our HR team is currently reviewing your profile for final approval. We will notify you once the final decision is made."
        elif status == "Waiting List":
            message = "Your application has been moved to the waiting list. This means you are still being considered for the position. If a seat becomes available, you will be automatically selected and notified."
        else:
            message = "Thank you for your interest in this role. However, the selection committee has decided to proceed with other candidates at this time."
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background-color: #00296b; padding: 20px; text-align: center; color: white;">
            <h2 style="margin: 0;">PM Internship Scheme Hub</h2>
        </div>
        <div style="padding: 30px; border: 1px solid #e1e4e8; border-top: none;">
            <p>Dear Candidate,</p>
            <p>Thank you for your active participation in the <strong>PM Internship Scheme</strong>.</p>
            <p>We are writing to provide a status update on your application for the internship opening at <strong>{company}</strong>.</p>
            
            <div style="background-color: {status_bg}; color: {status_color}; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid {status_color}; text-align: center;">
                <h3 style="margin: 0; font-size: 20px;">Current Status: {status}</h3>
            </div>

            <p>{message}</p>

            <p style="margin-top: 30px;">Best regards,<br><strong>Central Administration Team</strong><br>PM Internship Scheme Portal</p>
        </div>
    </body>
    </html>
    """
    _send_mail(email, subject, html, is_html=True)

def _send_mail(receiver, subject, content, is_html=False):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver
    msg.attach(MIMEText(content, "html" if is_html else "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        raise e # Explicitly raise to be caught by the UI

def send_candidate_confirmation(candidate_profile, application_data):
    """
    Sends a confirmation email to the candidate after they apply.
    """
    subject = f"APPLICATION RECEIVED: PM Internship Scheme - {application_data['company']}"
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background-color: #00296b; padding: 20px; text-align: center; color: white;">
            <h2 style="margin: 0;">PM Internship Scheme Confirmation</h2>
        </div>
        <div style="padding: 30px; border: 1px solid #e1e4e8; border-top: none;">
            <p>Dear {candidate_profile['name']},</p>
            <p>Your application for the <strong>{application_data['company']}</strong> internship has been successfully received.</p>
            
            <h3 style="color: #00296b;">Application Details:</h3>
            <ul>
                <li><strong>Sector:</strong> {application_data['sector']}</li>
                <li><strong>Reference ID:</strong> PMIS-{str(candidate_profile['id']).zfill(6)}</li>
                <li><strong>Status:</strong> Applied (Under Review)</li>
            </ul>

            <p>Your profile has been forwarded to the HR department of <strong>{application_data['company']}</strong>. You will receive another update once they review your application.</p>

            <p>You can track your application status anytime by logging into your dashboard.</p>

            <p style="margin-top: 30px;">Best regards,<br><strong>PM Internship Support Team</strong></p>
        </div>
    </body>
    </html>
    """
    _send_mail(candidate_profile['email'], subject, html, is_html=True)
