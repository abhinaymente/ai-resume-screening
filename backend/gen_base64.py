import base64
import json
import os

def generate_base64():
    source_path = "service_account.json"
    if not os.path.exists(source_path):
        print("Error: service_account.json not found")
        return

    # Read JSON
    with open(source_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Serialize to compact JSON string (no spaces)
    json_str = json.dumps(data, separators=(',', ':'))
    
    # Encode
    b64_bytes = base64.b64encode(json_str.encode("utf-8"))
    b64_str = b64_bytes.decode("utf-8")
    
    print(f"Correct Length: {len(b64_str)}")
    
    with open("final_creds.txt", "w", encoding="utf-8") as out:
        out.write(b64_str)
        
    print("✅ Credential string saved to final_creds.txt")

if __name__ == "__main__":
    generate_base64()
