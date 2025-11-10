import hashlib

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

def main():
    print("=== Simple SHA-1 Demo ===\n")
    msg = input("Enter message to send: ")
    digest = sha1(msg)
    print("\n[SENDER] Message: {}".format(msg))
    print("[SENDER] SHA-1 digest: {}".format(digest))
    received = msg
    recvd_digest = sha1(received)
    print("\n[RECEIVER] Received message: {}".format(received))
    print("[RECEIVER] Recomputed digest: {}".format(recvd_digest))
    if recvd_digest == digest:
        print("\nResult: Hashes match — integrity verified.")
    else:
        print("\nResult: Hash mismatch — message altered or corrupted.")
    print("\nNow demonstrating tampering: sender digest remains {}".format(digest))
    tampered = list(received)
    if len(tampered) > 0:
        tampered[0] = chr(ord(tampered[0]) ^ 0x01)
        tampered = ''.join(tampered)
        print("[ATTACKER] Tampered message: {}".format(tampered))
        print("[RECEIVER] Digest of tampered: {}".format(sha1(tampered)))
        print("=> Different digest shows tampering detected.")

if __name__ == "__main__":
    main()