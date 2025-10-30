#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise SystemExit("SECRET_KEY not found in .env")

# si la clé est stockée en base64 déjà encodée, on l'utilise telle quelle
cipher = Fernet(SECRET_KEY.encode() if isinstance(SECRET_KEY, str) else SECRET_KEY)

def enc(s):
    if s is None:
        s = ""
    return cipher.encrypt(s.encode()).decode()

# --- Remplis ici tes valeurs en clair ---
user = "administrateur"
password = "progtr00"

print("  '{0}',".format(enc(user)))
print("  '{0}',".format(enc(password)))
