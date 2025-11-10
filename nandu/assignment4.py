def mod_exp(b, e, m):
    return pow(b, e, m)


def main():
    p = int(input("Enter prime p: "))
    g = int(input("Enter generator g: "))
    a = int(input("Enter A's private key: "))
    b = int(input("Enter B's private key: "))
    c = int(input("Enter C's private key: "))

    A_pub = mod_exp(g, a, p)
    B_pub = mod_exp(g, b, p)
    C_pub = mod_exp(g, c, p)

    while True:
        print("\n1 Exchange Public Keys between A and B")
        print("2 Perform Man-In-The-Middle Attack by C")
        print("3 Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            print(f"A's Public Key: {A_pub}")
            print(f"B's Public Key: {B_pub}")
            S_A = mod_exp(B_pub, a, p)
            S_B = mod_exp(A_pub, b, p)
            print(f"A computes shared secret: {S_A}")
            print(f"B computes shared secret: {S_B}")
            if S_A == S_B:
                print("Secure communication established.")
            else:
                print("Shared secrets do not match!")

        elif choice == "2":
            print(f"A's Public Key (sent): {A_pub}")
            print(f"B's Public Key (sent): {B_pub}")
            print(f"C intercepts and sends its Public Key to both parties: {C_pub}")

            # A and B each derive a secret thinking it's with the other, but it's with C
            S_A = mod_exp(C_pub, a, p)  # secret A shares with C
            S_B = mod_exp(C_pub, b, p)  # secret B shares with C
            print(f"A computes shared secret with C: {S_A}")
            print(f"B computes shared secret with C: {S_B}")

            # C computes secrets with A and B using their original public keys
            S_C_A = mod_exp(A_pub, c, p)
            S_C_B = mod_exp(B_pub, c, p)
            print(f"C computes shared secret with A: {S_C_A}")
            print(f"C computes shared secret with B: {S_C_B}")

            if S_A == S_C_A and S_B == S_C_B:
                print("Man-In-The-Middle attack successful. C can intercept and modify messages.")
            else:
                print("MITM attack failed!")

        elif choice == "3":
            print("Exiting.")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
