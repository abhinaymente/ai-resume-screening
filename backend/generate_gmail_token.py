import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def generate_token():
    """
    Generates a Gmail OAuth 2.0 token for sending emails.
    Saves the token to 'gmail_token.json'.
    """
    print("Starting Gmail Token Generation...")
    
    if not os.path.exists('backend/credentials.json'):
         print("ERROR: 'backend/credentials.json' not found.")
         print("Please download your OAuth Client ID JSON from Google Cloud Console")
         print("and save it as 'backend/credentials.json'.")
         return

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'backend/credentials.json', SCOPES)
        
        # 1. Try Standard Local Server Flow (Best for Local Dev)
        # try:
        #     print("Attempting to open browser for authentication...")
        #     creds = flow.run_local_server(port=0)
        # except Exception as e:
        if True: # Force Manual Flow for Agent
            print(f"\nLocal server skipped. Switching to Manual Console Flow...")
            print(f"\nLocal server auth failed/timed out: (Forged Manual Mode)")
            print("Switching to Manual Console Flow...")
            # 2. Fallback to OOB/Console Flow
            # Note: This requires 'urn:ietf:wg:oauth:2.0:oob' redirect URI in Google Console
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print(f"\nPlease visit this URL to authorize:\n{auth_url}\n")
            code = input("Enter the authorization code: ").strip()
            flow.fetch_token(code=code)
            creds = flow.credentials

        # Save credentials
        with open('gmail_token.json', 'w') as token:
            token.write(creds.to_json())
            print("\nSuccess! Token saved to 'gmail_token.json'")
            print("Next: Copy this file content (Base64 encoded) to your Render GMAIL_TOKEN env var.")

    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")

if __name__ == '__main__':
    generate_token()
