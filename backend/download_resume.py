from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# ✅ Use shared Google auth (env-based, no local files)
from google_auth import get_credentials, SCOPES_SHEETS_DRIVE

# -------- AUTH --------
creds = get_credentials(SCOPES_SHEETS_DRIVE)
drive_service = build("drive", "v3", credentials=creds)

# -------- FUNCTIONS --------
def extract_file_id(link: str):
    """
    Extract file ID from Google Drive link
    """
    if "id=" in link:
        return link.split("id=")[1]
    elif "/d/" in link:
        return link.split("/d/")[1].split("/")[0]
    else:
        return None


def download_file(file_id: str, output_filename: str):
    """
    Download file from Google Drive using file ID
    """
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_filename, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()
