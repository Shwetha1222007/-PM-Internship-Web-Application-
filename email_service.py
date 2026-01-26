import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Professional configuration
SENDER_EMAIL = "shwetha12206@gmail.com"
APP_PASSWORD = "lgsgrnkiqskjclky"
HR_EMAIL = "shwetha12206@gmail.com"

def send_hr_announcement(candidate_profile, application_data):
    """
    Sends a highly detailed email to HR for review.
    """
    subject = f"APPLICATION FOR REVIEW: PM Internship Scheme - {candidate_profile['name']}"
    
    html = f"""
    <html>
    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="background-color: #00296b; padding: 25px; text-align: center; color: white; border-radius: 8px 8px 0 0;">
            <h1 style="margin: 0; font-size: 22px;">PM Internship Scheme - Official India</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.8;">Smart Allocation Engine - Candidate Profile Disclosure</p>
        </div>
        <div style="padding: 30px; border: 1px solid #e1e4e8; border-top: none; background-color: #ffffff;">
            <p>Dear Hiring Manager,</p>
            <p>A new candidate has been identified as a <strong>High Match</strong> for <strong>{application_data['company']}</strong> in the <strong>{application_data['sector']}</strong> sector.</p>
            
            <h3 style="color: #00296b; border-bottom: 2px solid #f9ab00; padding-bottom: 8px;">Candidate Technical Summary</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff; width: 35%;">Full Name</td><td style="padding: 10px; background: #f8faff;">{candidate_profile['name']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">ID Number</td><td style="padding: 10px;">PMIS-{str(candidate_profile['id']).zfill(6)}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff;">College Name</td><td style="padding: 10px; background: #f8faff;">{application_data['college_name']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">Academic CGPA</td><td style="padding: 10px;">{application_data['cgpa']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff;">Key Skills</td><td style="padding: 10px; background: #fffdf5;">{application_data['skills']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">Languages</td><td style="padding: 10px;">{application_data['languages']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; background: #f8faff;">Experience</td><td style="padding: 10px; background: #f8faff;">{application_data['experience']}</td></tr>
                <tr><td style="padding: 10px; font-weight: bold;">Rural Candidate</td><td style="padding: 10px;">{candidate_profile['rural']}</td></tr>
            </table>

            <div style="margin-top: 35px; text-align: center;">
                <p style="font-size: 14px; color: #666;">Evaluate and take immediate action on this application:</p>
                <a href="http://localhost:8501/?action=accept&aid={application_data['app_id']}" 
                   style="background-color: #28a745; color: white; padding: 14px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; margin-right: 15px; display: inline-block;">
                   APPROVE APPLICATION
                </a>
                <a href="http://localhost:8501/?action=reject&aid={application_data['app_id']}" 
                   style="background-color: #dc3545; color: white; padding: 14px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                   DECLINE PROFILE
                </a>
            </div>
        </div>
        <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
            This is an automated system generated email from the Ministry of Corporate Affairs Internship Portal.
        </div>
    </body>
    </html>
    """
    _send_mail(HR_EMAIL, subject, html, is_html=True)

def send_update_to_candidate(email, status, company):
    """
    Professional update for candidate.
    """
    subject = f"OFFICIAL NOTIFICATION: Internship Application Update - {company}"
    status_bg = "#d4edda" if status == "Selected" else "#f8d7da"
    status_color = "#155724" if status == "Selected" else "#721c24"
    
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

            {f"<p>Congratulations! You have been shortlisted by the selection committee. The company human resources team will reach out to you within the next 48 hours with the final offer letter and joining instructions.</p>" if status == "Selected" else "<p>Thank you for your interest in this role. However, the company has decided to pursue other candidates whose profiles more closely match their current requirements. We encourage you to apply for other exciting opportunities on our portal.</p>"}

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
