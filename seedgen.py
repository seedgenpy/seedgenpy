#!/usr/bin/env python3
import hashlib, getpass, hmac

NEED = 99
BIAS_LIMIT = 252
ITERATIONS = 600_000
SEPARATOR = b"seedgen:v1:dice:pbkdf2-sha256"

def pbkdf2_sha256(password: bytes, salt: bytes, iterations: int) -> bytes:
    prf = lambda k, m: hmac.new(k, m, hashlib.sha256).digest()
    u = prf(password, salt + (1).to_bytes(4, "big"))
    result = bytearray(u)
    for _ in range(iterations - 1):
        u = prf(password, u)
        for i in range(32):
            result[i] ^= u[i]
    return bytes(result)

def dice_rolls(passphrase: bytes) -> str:
    key = pbkdf2_sha256(passphrase, SEPARATOR, ITERATIONS)
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

