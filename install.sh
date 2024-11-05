#!/bin/bash

echo "Starting Dell Fan Control installation..."

# Step 1: Create necessary directories and set permissions
sudo mkdir -p /opt/fan_control
sudo chown $USER:$USER /opt/fan_control

# Step 2: Copy the fan control script and config files to /opt/fan_control
cp fan_control_service.py /opt/fan_control/
cp config.ini /opt/fan_control/

# Step 3: Prompt the user to enter their IPMI password
echo "Please enter the IPMI password (it will be saved in /opt/fan_control/ipmi_password.txt):"
read -s ipmi_password
echo "$ipmi_password" | sudo tee /opt/fan_control/ipmi_password.txt > /dev/null

# Secure the password file by setting appropriate permissions
sudo chmod 600 /opt/fan_control/ipmi_password.txt
echo "IPMI password saved securely."

# Step 4: Create a systemd service file for fan control
sudo tee /etc/systemd/system/fan_control.service > /dev/null <<EOL
[Unit]
Description=Fan Control Service for Dell R720xd
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/fan_control/fan_control_service.py
User=$USER
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Step 5: Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable fan_control.service
sudo systemctl start fan_control.service

echo "Installation complete. Fan Control Service is now running."
echo "You may want to update /opt/fan_control/config.ini to adjust settings as needed."
