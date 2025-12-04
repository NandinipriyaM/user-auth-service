import binascii
import base64
import pyotp
from pathlib import Path

# ================= CONFIG =================
DECRYPTED_SEED_FILE = "data/seed.txt"  # Path to decrypted hex seed
# =========================================

def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed
    
    Args:
        hex_seed: 64-character hex string
    
    Returns:
        6-digit TOTP code as string
    """
    if len(hex_seed) != 64 or not all(c in '0123456789abcdef' for c in hex_seed):
        raise ValueError("hex_seed must be a 64-character hex string")

    # Convert hex seed to bytes
    seed_bytes = binascii.unhexlify(hex_seed)

    # Convert bytes to base32 (required by pyotp)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')

    # Create TOTP object (SHA1, 30s period, 6 digits)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # Generate current TOTP code
    return totp.now()

def main():
    # Read decrypted hex seed
    try:
        hex_seed = Path(DECRYPTED_SEED_FILE).read_text().strip()
    except FileNotFoundError:
        print(f"Error: Decrypted seed file not found at {DECRYPTED_SEED_FILE}")
        return
    except Exception as e:
        print(f"Error reading decrypted seed file: {e}")
        return

    # Generate TOTP
    try:
        totp_code = generate_totp_code(hex_seed)
        print("Current TOTP code:", totp_code)
    except Exception as e:
        print(f"Error generating TOTP code: {e}")

if __name__ == "__main__":
    main()
