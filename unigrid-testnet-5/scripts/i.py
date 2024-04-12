import os
import sys
import subprocess
import urllib.request
import venv
import shutil
import tempfile

BASE_DIR = os.path.expanduser("~/.pax")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CHAIN_ID = "unigrid-testnet-5"
LOG_FILE = os.path.join(BASE_DIR, "paxd.log")
SERVICE_FILE = "/etc/systemd/system/paxd.service"
CONFIG_TOML = os.path.join(CONFIG_DIR, "config.toml")
     
ascii_art = r"""
 _   _ _   _ ___ ____ ____  ___ ____
| | | | \ | |_ _/ ___|  _ \|_ _|  _ \
| | | |  \| || | |  _| |_) || || | | |
| |_| | |\  || | |_| |  _ < | || |_| |
 \___/|_| \_|___\____|_| \_\___|____/
"""

# ANSI escape codes for colors
class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    ORANGE = '\033[38;5;208m'
    RESET = '\033[0m'

# Print the Paxd ASCII art
print(Colors.ORANGE + ascii_art + Colors.RESET)
print(Colors.ORANGE + " Copyright © 2021-2024 The Unigrid Foundation, UGD Software AB\n\n " + Colors.RESET)
# Example usage of colored text
print(Colors.GREEN + "Welcome to the Paxd Installation Script!" + Colors.RESET)
print(Colors.YELLOW + "This script will guide you through the setup process." + Colors.RESET)
print(Colors.CYAN + "\n")

def run_command(command, check=True):
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(Colors.RED + f"Error executing command: {command}\n{e.stderr}" + Colors.RESET)
            sys.exit(1)
        return e.stderr

def is_package_installed(package):
    dpkg_query_command = f"dpkg-query -W -f='${{Status}}' {package} 2>/dev/null | grep -c 'ok installed'"
    result = run_command(dpkg_query_command, check=False)
    return result.strip() == '1'

def install_python3_venv():
    print("The 'python3-venv' package is not installed. Trying to install it...")
    install_command = "sudo apt-get install -y python3-venv"
    run_command(install_command)
    print("'python3-venv' installed successfully.")

def is_command_available(command):
    return subprocess.run(f"command -v {command}", shell=True, stdout=subprocess.DEVNULL).returncode == 0

def install_package(package):
    run_command(f"sudo apt-get install -y {package}")

def install_python_packages(venv_dir, packages):
    pip_path = os.path.join(venv_dir, 'bin', 'pip')
    for package in packages:
        try:
            subprocess.check_call([pip_path, 'install', package])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")

def setup_virtual_environment(venv_dir):
    # Check for existing node data before creating the directory
    if os.path.isdir(BASE_DIR):
        reset_node = input("Node data found. Do you want to reset the node data? (yes/no): ")
        if reset_node.lower() == "yes":
            run_command(f"paxd comet unsafe-reset-all")
            print("Node data has been reset.")
    # Create the base directory if it doesn't exist
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    # Create the config directory if it doesn't exist
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in {venv_dir}...")
        try:
            venv.create(venv_dir, with_pip=True)
        except Exception as e:
            print(Colors.RED + f"Failed to create virtual environment: {e}" + Colors.RESET)
            sys.exit(1)
    else:
        print(f"Virtual environment already exists in {venv_dir}. Skipping creation.")

    # List of required Python packages
    required_packages = ["tomlkit", "requests"]

    # Install required packages
    install_python_packages(venv_dir, required_packages)

def run_python_script(venv_dir, script_content):
    python_path = os.path.join(venv_dir, 'bin', 'python')
    
    # Write the script content to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_script:
        temp_script.write(script_content)
        temp_script_path = temp_script.name

    # Run the temporary script using the Python interpreter from the virtual environment
    subprocess.run([python_path, temp_script_path], check=True)

    # Optionally, remove the temporary file after execution
    os.remove(temp_script_path)
    
def download_and_install_script(url, install_path):
    local_script_path = os.path.basename(url)
    urllib.request.urlretrieve(url, local_script_path)
    os.chmod(local_script_path, 0o755)  # Make the script executable

    # Use subprocess to move the file with sudo privileges
    destination_path = os.path.join(install_path, local_script_path)
    subprocess.run(["sudo", "mv", local_script_path, destination_path], check=True)

