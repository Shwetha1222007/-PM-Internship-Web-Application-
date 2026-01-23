import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "shwetha12206@gmail.com"          # 🔹 YOUR GMAIL
APP_PASSWORD = "lgsgrnkiqskjclky"             # 🔹 GMAIL APP PASSWORD
HR_EMAIL = "shwetha12206@gmail.com"               # 🔹 HR MAIL (same gmail OK)

def send_hr_email(candidate_name, company, skills, candidate_id):
    subject = f"ACTION REQUIRED: New Internship Application - {candidate_name} (ID: {candidate_id})"
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background-color: #f8f9fa; padding: 20px; border-bottom: 2px solid #0056b3;">
            <h2 style="color: #0056b3; margin: 0;">PM Internship Scheme - Portal Notification</h2>
        </div>
        <div style="padding: 20px;">
            <p>Dear Hiring Manager,</p>
            <p>A new application has been submitted for an internship at <strong>{company}</strong> through the PM Internship Scheme portal.</p>
            
            <div style="background-color: #ffffff; border: 1px solid #e1e4e8; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 0;">Candidate Details</h3>
                <p><strong>Name:</strong> {candidate_name}</p>
                <p><strong>Candidate ID:</strong> {candidate_id}</p>
                <p><strong>Skills:</strong> {skills}</p>
                <p><strong>Sector:</strong> Applied Sector</p>
            </div>

            <p><strong>About the PM Internship Scheme:</strong><br>
            A flagship initiative by the Government of India to provide 1 crore internship opportunities in top 500 companies over 5 years. This scheme aims to bridge the gap between academic learning and industry requirements.</p>

            <p>Please review the candidate's profile and take formal action:</p>
            
            <div style="margin-top: 25px;">
                <a href="http://localhost:8501/?action=accept&cid={candidate_id}&comp={company}" 
                   style="background-color: #28a745; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-right: 15px;">
                   APPROVE CANDIDATE
                </a>
                <a href="http://localhost:8501/?action=reject&cid={candidate_id}&comp={company}" 
                   style="background-color: #dc3545; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                   REJECT CANDIDATE
                </a>
            </div>
        </div>
        <div style="margin-top: 30px; font-size: 0.8em; color: #777; border-top: 1px solid #eee; padding-top: 10px;">
            This is an automated message from the PM Internship Scheme Smart Allocation Engine.
        </div>
    </body>
    </html>
    """
    _send_mail(HR_EMAIL, subject, html, is_html=True)

def send_candidate_email(candidate_email, status, company):
    subject = f"UPDATE: Your Internship Application for {company}"
    
    status_color = "#28a745" if status == "Selected" else "#dc3545"
    status_text = "CONGRATULATIONS!" if status == "Selected" else "Application Status Update"
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background-color: #f8f9fa; padding: 20px; border-bottom: 2px solid {status_color};">
            <h2 style="color: {status_color}; margin: 0;">{status_text}</h2>
        </div>
        <div style="padding: 20px;">
            <p>Dear Candidate,</p>
            <p>Thank you for your interest in the <strong>PM Internship Scheme</strong>.</p>
            
            <p>We are writing to inform you about your application for an internship at <strong>{company}</strong>.</p>
            
            <div style="background-color: #fdfdfe; border: 1px solid #e1e4e8; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid {status_color};">
                <p style="font-size: 1.2em; margin: 0;">Final Status: <strong style="color: {status_color};">{status}</strong></p>
            </div>

            {"<p>Our team will contact you shortly regarding the next steps, documentation, and joining formalities.</p>" if status == "Selected" else "<p>While we are unable to proceed with your application for this specific role, your profile remains in our database for future opportunities that match your skill set.</p>"}

            <p>Warm regards,<br>
            <strong>Administrative Team</strong><br>
            PM Internship Scheme Hub</p>
        </div>
        <div style="margin-top: 30px; font-size: 0.8em; color: #777; border-top: 1px solid #eee; padding-top: 10px;">
            Please do not reply to this email. For support, visit the official portal.
        </div>
    </body>
    </html>
    """
    _send_mail(candidate_email, subject, html, is_html=True)

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
        print(f"📩 Mail sent to {receiver}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
