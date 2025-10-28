# Base image Ubuntu Desktop LXDE + VNC/noVNC
FROM dorowu/ubuntu-desktop-lxde-vnc:latest

USER root

# Supprimer le dépôt Google Chrome pour éviter l'erreur GPG
RUN rm -f /etc/apt/sources.list.d/google-chrome.list || true

# Mettre à jour et installer quelques utilitaires
RUN apt update && \
    apt install -y sudo vim net-tools curl wget && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Définir l'utilisateur par défaut et mot de passe (optionnel)
ENV USER=administrateur
ENV PASSWORD=progtr00

# Expose les ports VNC et noVNC
EXPOSE 5900 80

# Répertoire pour persistance
VOLUME ["/home/ubuntu"]

# Lancement par défaut
CMD ["/startup.sh"]

