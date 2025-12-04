import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# ================= CONFIG =================
PRIVATE_KEY_FILE = "student_private.pem"    
ENCRYPTED_SEED_FILE = "encrypted/encrypted_seed.txt"
OUTPUT_FILE = "data/seed.txt"                       
# =========================================

def load_private_key(private_key_path: str) -> rsa.RSAPrivateKey:
    """Load RSA private key from PEM file"""
    try:
        pem_data = Path(private_key_path).read_bytes()
        private_key = serialization.load_pem_private_key(
            pem_data,
            password=None
        )
        return private_key
    except FileNotFoundError:
        print(f"Error: Private key file not found at {private_key_path}")
        raise
    except Exception as e:
        print(f"Error loading private key: {e}")
        raise

def decrypt_seed(encrypted_seed_b64: str, private_key: rsa.RSAPrivateKey) -> str:
    """Decrypt base64-encoded encrypted seed using RSA/OAEP"""
    try:
        # Step 1: Base64 decode
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)

        # Step 2: RSA/OAEP decrypt
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Step 3: Decode bytes to UTF-8
        hex_seed = decrypted_bytes.decode('utf-8')

        # Step 4: Validate 64-character hex string
        if len(hex_seed) != 64:
            raise ValueError("Decrypted seed is not 64 characters long")
        if not all(c in '0123456789abcdef' for c in hex_seed):
            raise ValueError("Decrypted seed contains invalid characters")

        return hex_seed

    except Exception as e:
        print(f"Error decrypting seed: {e}")
        raise

def main():
    # Load private key
    private_key = load_private_key(PRIVATE_KEY_FILE)

    # Read encrypted seed
    try:
        encrypted_seed_b64 = Path(ENCRYPTED_SEED_FILE).read_text().strip()
    except FileNotFoundError:
        print(f"Error: Encrypted seed file not found at {ENCRYPTED_SEED_FILE}")
        return
    except Exception as e:
        print(f"Error reading encrypted seed file: {e}")
        return

    # Decrypt seed
    try:
        hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
    except Exception:
        return

    # Ensure /data folder exists
    output_folder = Path("./data")
    output_folder.mkdir(exist_ok=True)

    # Save decrypted seed
    Path(OUTPUT_FILE).write_text(hex_seed)
    print(f"Decrypted seed saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
