import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_email(
    to_email: str,
    username: str,
    token: str,
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str
):
    # Verification URL (adjust to your domain)
    verification_url = f"http://localhost:8000/verify-email?token={token}"

    subject = "Verify your email address"
    body = f"""
    Hi {username},

    Please click the link below to verify your email address:
    {verification_url}

    If you didn't register, please ignore this email.

    Best,
    Your Team
    """

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"Verification email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send verification email: {e}")