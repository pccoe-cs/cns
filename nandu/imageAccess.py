def _encrypt_image(input_path, output_path, shift):
    with open(input_path, "rb") as file:
        image_data = file.read()
    
    # Skip first 100 bytes (header) to keep file readable
    header_size = 100
    header = image_data[:header_size]
    data_to_encrypt = image_data[header_size:]
    
    encrypted_data = bytearray(header)  # Keep header intact
    
    for byte in data_to_encrypt:
        encrypted_data.append((byte + shift) % 256)
    
    with open(output_path, "wb") as file:
        file.write(encrypted_data)

def _decrypted_image(input_path, output_path, shift):
    with open(input_path, "rb") as file:
        image_data = file.read()
    
    # Skip first 100 bytes (header)
    header_size = 100
    header = image_data[:header_size]
    data_to_decrypt = image_data[header_size:]
    
    decrypted_image = bytearray(header)  # Keep header intact

    for byte in data_to_decrypt:
        decrypted_image.append((byte - shift) % 256)

    with open(output_path, "wb") as file:
        file.write(decrypted_image)

if __name__ == "__main__":
    print("started image encryption and decryption")

    image_path = input("enter image path:")
    shift = int(input("enter shift value for image caesar cipher:"))

    # Preserve original file extension
    import os
    _, ext = os.path.splitext(image_path)
    encrypted_path = f"encrypted_image{ext}"
    decrypted_path = f"decrypt_image{ext}"

    _encrypt_image(image_path, encrypted_path, shift)
    _decrypted_image(encrypted_path, decrypted_path, shift)

    print(f"Encrypted image saved as: {encrypted_path}")
    print(f"Decrypted image saved as: {decrypted_path}")