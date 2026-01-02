def check_env_binary():
    try:
        with open(".env", "rb") as f:
            for line in f:
                if line.startswith(b"GOOGLE_CREDENTIALS="):
                    val = line.split(b"=", 1)[1].strip()
                    print(f"Found GOOGLE_CREDENTIALS line.")
                    print(f"Length: {len(val)}")
                    
                    # Check for non-ascii
                    try:
                        str_val = val.decode("utf-8")
                        print("✅ UTF-8 Decode: OK")
                    except UnicodeDecodeError as e:
                        print(f"❌ UTF-8 Decode Failed: {e}")
                        print("This means there are hidden binary characters (smart quotes, etc).")
                        return

                    # Check base64 chars only
                    import re
                    if not re.match(r'^[A-Za-z0-9+/=]+$', str_val):
                        print("❌ Failed: Contains characters that are NOT valid Base64.")
                        # Find the bad chars
                        bad = [c for c in str_val if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="]
                        print(f"   Bad characters found: {bad[:10]}")
                    else:
                        print("✅ Structure: Valid Base64 characters only.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_env_binary()
