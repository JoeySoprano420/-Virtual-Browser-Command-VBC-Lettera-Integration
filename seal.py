import hashlib, struct, os

MAGIC = b"LETSEAL"

def add_seal(exe_path):
    with open(exe_path, "rb") as f:
        data = f.read()

    digest = hashlib.sha256(data).digest()
    sealed = data + MAGIC + digest

    with open(exe_path, "wb") as f:
        f.write(sealed)

    print(f"[SEALED] Binary sealed with SHA256, length {len(digest)} bytes")
    return True

def verify_seal(exe_path):
    with open(exe_path, "rb") as f:
        data = f.read()

    if MAGIC not in data:
        print("[UNSEALED] No seal found.")
        return False

    payload, magic, digest = data[:-len(MAGIC)-32], data[-len(MAGIC)-32:-32], data[-32:]
    calc = hashlib.sha256(payload).digest()
    if digest == calc:
        print("[VERIFIED] Seal intact.")
        return True
    else:
        print("[CORRUPT] Seal invalid!")
        return False