def create_or_update_service(service_file, service_content):
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(service_content)
        temp_filepath = temp_file.name

    # Move the temporary file to the desired location with sudo
    move_command = f"sudo mv {temp_filepath} {service_file}"
    run_command(move_command)
    
    # Reload and enable the service
    run_command("sudo systemctl daemon-reload")
    run_command(f"sudo systemctl enable {os.path.basename(service_file)}")
    # run_command(f"sudo systemctl start {os.path.basename(service_file)}")

def manage_paxd_command(command):
    run_command(f"manage_paxd {command}")

def cleanup_files(files):
    for file in files:
        try:
            os.remove(file)
            print(Colors.GREEN + f"Removed file: {file}" + Colors.RESET)
        except OSError as e:
            print(Colors.RED + f"Error deleting file {file}: {e.strerror}" + Colors.RESET)

def main_installation_script(venv_dir):
    script_content = """

import os
import subprocess
import sys
import tomlkit
import requests
import json
import hashlib

BASE_DIR = os.path.expanduser("~/.pax")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CHAIN_ID = "unigrid-testnet-5"
LOG_FILE = os.path.join(BASE_DIR, "paxd.log")
SERVICE_FILE = "/etc/systemd/system/paxd.service"
CONFIG_TOML = os.path.join(CONFIG_DIR, "config.toml")
VENV_DIR = r'{venv_dir}'
RESET = "\033[0m"
def run_command(command, check=True, show_output=False):
    try:
        if show_output:
            # Run the command without capturing its output
            result = subprocess.run(command, shell=True, check=check)
        else:
            # Run the command and capture its output
            result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not show_output:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Error executing command: {command}" + RESET)
            sys.exit(1)
        if not show_output:
            return e.stderr

# Remove log file if it exists
if os.path.isfile(LOG_FILE):
    os.remove(LOG_FILE)

# Download and install paxd
response = run_command('curl -s https://api.github.com/repos/unigrid-project/cosmos-daemon/releases/latest')
latest_release = json.loads(response)
assets = latest_release.get('assets', [])
for asset in assets:
    if 'paxd' in asset.get('name', ''):
        download_url = asset.get('browser_download_url', '')
        break
else:
    print("Error: Could not find the download URL for paxd." + RESET)
    sys.exit(1)

print(f"Downloading: {download_url}")
download_command = f"wget {download_url} -O paxd"
print(f"Download command: {download_command}")
run_command(download_command, show_output=True)

run_command("sudo chmod +x paxd")
run_command("sudo mv paxd /usr/local/bin/")

# Prompt for node name and initialize
node_name = input("Enter node name (moniker): ")
run_command(f"paxd init {node_name} --home=$HOME/.pax --chain-id={CHAIN_ID} --overwrite")

def update_toml_section(file_path, section, config_updates):
    with open(file_path, 'r+') as file:
        data = tomlkit.loads(file.read())

        # Make sure the section exists
        data[section] = data.get(section, {})
        for key, value in config_updates.items():
            data[section][key] = value

        file.seek(0)
        file.write(tomlkit.dumps(data))
        file.truncate()

# Ask the user if they want to enable state-sync or fast sync
enable_state_sync = input("Would you like to enable state-sync to get synced in minutes? (yes/no): ")

if enable_state_sync.lower() == "yes":
    latest_height_json = requests.get("https://rpc-testnet.unigrid.org/block").json()
    latest_height = int(latest_height_json['result']['block']['header']['height'])
    snapshot_interval = 1000
    additional_offset = 1000
    last_snapshot_height = (latest_height - additional_offset) - ((latest_height - additional_offset) % snapshot_interval)

    snapshot_info_json = requests.get(f"https://rpc-testnet.unigrid.org/block?height={last_snapshot_height}").json()
    snapshot_hash = snapshot_info_json['result']['block_id']['hash']

    statesync_config_updates = {
        "enable": "true",
        "rpc_servers": "tcp://207.180.254.48:26657,tcp://194.233.95.48:26657",
        "trust_height": str(last_snapshot_height),
        "trust_hash": snapshot_hash,
        "trust_period": "168h0m0s",
        "discovery_time": "15s",
        "temp_dir": "",
        "chunk_request_timeout": "10s",
        "chunk_fetchers": "4"
    }

    update_toml_section(CONFIG_TOML, 'statesync', statesync_config_updates)

    print(f"State-sync has been enabled with height {last_snapshot_height} and hash {snapshot_hash}.")
else:
    print("State-sync not enabled. Continuing with regular sync.")

# Install jq
run_command("sudo apt-get install jq")

# Download and verify genesis.json
genesis_url = "https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-5/genesis/genesis.json"
run_command(f"wget -O genesis.json {genesis_url}")

checksum_url = "https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-5/genesis/sha256sum.txt"
run_command(f"wget -O sha256sum.txt {checksum_url}")

with open('sha256sum.txt', 'r') as f:
    checksum_expected = f.read().strip().split()[0]

checksum_actual = hashlib.sha256(open('genesis.json', 'rb').read()).hexdigest()

if checksum_expected == checksum_actual:
    # Move the genesis.json to the CONFIG_DIR
    genesis_destination = os.path.join(CONFIG_DIR, 'genesis.json')
    shutil.move('genesis.json', genesis_destination)
    print("genesis.json moved to " + genesis_destination)
else:
    print("Checksum verification failed!" + RESET)
    exit(1)
"""

    return script_content

    
