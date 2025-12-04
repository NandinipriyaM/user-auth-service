from pathlib import Path
import requests
import json

# ================= CONFIGURATION =================
STUDENT_ID = "23P31A0535"
GITHUB_REPO_URL = "https://github.com/NandinipriyaM/user-auth-service"
PUBLIC_KEY_FILE = "./student_public.pem"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
# =================================================

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API
    
    Steps:
    1. Read student public key from PEM file
    2. Prepare HTTP POST request payload
    3. Send POST request to instructor API
    4. Parse JSON response
    5. Save encrypted seed to file
    """
    # --- Step 1: Read public key ---
    try:
        public_key = Path(PUBLIC_KEY_FILE).read_text().strip()
    except FileNotFoundError:
        print(f"Error: Public key file not found at {PUBLIC_KEY_FILE}")
        return
    except Exception as e:
        print(f"Error reading public key: {e}")
        return

    # --- Step 2: Prepare payload ---
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # --- Step 3: Send POST request ---
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return

    # --- Step 4: Parse response ---
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Error: API response is not valid JSON")
        print("Response text:", response.text)
        return

    print("API Response:", data) 

    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        print("Error: 'encrypted_seed' is missing or empty in API response")
        return

    # --- Step 5: Save encrypted seed ---
    encrypted_folder = Path("./encrypted")
    encrypted_folder.mkdir(exist_ok=True)

    output_path = encrypted_folder / "encrypted_seed.txt"
    output_path.write_text(encrypted_seed)
    print(f"Encrypted seed saved to {output_path}")

if __name__ == "__main__":
    request_seed(STUDENT_ID, GITHUB_REPO_URL, API_URL)
