import hashlib, sys, os

MAGIC = b"LETSEAL"

def add_seal(exe_path):
    with open(exe_path, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).digest()
    sealed = data + MAGIC + digest
    with open(exe_path, "wb") as f:
        f.write(sealed)
    print(f"[SEALED] {exe_path} sealed (SHA256)")
    return True

def verify_seal(exe_path):
    with open(exe_path, "rb") as f:
        data = f.read()
    if MAGIC not in data:
        print("[UNSEALED] No seal found.")
        return False
    payload = data[:-len(MAGIC)-32]
    digest = data[-32:]
    calc = hashlib.sha256(payload).digest()
    if digest == calc:
        print("[VERIFIED] Seal intact.")
        return True
    else:
        print("[CORRUPT] Seal invalid!")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m lettera.seal [verify|seal] file")
        sys.exit(1)
    cmd, file = sys.argv[1], sys.argv[2]
    if cmd == "verify":
        verify_seal(file)
    elif cmd == "seal":
        add_seal(file)
