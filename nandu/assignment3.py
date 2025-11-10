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
    

class RailThenMonoCipher:
    """
    Composite cipher that first applies Rail Fence, then Monoalphabetic substitution.
    Encryption:  RailFence.encrypt -> Mono.encrypt
    Decryption: Mono.decrypt -> RailFence.decrypt
    """
    def __init__(self, rails: int = 3):
        self.rail = RailFenceCipher(rails)
        self.mono = MonoalphabeticCipher()

    def encrypt(self, plaintext: str) -> str:
        # Step 1: Rail fence
        after_rail = self.rail.encrypt(plaintext)
        # Step 2: Monoalphabetic substitution (will uppercase)
        after_mono = self.mono.encrypt(after_rail)
        return after_mono

    def decrypt(self, ciphertext: str) -> str:
        # Step 1: Monoalphabetic decryption (produces uppercase text)
        after_mono = self.mono.decrypt(ciphertext)  
        # Step 2: Rail fence decryption
        after_rail = self.rail.decrypt(after_mono)
        return after_rail


if __name__ == "__main__":
    rail_then_mono_cipher = RailThenMonoCipher(rails=3)

    input_text = "HELLO WORLD THIS IS A TEST MESSAGE"
    ciphertext = rail_then_mono_cipher.encrypt(input_text)  
    print(rail_then_mono_cipher.decrypt(ciphertext))