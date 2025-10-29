from flask import Flask, render_template, request, redirect, url_for, flash
import docker

app = Flask(__name__)
app.secret_key = "supersecret"
client = docker.from_env()

# 🔹 Ports internes utilisés pour chaque image
WEB_PORTS = {
    "ubuntu-desktop": 80,
    "ubuntu-desktop-wireshark": 80,
    "kali": 8080,
    "ubuntu-server": 8080
}

@app.route("/")
def index():
    # 🔹 Images autorisées
    ALLOWED_IMAGES = [
        "kali:latest",
        "ubuntu-desktop:latest",
        "ubuntu-desktop-wireshark:latest",
        "ubuntu-server:latest"
    ]

    # 🔹 On récupère l'adresse IP utilisée par le navigateur
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

