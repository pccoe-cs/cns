import random


class MonoalphabeticCipher:
    """
    A class to perform monoalphabetic substitution cipher encryption and decryption."""
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.forward_mapping = self._generate_mapping()
        self.backward_mapping = {v: k for k, v in self.forward_mapping.items()}

    def _generate_mapping(self):
        shuffled = list(self.alphabet)
        random.shuffle(shuffled)
        return dict(zip(self.alphabet, shuffled))

    def encrypt(self, plaintext):
        plaintext = plaintext.upper()
        ciphertext = ''.join(self.forward_mapping.get(char, char) for char in plaintext)
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.upper()
        plaintext = ''.join(self.backward_mapping.get(char, char) for char in ciphertext)
        return plaintext
    
class CaesarCipher:
    """
    A class to perform Caesar cipher encryption and decryption with a fixed shift of 3."""
    def __init__(self, shift=3):
        self.shift = shift
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def encrypt(self, plaintext):
        plaintext = plaintext.upper()
        ciphertext = ''
        for char in plaintext:
            if char in self.alphabet:
                index = (self.alphabet.index(char) + self.shift) % len(self.alphabet)
                ciphertext += self.alphabet[index]
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.upper()
        plaintext = ''
        for char in ciphertext:
            if char in self.alphabet:
                index = (self.alphabet.index(char) - self.shift) % len(self.alphabet)
                plaintext += self.alphabet[index]
            else:
                plaintext += char
        return plaintext

class VigenereCipher:
    """
    A class to perform Vigenère cipher encryption and decryption."""
    def __init__(self, key):
        self.key = key.upper()
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def _extend_key(self, length):
        repeats = length // len(self.key) + 1
        return (self.key * repeats)[:length]

    def encrypt(self, plaintext):
        plaintext = plaintext.upper()
        extended_key = self._extend_key(len(plaintext))
        ciphertext = ''
        for p_char, k_char in zip(plaintext, extended_key):
            if p_char in self.alphabet:
                p_index = self.alphabet.index(p_char)
                k_index = self.alphabet.index(k_char)
                c_index = (p_index + k_index) % len(self.alphabet)
                ciphertext += self.alphabet[c_index]
            else:
                ciphertext += p_char
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.upper()
        extended_key = self._extend_key(len(ciphertext))
        plaintext = ''
        for c_char, k_char in zip(ciphertext, extended_key):
            if c_char in self.alphabet:
                c_index = self.alphabet.index(c_char)
                k_index = self.alphabet.index(k_char)
                p_index = (c_index - k_index) % len(self.alphabet)
                plaintext += self.alphabet[p_index]
            else:
                plaintext += c_char
        return plaintext
    
class RailFenceCipher:
    """
    A class to perform Rail Fence cipher encryption and decryption."""
    def __init__(self, num_rails):
        self.num_rails = num_rails

    def encrypt(self, plaintext):
        rails = ['' for _ in range(self.num_rails)]
        rail = 0
        direction = 1

        for char in plaintext:
            rails[rail] += char
            rail += direction
            if rail == 0 or rail == self.num_rails - 1:
                direction *= -1

        return ''.join(rails)

    def decrypt(self, ciphertext):
        rail_lengths = [0] * self.num_rails
        rail = 0
        direction = 1

        for char in ciphertext:
            rail_lengths[rail] += 1
            rail += direction
            if rail == 0 or rail == self.num_rails - 1:
                direction *= -1

        rails = []
        index = 0
        for length in rail_lengths:
            rails.append(ciphertext[index:index + length])
            index += length

        result = []
        rail_indices = [0] * self.num_rails
        rail = 0
        direction = 1

        for _ in range(len(ciphertext)):
            result.append(rails[rail][rail_indices[rail]])
            rail_indices[rail] += 1
            rail += direction
            if rail == 0 or rail == self.num_rails - 1:
                direction *= -1

        return ''.join(result)

class VernamCipher:
    """
    A class to perform Vernam cipher encryption and decryption using XOR."""
    def __init__(self, key):
        self.key = key

    def _vernam(self, txt, key):
        """XOR-based Vernam cipher - works for both encrypt and decrypt."""
        result = ""
        for i in range(len(txt)):
            result += chr(ord(txt[i]) ^ ord(key[i]))
        return result

    def encrypt(self, plaintext):
        # Extend key to match plaintext length if needed
        if len(self.key) < len(plaintext):
            repeats = len(plaintext) // len(self.key) + 1
            extended_key = (self.key * repeats)[:len(plaintext)]
        else:
            extended_key = self.key
        return self._vernam(plaintext, extended_key)

    def decrypt(self, ciphertext):
        # XOR is self-inverse, so decryption uses same function
        if len(self.key) < len(ciphertext):
            repeats = len(ciphertext) // len(self.key) + 1
            extended_key = (self.key * repeats)[:len(ciphertext)]
        else:
            extended_key = self.key
        return self._vernam(ciphertext, extended_key)
    
if __name__ == "__main__":
    choice = input("Choose a cipher:\n1. Monoalphabetic Cipher\n2. Caesar Cipher\n3. Vigenère Cipher\n4. Rail Fence Cipher\n5. Vernam Cipher\n")
    plaintext = input("Enter the plaintext: ")
    if choice == '1':
        cipher = MonoalphabeticCipher()
        print("Encrypted:", cipher.encrypt(plaintext))
        print("Decrypted:", cipher.decrypt(cipher.encrypt(plaintext)))
    elif choice == '2':
        cipher = CaesarCipher()
        print("Encrypted:", cipher.encrypt(plaintext))
        print("Decrypted:", cipher.decrypt(cipher.encrypt(plaintext)))
    elif choice == '3':
        key = input("Enter the key for Vigenère Cipher: ")
        cipher = VigenereCipher(key)
        print("Encrypted:", cipher.encrypt(plaintext))
        print("Decrypted:", cipher.decrypt(cipher.encrypt(plaintext)))
    elif choice == '4':
        num_rails = int(input("Enter the number of rails for Rail Fence Cipher: "))
        cipher = RailFenceCipher(num_rails)
        print("Encrypted:", cipher.encrypt(plaintext))
        print("Decrypted:", cipher.decrypt(cipher.encrypt(plaintext)))
    elif choice == '5':
        key = input("Enter the key for Vernam Cipher (same length as plaintext): ")
        cipher = VernamCipher(key)
        print("Encrypted:", cipher.encrypt(plaintext))
        print("Decrypted:", cipher.decrypt(cipher.encrypt(plaintext)))
    else:
        print("Invalid choice.")
        exit()