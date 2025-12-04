import os
from pathlib import Path
import pyotp
from datetime import datetime, timezone

SEED_FILE = "/data/seed.txt"
OUTPUT_FILE = "/cron/last_code.txt"

def read_seed():
    seed_path = Path(SEED_FILE)
    if not seed_path.exists():
        return None
    return seed_path.read_text().strip()

def generate_totp(hex_seed: str) -> str:
    base32_seed = pyotp.utils.hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.now()

def main():
    hex_seed = read_seed()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    if not hex_seed:
        line = f"{timestamp} - Seed not found\n"
    else:
        code = generate_totp(hex_seed)
        line = f"{timestamp} - 2FA Code: {code}\n"

    with open(OUTPUT_FILE, "a") as f:
        f.write(line)

if __name__ == "__main__":
    main()
