import binascii
import base64
import pyotp
from pathlib import Path

# ================= CONFIG =================
DECRYPTED_SEED_FILE = "data/seed.txt"   # decrypted hex seed file
# ==========================================


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance
    
    Args:
        hex_seed: 64-character hex string
        code: 6-digit code to verify
        valid_window: Number of periods before/after to accept (default 1 = ±30s)
    
    Returns:
        True if code is valid, False otherwise
    """

    # Validate hex seed
    if len(hex_seed) != 64 or not all(c in '0123456789abcdef' for c in hex_seed):
        raise ValueError("hex_seed must be a 64-character lowercase hex string")

    # Convert hex → bytes
    seed_bytes = binascii.unhexlify(hex_seed)

    # Convert bytes → base32
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')

    # Create TOTP object
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # Verify the code with window tolerance
    return totp.verify(code, valid_window=valid_window)


def main():
    # Read decrypted seed
    try:
        hex_seed = Path(DECRYPTED_SEED_FILE).read_text().strip()
    except FileNotFoundError:
        print(f"Error: decrypted seed file not found at {DECRYPTED_SEED_FILE}")
        return
    except Exception as e:
        print("Error reading seed file:", e)
        return

    # Get user input
    code = input("Enter the 6-digit TOTP code to verify: ").strip()

    # Validate user input
    if not (code.isdigit() and len(code) == 6):
        print("Invalid code format. Must be 6 digits.")
        return

    # Verify TOTP
    try:
        if verify_totp_code(hex_seed, code):
            print("TOTP code is VALID")
        else:
            print("TOTP code is INVALID")
    except Exception as e:
        print("Error verifying TOTP:", e)


if __name__ == "__main__":
    main()
