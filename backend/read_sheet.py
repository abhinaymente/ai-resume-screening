from googleapiclient.discovery import build
import pandas as pd

# ✅ Shared Google auth (env-based, Render-safe)
from google_auth import get_credentials, SCOPES_SHEETS_DRIVE

# ---------- CONFIG ----------
SPREADSHEET_ID = "1rC-88voXWtwb102CSdu6k3y-OCJxk1YMJNJuHUkpYpA"

# ---------- AUTH ----------
creds = get_credentials(SCOPES_SHEETS_DRIVE)
service = build("sheets", "v4", credentials=creds)

# ---------- READ SHEET ----------
sheet = service.spreadsheets()
result = sheet.values().get(
    spreadsheetId=SPREADSHEET_ID,
    range="Form Responses 1"
).execute()

values = result.get("values", [])

if len(values) < 2:
    print("No data found in sheet")
else:
    df = pd.DataFrame(values[1:], columns=values[0])
    print(df["resume"])
