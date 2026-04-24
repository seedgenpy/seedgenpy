#!/usr/bin/env python3
import hashlib, getpass, hmac

NEED = 99
BIAS_LIMIT = 252
ITERATIONS = 600_000
SEPARATOR = b"seedgen:v1:dice:pbkdf2-sha256"

def dice_rolls(passphrase: bytes) -> str:
    key = hashlib.pbkdf2_hmac("sha256", passphrase, SEPARATOR, ITERATIONS, dklen=32)
    valid, counter = [], 0
    while len(valid) < NEED:
        block = hmac.new(key, counter.to_bytes(8, "big"), hashlib.sha256).digest()
        valid += [b for b in block if b < BIAS_LIMIT]
        counter += 1
    return "".join(str((x % 6) + 1) for x in valid[:NEED])

if __name__ == "__main__":
    p1 = getpass.getpass("Passphrase : ").encode("utf-8")
    p2 = getpass.getpass("Confirm : ").encode("utf-8")
    if len(p1) == 0 or not hmac.compare_digest(p1, p2):
        raise SystemExit("Error: invalid or mismatched passphrase")
    print(dice_rolls(p1))

