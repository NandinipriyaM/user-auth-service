from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair(key_size: int = 4096):
    """
    Generate RSA key pair and return (private_key, public_key)
    """
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )

    # Get public key
    public_key = private_key.public_key()

    return private_key, public_key

def save_keys_to_files(private_key, public_key, priv_file="student_private.pem", pub_file="student_public.pem"):
    """
    Save private and public keys to PEM files
    """
    # Save private key
    with open(priv_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save public key
    with open(pub_file, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

if __name__ == "__main__":
    private_key, public_key = generate_rsa_keypair()
    save_keys_to_files(private_key, public_key)

    print("Keys saved successfully!")
