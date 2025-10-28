FROM ubuntu:latest

# Installer wget et tar
RUN apt update && apt install -y wget tar curl iputils-ping

# Télécharger la dernière release Gotty
RUN wget https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz -O /tmp/gotty.tar.gz \
    && tar -xzf /tmp/gotty.tar.gz -C /tmp \
    && mv /tmp/gotty /usr/local/bin/gotty \
    && chmod +x /usr/local/bin/gotty \
    && rm -rf /tmp/gotty*
    

# Lancer Gotty par défaut
CMD ["gotty", "--permit-write", "--port", "8080", "bash"]
