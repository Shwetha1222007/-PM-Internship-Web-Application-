import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "shwetha12206@gmail.com"          # 🔹 YOUR GMAIL
APP_PASSWORD = "lgsgrnkiqskjclky"             # 🔹 GMAIL APP PASSWORD
HR_EMAIL = "shwetha12206@gmail.com"               # 🔹 HR MAIL (same gmail OK)


def send_hr_email(candidate_name, company, skills, candidate_id):
    subject = "PM Internship Application – Action Required"

    body = f"""
New Internship Application Received

Candidate Name : {candidate_name}
Candidate ID   : {candidate_id}
Skills         : {skills}
Company        : {company}

ACCEPT:
http://localhost:8501/?action=accept&cid={candidate_id}

REJECT:
http://localhost:8501/?action=reject&cid={candidate_id}
"""

    _send_mail(HR_EMAIL, subject, body)


def send_candidate_email(candidate_email, status, company):
    subject = "PM Internship Application Status"

    body = f"""
Dear Candidate,

Your internship application for {company} has been {status}.

Status: {status}

Thank you for applying.
PM Internship Scheme
"""

    _send_mail(candidate_email, subject, body)


def _send_mail(receiver, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

    print(f"📩 Mail sent to {receiver}")
