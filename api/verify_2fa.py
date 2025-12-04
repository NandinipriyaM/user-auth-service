import time
from pathlib import Path
from fastapi import APIRouter, Request

from utils.totp_generator import generate_totp 

SEED_FILE = "data/seed.txt"
router = APIRouter()

@router.post("/verify-2fa")
async def verify_2fa(request: Request):
    body = await request.json()
    code = body.get("code")

    # 1. Validate code
    if not code:
        return {"error": "Missing code"}

    seed_path = Path(SEED_FILE)

    # 2. Check if seed exists
    if not seed_path.exists():
        return {"error": "Seed not decrypted yet"}

    # 3. Read seed
    hex_seed = seed_path.read_text().strip()

    # 4. Verify with ±1 time window tolerance
    now = int(time.time())
    intervals = [
        now // 30,         # current
        (now // 30) - 1,   # previous (tolerance)
        (now // 30) + 1    # next (tolerance)
    ]

    valid = False
    for counter in intervals:
        try:
            expected = generate_totp(hex_seed, interval=30, digits=6)
            if code == expected:
                valid = True
                break
        except Exception:
            return {"error": "Invalid seed"}

    # 5. Return result
    return {"valid": valid}
