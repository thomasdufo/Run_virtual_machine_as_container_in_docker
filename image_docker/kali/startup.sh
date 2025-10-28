#!/bin/bash
set -e

echo "=== Lancement du serveur VNC et de noVNC pour Kali XFCE ==="

# Démarrer dbus
service dbus start || true

# Créer le dossier .vnc et donner les bonnes permissions
mkdir -p /home/kali/.vnc
chown -R kali:kali /home/kali/.vnc

# Créer le mot de passe VNC pour l'utilisateur kali
su - kali -c "bash -c 'echo \"$VNC_PASSWORD\" | vncpasswd -f > ~/.vnc/passwd'"
su - kali -c "chmod 600 ~/.vnc/passwd"

# Créer xstartup pour XFCE
cat > /home/kali/.vnc/xstartup <<'XSU'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4
XSU

chown kali:kali /home/kali/.vnc/xstartup
chmod +x /home/kali/.vnc/xstartup

# Lancer le serveur VNC sur :1
su - kali -c "vncserver :1 -geometry 1280x800 -depth 24"

sleep 2

# Lancer websockify/noVNC
websockify --web=/usr/share/novnc/ --wrap-mode=ignore 8080 localhost:5901 &

# Afficher le lien direct pour connexion automatique
echo "✅ noVNC disponible (connexion directe) : http://localhost:8086/vnc_auto.html?host=localhost&port=8080&password=$VNC_PASSWORD"

# Garder le container vivant
tail -f /dev/null
