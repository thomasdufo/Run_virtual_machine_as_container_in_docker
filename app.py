from flask import Flask, render_template, request, redirect, url_for, flash
import docker
import mysql.connector as MC
from dotenv import load_dotenv
import os
import time
from cryptography.fernet import Fernet


load_dotenv() # upload environment varible : .env


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


SECRET_KEY = os.getenv("SECRET_KEY").encode() # recuperation de la cle secrete depuis le fichier .env



cipher = Fernet(SECRET_KEY) # Initialiser l'instance de Fernet pour le chiffrement/déchiffrement


client = docker.from_env() # connect to docker 

# internal port for image
WEB_PORTS = {
    "ubuntu-desktop": 80,
    "ubuntu-desktop-wireshark": 80,
    "kali": 8080,
    "ubuntu-server": 8080
}




# Chiffrer une donnée
def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

# Déchiffrer une donnée
def decrypt_data(data):
    return cipher.decrypt(data.encode()).decode()


# Fonction pour attendre que la base de données soit prête
def connect_db():
    for i in range(10):  # Essayer jusqu'à 10 fois
        try:
            connection = MC.connect(
                host="mysql",
                user=decrypt_data('gAAAAABpAzkleB5qvJb9Ig8oc-zTcQzNP3qooXD4nVD5GTtXXnygT6wkG5-a96aEp_3gAmTGspofdhx8VXFp_zZWFsDGixmjkA=='),
                password=decrypt_data('gAAAAABpAzklPoLY6Tgfj2aVqC66DuIL7ozhQzhdtXCqz-5ORVF_1oR-XttzoVMCKkou9fZNpuwGxzq60L-7pNNgicE3NPORzw=='),
                database="project_web_site"
            )
            print("Connexion réussie à la base de données !")
            return connection
        except MC.Error as e:
            print(f"Tentative {i+1}/10 : MySQL pas encore prêt ({e}), attente...")
            time.sleep(3)  # Attendre 3 secondes avant de réessayer
    return None  # Si échec après 10 tentatives

connection = connect_db()


@app.route("/")
def index():
    # autorised image
    ALLOWED_IMAGES = [
        "kali:latest",
        "ubuntu-desktop:latest",
        "ubuntu-desktop-wireshark:latest",
        "ubuntu-server:latest"
    ]

    # find ip adrress of browser
    server_ip = request.host.split(":")[0]

    # 🔹 Liste filtrée des images locales
    images = []
    for img in client.images.list():
        if img.tags:
            for tag in img.tags:
                if tag in ALLOWED_IMAGES:
                    images.append(tag)

    # 🔹 Liste filtrée des conteneurs associés à ces images
    containers = []
    for c in client.containers.list(all=True):
        c.reload()
        img_tag = c.image.tags[0] if c.image.tags else c.image.id
        if img_tag in ALLOWED_IMAGES:
            ports = c.attrs["NetworkSettings"]["Ports"] or {}
            bindings = {k: v[0]["HostPort"] for k, v in ports.items() if v}
            containers.append({
                "id": c.short_id,
                "name": c.name,
                "image": img_tag,
                "status": c.status,
                "ports": bindings
            })

    return render_template(
        "index.html",
        images=images,
        containers=containers,
        web_ports=WEB_PORTS,
        server_ip=server_ip
    )

@app.route("/deploy/<image_name>", methods=["POST"])
def deploy(image_name):
    container_name = request.form["container_name"]
    try:
        container = client.containers.run(
            image_name,
            name=container_name,
            detach=True,
            ports={WEB_PORTS.get(image_name.split(":")[0], 80): None},
            stdin_open=True,
            tty=True
        )
        container.reload()
        port_bindings = container.attrs["NetworkSettings"]["Ports"]
        assigned_ports = {k: v[0]["HostPort"] for k, v in port_bindings.items() if v}
        flash(f"Conteneur '{container_name}' déployé sur {assigned_ports}", "success")
    except Exception as e:
        flash(f"Erreur : {str(e)}", "danger")
    return redirect(url_for("index"))

@app.route("/start/<container_id>")
def start(container_id):
    try:
        c = client.containers.get(container_id)
        c.start()
        flash(f"{c.name} démarré", "success")
    except Exception as e:
        flash(f"Erreur : {str(e)}", "danger")
    return redirect(url_for("index"))

@app.route("/stop/<container_id>")
def stop(container_id):
    try:
        c = client.containers.get(container_id)
        c.stop()
        flash(f"{c.name} arrêté", "info")
    except Exception as e:
        flash(f"Erreur : {str(e)}", "danger")
    return redirect(url_for("index"))

@app.route("/remove/<container_id>")
def remove(container_id):
    try:
        c = client.containers.get(container_id)
        c.remove(force=True)
        flash(f"{c.name} supprimé", "warning")
    except Exception as e:
        flash(f"Erreur : {str(e)}", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

