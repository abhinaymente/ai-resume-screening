import os
import json
import base64
from google.oauth2.service_account import Credentials

# Scopes used across the project
SCOPES_SHEETS_DRIVE = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

SCOPES_CALENDAR = [
    "https://www.googleapis.com/auth/calendar",
]

def get_credentials(scopes):
    """
    Load Google service account credentials from base64 env variable.
    Works on Render / cloud.
    """
    encoded = os.environ["GOOGLE_CREDENTIALS"]
    decoded = base64.b64decode(encoded).decode("utf-8")
    creds_dict = json.loads(decoded)

    return Credentials.from_service_account_info(
        creds_dict,
        scopes=scopes
    )
