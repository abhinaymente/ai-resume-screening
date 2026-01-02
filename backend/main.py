from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import time

from google_auth import get_credentials, SCOPES_SHEETS_DRIVE
from resume_reader import extract_text
from ai_evaluator import check_resume
from email_sender import send_email
from calendar_invite import schedule_interview

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- GLOBAL STATE ----------
LOGS = []
RESULTS = []

def log(msg: str):
    timestamp = time.strftime("%H:%M:%S")
    LOGS.append(f"[{timestamp}] {msg}")

# ---------- REQUEST MODEL ----------
class SheetRequest(BaseModel):
    sheet_link: str

# ---------- HELPERS ----------
def get_services():
    """Lazy load services to avoid startup crash if creds are missing"""
    print("Loading Google Credentials...")
    creds = get_credentials(SCOPES_SHEETS_DRIVE)
    sheets = build("sheets", "v4", credentials=creds)
    drive = build("drive", "v3", credentials=creds)
    return sheets, drive

def extract_sheet_id(link: str):
    return link.split("/d/")[1].split("/")[0]

def extract_file_id(link: str):
    if "id=" in link:
        return link.split("id=")[1]
    return link.split("/d/")[1].split("/")[0]

def download_resume(drive_service, file_id: str, filename: str):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

# ---------- BACKGROUND JOB ----------
def run_processing(sheet_link: str):
    LOGS.clear()
    RESULTS.clear()

    try:
        log("Initializing services...")
        # LATE BINDING: Initialize services here
        try:
            sheets_service, drive_service = get_services()
        except Exception as e:
            log(f"CRITICAL ERROR: Failed to load Google Credentials: {e}")
            return

        log("Started resume screening")

        sheet_id = extract_sheet_id(sheet_link)
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range="Form Responses 1"
        ).execute()

        rows = result.get("values", [])

        if len(rows) < 2:
            log("No responses found in Google Sheet")
            log("All resumes processed")
            return

        headers = rows[0]
        data_rows = rows[1:]

        # Create simplified list to find indices safely
        lower_headers = [h.lower().strip() for h in headers]
        
        try:
            email_idx = -1
            resume_idx = -1
            
            # Smart header match
            for i, h in enumerate(lower_headers):
                if "email" in h: email_idx = i
                if "resume" in h or "upload" in h or "cv" in h: resume_idx = i

            if email_idx == -1 or resume_idx == -1:
                log(f"Error: Columns not found. Headers: {headers}")
                return

        except Exception as e:
            log(f"Header parsing error: {e}")
            return

        for i, row in enumerate(data_rows, start=1):
            if len(row) <= max(email_idx, resume_idx):
                log(f"[{i}] Skipping empty/incomplete row")
                continue

            email = row[email_idx]
            resume_link = row[resume_idx]

            log(f"[{i}] Processing {email}")

            try:
                file_id = extract_file_id(resume_link)
                filename = f"resume_{i}.pdf"

                log(f"[{i}] Downloading resume...")
                download_resume(drive_service, file_id, filename)
                
                log(f"[{i}] Extracting text...")
                resume_text = extract_text(filename)

                log(f"[{i}] Analyzing with AI...")
                decision = check_resume(resume_text)
                
                status = "ELIGIBLE" if decision.startswith("ELIGIBLE") else "NOT ELIGIBLE"

                log(f"[{i}] Sending email ({status})...")
                if status == "ELIGIBLE":
                    meet = schedule_interview()
                    send_email(email, f"ELIGIBLE\nMeet: {meet}")
                else:
                    send_email(email, "NOT ELIGIBLE")

                RESULTS.append({
                    "email": email,
                    "status": status
                })

                if os.path.exists(filename):
                    os.remove(filename)
                log(f"[{i}] Completed")

            except Exception as e:
                log(f"[{i}] ERROR for {email}: {str(e)}")
                RESULTS.append({
                    "email": email,
                    "status": "ERROR"
                })

        log("All resumes processed")

    except Exception as e:
        log(f"FATAL ERROR: {str(e)}")
        log("All resumes processed")

# ---------- ROUTES ----------
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Resume Screener API is running"}

@app.post("/process")
def start(data: SheetRequest, bg: BackgroundTasks):
    bg.add_task(run_processing, data.sheet_link)
    return {"status": "started"}

@app.get("/logs")
def get_logs():
    return {"logs": LOGS}

@app.get("/results")
def get_results():
    return {"results": RESULTS}
