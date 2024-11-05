#!/bin/bash

# Install necessary packages
echo "Installing ipmitool and python3..."
sudo apt update
sudo apt install -y ipmitool python3

# Create directory for fan control files
echo "Creating directory /opt/fan_control..."
sudo mkdir -p /opt/fan_control

# Copy Python script and configuration files to /opt/fan_control
echo "Copying files to /opt/fan_control..."
sudo cp fan_control_service.py /opt/fan_control/
sudo cp config.ini /opt/fan_control/
sudo touch /opt/fan_control/fan_control.log
sudo cp ipmi_password.txt /opt/fan_control/

# Set permissions and ownership
echo "Setting permissions..."
sudo chown -R root:root /opt/fan_control
sudo chmod -R 640 /opt/fan_control
sudo chmod 644 /opt/fan_control/config.ini
sudo chmod 644 /opt/fan_control/fan_control.log
sudo chmod 600 /opt/fan_control/ipmi_password.txt
sudo chmod +x /opt/fan_control/fan_control_service.py

# Create systemd service file
echo "Creating fan_control.service in /etc/systemd/system..."
cat <<EOT | sudo tee /etc/systemd/system/fan_control.service
[Unit]
Description=Fan Control Service for Dell R720xd
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/fan_control/fan_control_service.py
WorkingDirectory=/opt/fan_control
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOT

# Reload systemd, enable and start the service
echo "Reloading systemd daemon, enabling and starting fan_control.service..."
sudo systemctl daemon-reload
sudo systemctl enable fan_control.service
sudo systemctl start fan_control.service

# Prompt to edit config.ini
echo "Installation complete. Please edit /opt/fan_control/config.ini to configure IPMI settings and fan control preferences."
echo "Use 'sudo nano /opt/fan_control/config.ini' to edit the configuration file."

# Confirm service status
echo "Checking fan_control.service status..."
sudo systemctl status fan_control.service
