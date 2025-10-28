# Base : image Kali officielle
FROM kalilinux/kali-rolling

USER root

# Mise à jour + installation du bureau XFCE + VNC + noVNC
RUN apt update && \
    apt install -y xfce4 xfce4-goodies novnc websockify tightvncserver dbus-x11 sudo net-tools curl wget vim && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur standard
RUN useradd -m -s /bin/bash kali && echo "kali:kali" | chpasswd && adduser kali sudo

# Copier le script de démarrage
COPY startup.sh /usr/local/bin/startup.sh
RUN chmod +x /usr/local/bin/startup.sh

# Variables d'environnement
ENV USER=administrateur
ENV PASSWORD=progtr00
ENV VNC_PASSWORD=progtr00
ENV DISPLAY=:1

# Ports : 5900 (VNC) et 8080 (noVNC)
EXPOSE 5900 8080

# Script de démarrage
CMD ["/usr/local/bin/startup.sh"]
