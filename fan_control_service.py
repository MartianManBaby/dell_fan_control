import logging
import subprocess
import time
import configparser

# Set up logging
logging.basicConfig(
    filename='/opt/fan_control/fan_control.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load configuration
config = configparser.ConfigParser()
config.read('/opt/fan_control/config.ini')
ipmi_ip = config['ipmi']['ip']
username = config['ipmi']['username']
password_file = config['ipmi']['password_file']
max_rpm = int(config['fan_control']['max_rpm'])
min_temp = int(config['fan_control']['min_temp'])
baseline_temp = int(config['fan_control']['baseline_temp'])
baseline_speed = int(config['fan_control']['baseline_speed'])
max_temp = int(config['fan_control']['max_temp'])
update_interval = int(config['fan_control']['update_interval'])
auto_control = config['fan_control'].getboolean('auto_control')

# Initialize global variables
manual_fan_speed = None

# Helper function to run IPMI commands
def run_ipmi_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        logging.debug(f"Command output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e.stderr}")
        return None

# Parse temperature data from IPMI output
def retrieve_temperatures():
    command = f"sudo ipmitool -I lanplus -H {ipmi_ip} -U {username} -f {password_file} sdr type Temperature"
    output = run_ipmi_command(command)
    temperatures = []

    if output:
        for line in output.splitlines():
            try:
                # Extract only the numerical temperature value before "degrees"
                temp_str = line.split('|')[-1].strip()
                temp_value = int(temp_str.split()[0])  # Get the numeric part before "degrees"
                temperatures.append(temp_value)
                logging.debug(f"Temperature found: {temp_value}°C")
            except (IndexError, ValueError) as e:
                logging.error(f"Error parsing temperature: {line}")

    logging.info(f"Retrieved temperatures: {temperatures}")
    return temperatures

# Set fan speed via IPMI
def set_fan_speed(percentage):
    fan_speed_hex = format(int(percentage), 'x').zfill(2)
    command = f"sudo ipmitool -I lanplus -H {ipmi_ip} -U {username} -f {password_file} raw 0x30 0x30 0x02 0xff 0x{fan_speed_hex}"
    run_ipmi_command(command)
    logging.info(f"Fan speed set to {percentage}%")

# Fan control logic
def fan_control_loop():
    logging.info("Entering main fan control loop.")
    while True:
        temperatures = retrieve_temperatures()
        if not temperatures:
            logging.warning("No temperature data available.")
        else:
            max_temp_current = max(temperatures)
            logging.info(f"Max current temperature: {max_temp_current}°C")

            if manual_fan_speed is not None:
                set_fan_speed(manual_fan_speed)
                logging.info(f"Manual control: Fan speed set to {manual_fan_speed}%")
            elif auto_control:
                # Determine fan speed based on current temperature
                if max_temp_current < baseline_temp:
                    fan_speed = max(baseline_speed, 10)  # Minimum of 10% for quiet operation
                elif max_temp_current < max_temp:
                    fan_speed = min(baseline_speed + ((max_temp_current - baseline_temp) / (max_temp - baseline_temp)) * (100 - baseline_speed), 100)
                else:
                    fan_speed = 100

                set_fan_speed(fan_speed)
                logging.info(f"Auto-control: Fan speed adjusted to {fan_speed}%")

        time.sleep(update_interval)

if __name__ == "__main__":
    logging.info("Starting Fan Control Service Initialization...")
    logging.debug(f"Settings - IP: {ipmi_ip}, Max RPM: {max_rpm}, Min Temp: {min_temp}, Baseline Temp: {baseline_temp}, Baseline Speed: {baseline_speed}, Max Temp: {max_temp}, Update Interval: {update_interval}, Auto Control: {auto_control}")
    fan_control_loop()
