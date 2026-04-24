#!/usr/bin/env python3
import hashlib, getpass, hmac, unicodedata

NEED = 99
BIAS_LIMIT = 252
ITERATIONS = 600_000
SEPARATOR = b"seedgen:v1:dice:pbkdf2-sha256"

def pbkdf2_sha256(password: bytes, salt: bytes, iterations: int) -> bytes:
    u = hmac.digest(password, salt + (1).to_bytes(4, "big"), hashlib.sha256)
    result = bytearray(u)
    for _ in range(iterations - 1):
        u = hmac.digest(password, u, hashlib.sha256)
        for i in range(32):
            result[i] ^= u[i]
    return bytes(result)

def dice_rolls(passphrase: bytes) -> str:
    key = pbkdf2_sha256(passphrase, SEPARATOR, ITERATIONS)
    valid, counter = [], 0
    while len(valid) < NEED:
        block = hmac.digest(key, counter.to_bytes(8, "big"), hashlib.sha256)
        valid += [b for b in block if b < BIAS_LIMIT]
        counter += 1
    return "".join(str((x % 6) + 1) for x in valid[:NEED])

def normalize(p: str) -> bytes:
    return unicodedata.normalize("NFC", p).encode("utf-8")

if __name__ == "__main__":
    p1 = normalize(getpass.getpass("Passphrase : "))
    p2 = normalize(getpass.getpass("Confirm : "))
    if len(p1) == 0 or not hmac.compare_digest(p1, p2):
        raise SystemExit("Error: invalid or mismatched passphrase")
    print(dice_rolls(p1))