if __name__ == "__main__":
    # Check and install python3-venv if necessary
    if not is_package_installed("python3-venv"):
        install_python3_venv()

    # Check for pip3, sudo, and python3
    if not is_command_available("pip3"):
        print("pip3 is not installed. Installing python3-pip...")
        install_package("python3-pip")
        print("python3-pip installed successfully.")

    if not is_command_available("sudo"):
        response = input("sudo is required to run this script. Would you like to install sudo? (yes/no): ")
        if response.lower() == "yes":
            print("Installing sudo. Please enter your password if prompted.")
            run_command("su -c 'apt-get update && apt-get install sudo'")
            print("sudo installed successfully.")
        else:
            print(Colors.RED + "sudo is required to run this script. Exiting." + Colors.RESET)
            sys.exit(1)

    if not is_command_available("python3"):
        py_response = input("Would you like to install Python 3? (yes/no): ")
        if py_response.lower() == "yes":
            print("Installing Python 3. This may require your password.")
            install_package("python3")
            print("Python 3 installed successfully.")
        else:
            print(Colors.RED + "Python 3 is required to run this script. Exiting." + Colors.RESET)
            sys.exit(1)

    # Setup virtual environment and install required Python packages
    venv_dir = os.path.expanduser('~/.pax/venv')
    setup_virtual_environment(venv_dir)
    os.environ["PATH"] = os.path.join(venv_dir, "bin") + os.pathsep + os.environ["PATH"]

    # Execute the main installation script in the virtual environment
    run_python_script(venv_dir, main_installation_script(venv_dir))

    # Service setup and additional script installation
    service_file = "/etc/systemd/system/paxd.service"
    service_content = """[Unit]
Description=Unigrid Paxd Service
After=network.target

[Service]
User={0}
ExecStart=/usr/local/bin/paxd start --hedgehog=https://207.180.254.48:39886 --p2p.seeds "96de577a45c68d8d539236334eb097515b63c70a@207.180.254.48:26656,fe420bfcff68beff824d9777bfe6ce1aa4cf8f43@149.102.133.13:26656,06ed85d8b34ca3a4275072894fc297dce416b708@194.233.95.48:26656"
Restart=always
RestartSec=3
StandardOutput=file:{1}/.pax/paxd.log
StandardError=file:{1}/.pax/paxd-error.log

[Install]
WantedBy=multi-user.target""".format(os.getenv("USER"), os.getenv("HOME"))
    create_or_update_service(service_file, service_content)

    install_manager_script_url = "https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-5/scripts/manage_paxd"
    download_and_install_script(install_manager_script_url, "/usr/local/bin")
    # start the paxd service
    manage_paxd_command("restart")

    # Clean up files after the installation
    files_to_cleanup = ['i.py', 'genesis.json', 'sha256sum.txt']
    cleanup_files(files_to_cleanup)
    # Print the Paxd ASCII art
    print(Colors.ORANGE + ascii_art + Colors.RESET)
    print(Colors.ORANGE + " Copyright © 2021-2024 The Unigrid Foundation, UGD Software AB\n\n " + Colors.RESET)

    print(Colors.GREEN + "Paxd has been installed successfully and started.\n\n" + Colors.RESET)
    print(Colors.YELLOW + "You can manage the Paxd service using the 'manage_paxd' command.\n" + Colors.RESET)
    print(Colors.YELLOW + "For example, to restart the Paxd service,  'manage_paxd restart' \n" + Colors.RESET)
    print(Colors.YELLOW + "To stop the service, 'manage_paxd stop'\n\n" + Colors.RESET)
    print(Colors.YELLOW + "You can check the Paxd log file using the 'tail -f $HOME/.pax/paxd.log' command:\n\n" + Colors.RESET)
    print(Colors.ORANGE + "For more information, visit https://docs.unigrid.org\n\n" + Colors.RESET)

