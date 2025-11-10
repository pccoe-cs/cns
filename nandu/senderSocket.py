import socket
import time


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


def main():
    try:
        # Create socket and connect to receiver
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 65433))
        print("Sender: Requesting public key from receiver...")

        # Receive public key (e, n) from receiver
        key_data = s.recv(1024).decode('utf-8').strip()
        parts = key_data.split(',')
        e = int(parts[0])
        n = int(parts[1])
        print(f"Sender: Received public key (e={e}, n={n}) from receiver")

        # Input plaintext with validation
        while True:
            try:
                plaintext = int(input(f"Sender: Enter integer plaintext to encrypt (0 < plaintext < {n}): "))
                if 0 < plaintext < n:
                    break
                print("Invalid input, please try again.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        # Encrypt the plaintext
        start_time = time.perf_counter()
        cipher = modexp(plaintext, e, n)
        encryption_time = time.perf_counter() - start_time

        print(f"Sender: Ciphertext is: {cipher}")
        print(f"Encryption Time is: {encryption_time:.6f} seconds")

        # Send ciphertext to receiver
        s.sendall(str(cipher).encode('utf-8'))
        print("Sender: Ciphertext is sent to receiver")

        # Close connection
        s.close()

    except ConnectionRefusedError:
        print("Error: Could not connect to receiver. Make sure receiver is running first!")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()