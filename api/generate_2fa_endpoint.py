import time
from pathlib import Path
from fastapi import APIRouter, HTTPException
from utils.totp_generator import generate_totp

router = APIRouter()

SEED_FILE = Path("data/seed.txt")
INTERVAL = 30

@router.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = SEED_FILE.read_text().strip()

    try:
        code = generate_totp(hex_seed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid seed: {e}")

    now = int(time.time())
    remaining = INTERVAL - (now % INTERVAL)
    if remaining == INTERVAL:
        remaining = 0

    return {"code": code, "valid_for": remaining}
