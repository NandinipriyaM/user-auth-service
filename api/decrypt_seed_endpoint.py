import base64
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

PRIVATE_KEY_PATH = "student_private.pem"
OUTPUT_SEED_PATH = "data/seed.txt"

router = APIRouter()

class SeedRequest(BaseModel):
    encrypted_seed: str


def load_private_key():
    try:
        pem = Path(PRIVATE_KEY_PATH).read_bytes()
        return serialization.load_pem_private_key(pem, password=None)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load private key: {e}"
        )

@router.post("/decrypt-seed")
def decrypt_seed(request: SeedRequest):
    try:
        private_key = load_private_key()
        encrypted_bytes = base64.b64decode(request.encrypted_seed)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        hex_seed = decrypted_bytes.decode().strip()
        print("Decrypted seed:", hex_seed)

        if len(hex_seed) != 64 or not all(c in "0123456789abcdef" for c in hex_seed):
            return {"error": "Decryption failed"}  # <--- return error JSON if invalid

        Path("data").mkdir(exist_ok=True)
        Path(OUTPUT_SEED_PATH).write_text(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        print("Error:", e)
        return {"error": "Decryption failed"}  # <--- return error JSON instead of raising HTTPException


