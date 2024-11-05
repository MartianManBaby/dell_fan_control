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
The provided setup script installs dependencies, copies files to their necessary locations, and sets up a systemd service to run the fan control script automatically on startup.
Run the setup script:
```bash
sudo ./setup.sh
```

### Step 3: Update Configuration
Edit the configuration file /opt/dell_fan_control/config.ini to match your server’s IP address and customize your temperature and fan speed settings. The script will use these settings to determine fan speeds dynamically.
```ini
[ipmi]
ip = 192.168.1.3
username = root
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

## Configuring password_file
For security, the IPMI password is stored in a separate file specified in config.ini. Set this up by creating a file with the password in /opt/dell_fan_control/ipmi_password.txt:
```bash
echo 'YourIPMIPassword' | sudo tee /opt/dell_fan_control/ipmi_password.txt
sudo chmod 600 /opt/dell_fan_control/ipmi_password.txt
```

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
