from cryptography.fernet import Fernet

# 1️⃣ Generate a key (do this once and store it safely)
key = Fernet.generate_key()
print("Encryption Key:", key.decode())

# 2️⃣ Create a Fernet instance
cipher = Fernet(key)

# 3️⃣ Encrypt some text
text = "Secret message"
encrypted_text = cipher.encrypt(text.encode())
print("Encrypted:", encrypted_text.decode())

# 4️⃣ Decrypt the text
decrypted_text = cipher.decrypt(encrypted_text).decode()
print("Decrypted:", decrypted_text)
