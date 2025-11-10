import socket
import time


def gcd(a, b):
    """Calculate Greatest Common Divisor using Euclidean algorithm"""
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    """Find modular multiplicative inverse of e mod phi"""
    for d in range(1, phi):
        if (d * e) % phi == 1:
            return d
    return 0


def modexp(base, exp, mod):
    """Fast modular exponentiation using binary method"""
    result = 1
    b = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * b) % mod
        b = (b * b) % mod
        exp = exp // 2
    return result


def is_prime(num):
    """Check if a number is prime"""
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def main():
    try:
        # Step 1: Generate RSA keys
        print("=== RSA Key Generation ===")
        
        while True:
            try:
                p = int(input("Enter first prime (p): "))
                q = int(input("Enter second prime (q): "))
                
                if not is_prime(p):
                    print(f"Error: {p} is not prime. Try again.")
                    continue
                if not is_prime(q):
                    print(f"Error: {q} is not prime. Try again.")
                    continue
                if p == q:
                    print("Error: p and q must be different. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter integers.")

        n = p * q
        phi = (p - 1) * (q - 1)

        # Choose e such that 1 < e < phi and gcd(e, phi) = 1
        e = 3
        while gcd(e, phi) != 1:
            e += 1

        # Compute d (modular inverse of e mod phi)
        d = mod_inverse(e, phi)

        print(f"\nGenerated Public Key: (e={e}, n={n})")
        print(f"Generated Private Key: (d={d}, n={n})")

        # Step 2: Setup socket server and send public key
        print("\n=== Starting Server ===")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", 65433))
        server_socket.listen(1)
        
        print("Receiver: Waiting for connection from Sender...")

        conn, addr = server_socket.accept()
        print(f"Receiver: Connected by {addr[0]}:{addr[1]}")

        # Send the public key (e, n)
        public_key = f"{e},{n}"
        conn.sendall(public_key.encode('utf-8'))
        print("Receiver: Public Key is sent to Sender")

        # Step 3: Receive ciphertext and decrypt
        cipher_str = conn.recv(1024).decode('utf-8').strip()
        cipher = int(cipher_str)
        print(f"Receiver: Ciphertext received: {cipher}")

        # Decrypt the ciphertext
        start_time = time.perf_counter()
        decrypted = modexp(cipher, d, n)
        decryption_time = time.perf_counter() - start_time

        print(f"Receiver: Decrypted Text is: {decrypted}")
        print(f"Decryption Time is: {decryption_time:.6f} seconds")

        # Close connections
        conn.close()
        server_socket.close()
        
        print("\n=== Session Complete ===")

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()