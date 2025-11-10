import time

def modexp(b, e, m):
    """Fast modular exponentiation using binary method"""
    r = 1
    b = b % m
    while e > 0:
        if e % 2 == 1:
            r = (r * b) % m
        e = e // 2
        b = (b * b) % m
    return r

if __name__ == "__main__":
    # Read public key
    try:
        with open("data.txt", "r") as f:
            n, e = map(int, f.readline().split())
        print(f"Loaded public key: (n={n}, e={e})")
    except FileNotFoundError:
        print("Error: data.txt not found. Run receiver first!")
        exit()

    time1 = time.perf_counter()

    while True:
        m = int(input(f"\nEnter the number to encrypt (must be less than {n}): "))
        if 0 <= m < n:
            break
        else:
            print(f"Error: Message must be between 0 and {n-1}. Try again!")

    c = modexp(m, e, n)
    print(f"\nCiphertext = {c}")

    # Append ciphertext to data.txt
    with open("data.txt", "a") as f:
        f.write(f"{c}\n")

    print("\n[+] Ciphertext saved to data.txt successfully!")
    print("Encryption complete.", time.perf_counter() - time1, "seconds")