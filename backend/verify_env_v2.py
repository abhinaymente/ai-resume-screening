import os
import json
import base64
from dotenv import load_dotenv

def verify_google_creds():
    load_dotenv()
    print("--- Checking GOOGLE_CREDENTIALS ---")
    
    raw = os.getenv("GOOGLE_CREDENTIALS")
    
    if not raw:
        print("❌ GOOGLE_CREDENTIALS is MISSING in .env")
        return

    print(f"Length: {len(raw)}")
    
    # Check for invalid characters (spaces/newlines) which broke it before
    if " " in raw:
        print("⚠️ Warning: Contains spaces (might be invalid base64 if not careful)")
    if "\n" in raw:
        print("⚠️ Warning: Contains newlines")

    try:
        # Decode
        decoded_bytes = base64.b64decode(raw)
        decoded_str = decoded_bytes.decode("utf-8")
        
        # Parse JSON
        data = json.loads(decoded_str)
        
        # logical checks
        if data.get("type") == "service_account":
            print("✅ Format: Base64 -> JSON (Service Account)")
            print(f"✅ Project ID: {data.get('project_id')}")
            print(f"✅ Client Email: {data.get('client_email')}")
            print("--------------------------------------------------")
            print("🎉 CONCLUSION: Your GOOGLE_CREDENTIALS looks PERFECT!")
            print("--------------------------------------------------")
        else:
            print("⚠️ Parsed JSON, but 'type' is not 'service_account'. Might be wrong key file.")
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"Decoded String (First 100 chars): {repr(decoded_str[:100])}")
        print("This means the Base64 decoded successfully, but the result wasn't valid JSON.")
    except Exception as e:
        print(f"❌ Invalid Base64 or Encoding Error: {e}")
        print("This usually means copy-paste errors, truncation, or invalid characters.")

if __name__ == "__main__":
    verify_google_creds()
