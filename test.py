#!/usr/bin/env python3
import requests
import json

PORTAINER_URL = "http://127.0.0.1:9000"
USERNAME = "admin"
PASSWORD = "progtr000000"

# Authentification
resp = requests.post(f"{PORTAINER_URL}/api/auth",
                     json={"Username": USERNAME, "Password": PASSWORD})
resp.raise_for_status()
token = resp.json()["jwt"]
headers = {"Authorization": f"Bearer {token}"}

# Récupération des custom templates
resp = requests.get(f"{PORTAINER_URL}/api/custom_templates", headers=headers)
resp.raise_for_status()
templates = resp.json()

print("Nombre de templates:", len(templates))
for t in templates:
    print("="*50)
    print(json.dumps(t, indent=4))

