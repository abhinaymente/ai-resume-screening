import os
import smtplib
import ssl
from dotenv import load_dotenv

def test_connection():
    load_dotenv()
    
    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = os.getenv("EMAIL_HOST_USER") or os.getenv("FROM_EMAIL")
    password = os.getenv("EMAIL_HOST_PASSWORD")

    print("--- Gmail SMTP Connection Test ---")
    
    if not sender_email:
        print("❌ Error: EMAIL_HOST_USER is missing in .env")
        return
    
    if not password:
        print("❌ Error: EMAIL_HOST_PASSWORD is missing in .env")
        return

    print(f"📧 User: {sender_email}")
    print("🔑 Password: [HIDDEN]")
    print("🔌 Connecting to smtp.gmail.com:465...")

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            print("✅ Connection established.")
            print("🔐 Logging in...")
            server.login(sender_email, password)
            print("✅ Login successful!")
            print("🎉 Your email configuration is correct.")
    except smtplib.SMTPAuthenticationError:
        print("❌ Login failed: Authentication error.")
        print("   - Check if your App Password is correct.")
        print("   - Ensure 2-Step Verification is enabled.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
