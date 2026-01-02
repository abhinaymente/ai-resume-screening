import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from gmail_client import get_gmail_service

load_dotenv()

def send_email(to_email: str, decision: str):
    """
    Sends email using Gmail API (Oauth 2.0) to bypass SMTP port blocks.
    """
    try:
        service = get_gmail_service()
    except Exception as e:
        print(f"FAILED to load Gmail Service: {e}")
        # If we can't load the service, we can't send email.
        # But we don't want to crash the whole app loop? 
        # Actually raising error is better so logs show it.
        raise e

    COMPANY_NAME = "DUDE TECH"
    TAGLINE = "Building smart hiring systems"
    BRAND_GRADIENT = "linear-gradient(135deg,#667eea,#764ba2)"
    
    # Check "FROM_EMAIL" env var if user wants custom display name logic, 
    # though Gmail API usually forces the authenticated user's address as sender.
    sender_email = "me" 

    # Create message container
    msg = MIMEMultipart("alternative")
    msg['To'] = to_email
    msg['From'] = f"{COMPANY_NAME} <me>" # Gmail API handles the 'me'

    # ================= ELIGIBLE =================
    if decision.startswith("ELIGIBLE"):
        meet_link = decision.split("Meet:")[-1].strip()
        subject = "🎉 Interview Invitation – Software Engineer | DUDE TECH"
        msg['Subject'] = subject

        html_body = f"""
        <html>
        <body style="margin:0;background:#f4f6fc;font-family:Arial,sans-serif;">
          <div style="max-width:600px;margin:30px auto;background:#ffffff;
                      border-radius:14px;overflow:hidden;
                      box-shadow:0 15px 40px rgba(0,0,0,0.2)">
            <!-- HEADER -->
            <div style="background:{BRAND_GRADIENT};padding:26px;color:white;">
              <h2 style="margin:0;">{COMPANY_NAME}</h2>
              <p style="margin:6px 0 0;font-size:14px;">{TAGLINE}</p>
            </div>
            <!-- BODY -->
            <div style="padding:26px;color:#1a202c;">
              <p>Hello,</p>
              <p>Thank you for applying for the <strong>Software Engineer</strong> position at <strong>{COMPANY_NAME}</strong>.</p>
              <p>After reviewing your resume, we are happy to inform you that your profile has been <strong>shortlisted</strong>.</p>
              <div style="background:#eef2ff;padding:16px;border-radius:10px;margin:20px 0;">
                <p style="margin:0;"><strong>📅 Interview Details</strong></p>
                <p style="margin:8px 0;">Mode: Google Meet</p>
                <p style="margin:8px 0;">Meeting Link:<br/><a href="{meet_link}" style="color:#4f46e5;">{meet_link}</a></p>
              </div>
              <p style="margin-top:28px;">Best regards,<br/><strong>Hiring Team</strong><br/>{COMPANY_NAME}</p>
            </div>
            <!-- FOOTER -->
            <div style="background:#f8fafc;padding:14px;text-align:center;font-size:12px;color:#6b7280;">
              © {COMPANY_NAME} · AI-powered recruitment platform
            </div>
          </div>
        </body>
        </html>
        """

    # ================= NOT ELIGIBLE =================
    else:
        subject = "Application Update – Software Engineer | DUDE TECH"
        msg['Subject'] = subject

        html_body = f"""
        <html>
        <body style="margin:0;background:#f4f6fc;font-family:Arial,sans-serif;">
          <div style="max-width:600px;margin:30px auto;background:#ffffff;
                      border-radius:14px;overflow:hidden;
                      box-shadow:0 15px 40px rgba(0,0,0,0.2)">
            <!-- HEADER -->
            <div style="background:#111827;padding:26px;color:white;">
              <h2 style="margin:0;">{COMPANY_NAME}</h2>
              <p style="margin:6px 0 0;font-size:14px;">{TAGLINE}</p>
            </div>
            <!-- BODY -->
            <div style="padding:26px;color:#1a202c;">
              <p>Hello,</p>
              <p>Thank you for your interest in the <strong>Software Engineer</strong> position.</p>
              <p>After careful review, we will not be moving forward with your application at this time.</p>
              <p style="margin-top:28px;">Best regards,<br/><strong>Hiring Team</strong><br/>{COMPANY_NAME}</p>
            </div>
            <!-- FOOTER -->
            <div style="background:#f8fafc;padding:14px;text-align:center;font-size:12px;color:#6b7280;">
              © {COMPANY_NAME} · AI-powered recruitment platform
            </div>
          </div>
        </body>
        </html>
        """

    # Attach HTML
    msg.attach(MIMEText(html_body, "html"))

    # Send via Gmail API
    try:
        raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        message = service.users().messages().send(userId=sender_email, body={'raw': raw_string}).execute()
        print(f"Email sent via Gmail API! Message Id: {message['id']}")
    except Exception as e:
        print(f"An error occurred sending email: {e}")
        raise e
