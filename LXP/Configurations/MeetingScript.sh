#!/bin/bash
sudo apt update
sudo apt install apt-transport-https
sudo apt-add-repository universe
sudo apt update
sudo hostnamectl set-hostname <your_IP>
sudo curl -sL https://prosody.im/files/prosody-debian-packages.key -o /etc/apt/keyrings/prosody-debian-packages.key
echo "deb [signed-by=/etc/apt/keyrings/prosody-debian-packages.key] http://packages.prosody.im/debian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/prosody-debian-packages.list
sudo apt install lua5.2
curl -sL https://download.jitsi.org/jitsi-key.gpg.key | sudo sh -c 'gpg --dearmor > /usr/share/keyrings/jitsi-keyring.gpg'
echo "deb [signed-by=/usr/share/keyrings/jitsi-keyring.gpg] https://download.jitsi.org stable/" | sudo tee /etc/apt/sources.list.d/jitsi-stable.list
sudo apt update
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 10000/udp
sudo ufw allow 22/tcp
sudo ufw allow 3478/udp
sudo ufw allow 5349/tcp
sudo ufw enable
sudo ufw status verbose
sudo apt install jitsi-meet


# for uninstall
# https://github.com/jitsi/jitsi-meet/issues/2663

# Step 1
# apt-get --purge remove jitsi-meet jitsi-meet-prosody jitsi-meet-web jitsi-meet-web-config jicofo jitsi-videobridge

# step 2
# apt-get autoclean

# step 3
# apt-get --force-yes remove

# step 4
# apt-get install --reinstall dpkg

# step 5
# cd /var/lib/dpkg/info

# step 6
# sudo rm jitsi-meet-web-config.postinst

# for install
# https://jitsi.org/downloads/ubuntu-debian-installations-instructions/

# final
# https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-quickstart/
# use till below command
# sudo apt install jitsi-meet
