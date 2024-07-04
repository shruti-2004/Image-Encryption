from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_image(image_path, key):
    image = Image.open(image_path)
    image_bytes = image.tobytes()
    
    cipher = AES.new(key, AES.MODE_CBC)
    
    encrypted_bytes = cipher.encrypt(pad(image_bytes, AES.block_size))
    
    with open(image_path + ".enc", "wb") as f:
        f.write(cipher.iv)
        f.write(encrypted_bytes)
    
    hex_key = key.hex()
    print("Image encrypted and saved as " + image_path + ".enc")
    print("Key (save this for decryption):", hex_key)

def decrypt_image(encrypted_image_path, output_path):
    hex_key = input("Enter the decryption key: ")
    key = bytes.fromhex(hex_key)
    
    with open(encrypted_image_path, "rb") as f:
        iv = f.read(16)
        encrypted_bytes = f.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    
    original_image = Image.open(encrypted_image_path.replace(".enc", ""))
    mode = original_image.mode
    size = original_image.size
    
    decrypted_image = Image.frombytes(mode, size, decrypted_bytes)
    
    decrypted_image.save(output_path)
    
    print("Image decrypted and saved as " + output_path)

def generate_key():
    return os.urandom(16)

if __name__ == "__main__":
    image_path = "car.jpeg"
    
    key = generate_key()
    
    encrypt_image(image_path, key)
    
    decrypt_image(image_path + ".enc", "decrypted_image.jpeg")
