#!/usr/bin/env python3


import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Nom du fichier .env
ENV_FILE = ".env"

# Vérifier si le fichier .env existe déjà
if not os.path.exists(ENV_FILE):
    # Générer une nouvelle clé secrète
    secret_key = Fernet.generate_key().decode()

    # Écrire la clé dans .env
    with open(ENV_FILE, "w") as f:
        f.write(f"SECRET_KEY={secret_key}\n")

    print("Fichier .env créé avec une nouvelle clé secrète.")

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé secrète
SECRET_KEY = os.getenv("SECRET_KEY").encode()

# Initialiser Fernet
cipher = Fernet(SECRET_KEY)
