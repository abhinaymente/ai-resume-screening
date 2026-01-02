import os
import json
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """
    Lazy loads Gmail Service from GMAIL_TOKEN env var (Base64 encoded json).
    """
    encoded_token = os.getenv("GMAIL_TOKEN")
    
    if not encoded_token:
        # Fallback for local testing if file exists
        if os.path.exists("gmail_token.json"):
            return build('gmail', 'v1', credentials=Credentials.from_authorized_user_file('gmail_token.json', SCOPES))
        raise ValueError("GMAIL_TOKEN not set in .env")

    try:
        decoded_json = base64.b64decode(encoded_token).decode("utf-8")
        creds_data = json.loads(decoded_json)
        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        raise ValueError(f"Invalid GMAIL_TOKEN: {e}")
