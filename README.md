# Dell Fan Control for Dell R720xd Servers

## Overview
This project provides a customizable Python-based fan control solution for Dell R720xd servers, allowing users to control fan speeds dynamically based on server temperature readings. It’s ideal for reducing fan noise and optimizing cooling, especially in home lab environments.

## Features
- Automatic fan speed adjustment based on temperature thresholds.
- Configurable minimum, baseline, and maximum fan speeds.
- Manual fan speed option with temperature monitoring.
- Temperature logging for tracking and adjusting fan behavior.
- Flexible, easy-to-edit configuration through `config.ini`.

## Requirements
- **OS**: Tested on Ubuntu.
- **Hardware**: Designed for Dell R720xd server.
- **Software**: Python 3.x, ipmitool.

## Installation

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/dell_fan_control.git
cd dell_fan_control
```

### Step 2: Run the Setup Script
The provided setup script installs dependencies, copies files to their necessary locations, and sets up a systemd service to run the fan control script automatically on startup. Place install.sh, fan_control_service.py, config.ini, and ipmi_password.txt in the same directory
Run the setup script:
```bash
chmod +x install.sh
sudo ./setup.sh
```

### Step 3: Update Configuration
Edit the configuration file /opt/dell_fan_control/config.ini to match your server’s IP address and customize your temperature and fan speed settings. The script will use these settings to determine fan speeds dynamically.
```bash
sudo nano /opt/fan_control/config.ini
```

## Config File:
```ini
[ipmi]
ip = 192.168.1.3
username = fanuser
password_file = /opt/dell_fan_control/ipmi_password.txt
```

### Step 4: Start the Service
After installation, the setup script will start the fan control service automatically. You can manage it using these commands:
```bash
# To start the service
sudo systemctl start fan_control.service

# To stop the service
sudo systemctl stop fan_control.service

# To check the status of the service
sudo systemctl status fan_control.service
```

## Configuration
The config.ini file allows you to set IPMI parameters, temperature thresholds, fan speed limits, and more. Below are the available options:
```bash
[ipmi]
# The IP address of the IPMI server
ip = 192.168.0.3

# Username for IPMI access
username = fanuser

# Path to the file containing the IPMI password
password_file = /opt/fan_control/ipmi_password.txt

[fan_control]
# Fan speed to set when manual control is enabled (percentage)
manual_fan_speed = 15

# Maximum fan RPM value
max_rpm = 24000

# Minimum temperature threshold (°C) below which the fan will stay at baseline speed
min_temp = 30

# Baseline temperature (°C) for low-speed operation
baseline_temp = 45

# Baseline fan speed (percentage) when temperatures are below baseline
baseline_speed = 12

# Maximum temperature threshold (°C) where fan speed will increase proportionally
max_temp = 70

# Interval (in seconds) for updating temperature readings and adjusting fan speed
update_interval = 60

# Enable (true) or disable (false) automatic control mode
auto_control = true

# Set the logging level (INFO, DEBUG, etc.)
log_level = DEBUG

```

## Manual Installation

### Step 1: Clone the Repository and Navigate to the Directory
```bash
git clone https://github.com/MartianManBaby/dell_fan_control.git
cd dell_fan_control
```

### Step 2: Create Required Directories and Copy Files
- Create a directory for the fan control files:
```bash
sudo mkdir -p /opt/fan_control
```
- Copy the main Python Script and configuration file to this directory:
```bash
sudo cp fan_control_service.py /opt/fan_control/
sudo cp config.ini /opt/fan_control/
```

### Step 3: Set Up Permissions
- Set ownership of the /opt/fan_control directory to the user that will run the service (adjust fancontrol to your username or service account):
```bash
sudo chown -R fancontrol:fancontrol /opt/fan_control
```
- Ensure the Python script and configuration file are executable and readable:
```bash
sudo chmod 750 /opt/fan_control/fan_control_service.py
sudo chmod 640 /opt/fan_control/config.ini
```

### Step 4: Create the Password File
- The IPMI password is stored in a separate file for security. Create the file and set secure permissions:
- Create the password file:
```bash
sudo nano /opt/fan_control/ipmi_password.txt
```
- Enter your IPMI password in the file, then save and close the editor.
- Set ownership and permissions on the password file:
```bash
sudo chown fancontrol:fancontrol /opt/fan_control/ipmi_password.txt
sudo chmod 640 /opt/fan_control/ipmi_password.txt
```

### Step 5: Configure sudo Permissions
- To allow the script to run IPMI commands without requiring a password each time, edit the sudoers file
- Open the sudoers file for editing:
```bash
sudo visudo
```
- Add the following line, adjusting fancontrol to match the user account running the service:
```bash
fancontrol ALL=(ALL) NOPASSWD: /usr/bin/ipmitool
```

### Step 6: Set Up Systemd Service
- Copy the service file to the systemd directory:
```bash
sudo cp fan_control.service /etc/systemd/system/
```
- Reload the systemd daemon to recognize the new service:
```bash
sudo systemctl daemon-reload
```
- Enable the service to start at boot:
```bash
sudo systemctl enable fan_control.service
```

### Step 7: Configure the config.ini File
- Open the configuration file to customize your settings:
```bash
sudo nano /opt/fan_control/config.ini
```
- Adjust parameters as needed. Some key settings include:
```ini
IP Address (ip): The IP of your IPMI interface.
Username (username): IPMI user for access.
Baseline Temp (baseline_temp) and Baseline Speed (baseline_speed): Adjust to optimize fan speed based on temperature thresholds.
Max Temperature (max_temp): Set a maximum temperature to help control fan speed.
```

### Step 8: Start the Fan Control Service
- Start the fan control service:
```bash
sudo systemctl start fan_control.service
```
- Check the status to ensure it is running:
```bash
sudo systemctl status fan_control.service
```
Your fan control service should now be active. Logs for the service will be written to /opt/fan_control/fan_control.log, where you can monitor its operation and troubleshoot if necessary.

## Usage
After configuring the system, fan speeds will adjust automatically based on server temperatures as follows:

- **Auto-control mode**: Adjusts fan speed based on min_temp, baseline_temp, and max_temp.
- **Manual mode**: Fixes fan speed at manual_speed while continuing to monitor temperatures.
- You can switch between these modes by editing config.ini and restarting the service.

## Monitoring and Troubleshooting
To monitor fan control and temperature logs, use:
```bash
sudo journalctl -u fan_control.service
```

## If you encounter issues:
- Ensure ipmitool is installed and properly configured.
- Confirm IPMI settings (IP, username, password).
- Check log files for any error messages related to IPMI commands or temperature parsing.
- Check permissions for the fancontrol user and verify it can access the script, impitool, config, and password file
