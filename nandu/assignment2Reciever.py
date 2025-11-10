import time

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(e, phi):
    for i in range(1, phi):
        if (e * i) % phi == 1:
            return i
    return None

def modexp(b, e, m):
    r = 1
    for i in range(e):
        r = (r * b) % m
    return r

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Generate keys
while True:
    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))
    if is_prime(p) and is_prime(q):
        break
    else:
        print("Both p and q must be prime numbers! Try again.\n")

n = p * q
phi = (p - 1) * (q - 1)
print(f"\nn = {n}, phi = {phi}")

while True:
    e = int(input("Enter e: "))
    if gcd(e, phi) == 1:
        break
    else:
        print("Invalid e! Try again.")

d = modinv(e, phi)
print(f"\nPublic key: (n={n}, e={e})")
print(f"Private key (d) = {d} - KEEP SECRET!")

# Save public key
with open("data.txt", "w") as f:
    f.write(f"{n} {e}\n")
print("\n[+] Public key saved to data.txt")

input("\nPress Enter after sender creates ciphertext...")

# Decrypt
try:
    time1 = time.perf_counter()
    with open("data.txt", "r") as f:
        lines = f.readlines()
        cipher = [int(x) for x in lines[1].split()]
    time2 = time.perf_counter()
    
    print("Received Ciphertext:", cipher)
    print("Decrypting...", time2 - time1, "seconds")
    print("\nDecrypted Message: ", end="")
    for c in cipher:
        m = modexp(c, d, n)
        print(m, end=" ")
    print()
except (FileNotFoundError, IndexError):
    print("Error: No ciphertext found in data.txt!")
    exit()