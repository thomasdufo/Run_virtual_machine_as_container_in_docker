#!/bin/bash
set -e

echo "=== Nettoyage des fichiers temporaires X et des verrous ==="
rm -f /tmp/.X*-lock
rm -rf /tmp/.X11-unix/X*

echo "=== Lancement du serveur VNC et de noVNC pour Kali XFCE ==="

service dbus start || true

mkdir -p /home/kali/.vnc
chown -R kali:kali /home/kali/.vnc

su - kali -c "bash -c 'echo \"$VNC_PASSWORD\" | vncpasswd -f > ~/.vnc/passwd'"
su - kali -c "chmod 600 ~/.vnc/passwd"

cat > /home/kali/.vnc/xstartup <<'XSU'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4
XSU

chown kali:kali /home/kali/.vnc/xstartup
chmod +x /home/kali/.vnc/xstartup

# Lancer le serveur VNC uniquement si aucun serveur Xtightvnc n'est actif
if ! pgrep Xtightvnc > /dev/null; then
    su - kali -c "vncserver :1 -geometry 1280x800 -depth 24"
else
    echo "VNC server already running"
fi

sleep 2
websockify --web=/usr/share/novnc/ --wrap-mode=ignore 8080 localhost:5901 &

echo "✅ noVNC disponible : http://localhost:8080/?password=$VNC_PASSWORD"

tail -f /dev/null

