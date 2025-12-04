import base64
import subprocess
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# ===================== Functions =====================

def sign_message(message: str, private_key: rsa.RSAPrivateKey) -> bytes:
    """
    Sign a message (ASCII string) using RSA-PSS with SHA-256
    """
    signature = private_key.sign(
        message.encode('utf-8'),  # ASCII bytes
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """
    Encrypt data using RSA/OAEP with SHA-256
    """
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

# ===================== Main Script =====================

# Step 1: Get current commit hash (40-character hex)
commit_hash = subprocess.check_output(
    ["git", "log", "-1", "--format=%H"]
).decode("utf-8").strip()
print(f"Commit Hash: {commit_hash}")

# Step 2: Load student private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Step 3: Sign commit hash
signature_bytes = sign_message(commit_hash, private_key)

# Step 4: Load instructor public key
with open("instructor_public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Step 5: Encrypt signature
encrypted_signature_bytes = encrypt_with_public_key(signature_bytes, public_key)

# Step 6: Base64 encode encrypted signature
encrypted_signature_b64 = base64.b64encode(encrypted_signature_bytes).decode('utf-8')
print(f"Encrypted Signature (Base64, single line):\n{encrypted_signature_b64}")
