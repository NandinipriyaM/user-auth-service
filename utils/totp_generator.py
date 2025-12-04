import time
import hmac
import hashlib
import struct

def generate_totp(hex_seed: str, interval: int = 30, digits: int = 6) -> str:
    hex_seed = hex_seed.strip()

    if hex_seed.startswith(("0x", "0X")):
        hex_seed = hex_seed[2:]

    if any(c not in "0123456789abcdefABCDEF" for c in hex_seed):
        raise ValueError("Seed must be hex string")

    key = bytes.fromhex(hex_seed)
    counter = int(time.time()) // interval

    msg = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()

    offset = hmac_hash[-1] & 0x0F
    binary = (
        ((hmac_hash[offset] & 0x7F) << 24)
        | (hmac_hash[offset + 1] << 16)
        | (hmac_hash[offset + 2] << 8)
        | (hmac_hash[offset + 3])
    )

    otp = binary % (10 ** digits)
    return str(otp).zfill(digits)
