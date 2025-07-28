README for Q3 - Ransomware Script
==================================

Name: Sheethal Santhanam
UOW Student Number: 9996527

This Python script simulates a simple ransomware attack scenario.

HOW TO RUN:
-----------
1. Make sure 'my_secrets.txt' exists in the same folder.
   Example command to create it:
   echo 'This is a top secret.' > my_secrets.txt

2. Run the script using:
   python3 ransomware.py

WHAT IT DOES:
-------------
The script performs the following steps:
1. Generates a random 16-byte AES key and saves it to 'key.txt'
2. Generates a 2048-bit RSA key pair ('private.pem' and 'public.pem')
3. Encrypts the file 'my_secrets.txt' into 'data_cipher.txt' using AES
4. Encrypts the AES key using RSA public key, then base64-encodes it into 'key_cipher.txt'
5. Deletes 'key.txt' and 'my_secrets.txt'
6. Displays a ransom note on the screen

REQUIREMENTS:
-------------
- Tested on Kali Linux
- Requires OpenSSL installed (default in Kali)
- Python 3

FILES:
------
- ransomware.py         → Main Python script
- data_cipher.txt       → AES-encrypted victim file
- key_cipher.txt        → RSA-encrypted AES key (base64 format)
- private.pem / public.pem → RSA keys used for the encryption
