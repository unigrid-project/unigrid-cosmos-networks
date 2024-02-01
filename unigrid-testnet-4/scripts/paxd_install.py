import os
import subprocess
import sys
import hashlib

def install_package(package):
    pip3_path = '/usr/bin/pip3'  # Specify the absolute path to pip3
    subprocess.check_call([pip3_path, "install", package])

# Check and install tomlkit and requests if they are not installed
try:
    import tomlkit
except ImportError:
    print("Installing tomlkit...")
    install_package("tomlkit")

try:
    import requests
except ImportError:
    print("Installing requests...")
    install_package("requests")
    
import requests

# Define constants
CHAIN_ID = "unigrid-testnet-4"
BASE_DIR = os.path.expanduser("~/.pax")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
LOG_FILE = os.path.join(BASE_DIR, "paxd.log")
SERVICE_FILE = "/etc/systemd/system/paxd.service"

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip()

# Check if the base directory exists
if os.path.isdir(BASE_DIR):
    reset_node = input("Node data found. Do you want to reset the node data? (yes/no): ")
    if reset_node.lower() == "yes":
        run_command("paxd comet unsafe-reset-all")
        print("Node data has been reset.")

# Remove log file if it exists
if os.path.isfile(LOG_FILE):
    os.remove(LOG_FILE)

# Download and install paxd
download_url = run_command("curl -s https://api.github.com/repos/unigrid-project/cosmos-daemon/releases/latest | grep 'browser_download_url.*paxd' | cut -d '\"' -f 4")
print(f"Downloading: {download_url}")
run_command(f"wget {download_url}")
run_command("chmod +x paxd")
run_command("sudo mv paxd /usr/local/bin/")

# Prompt for node name and initialize
node_name = input("Enter node name (moniker): ")
run_command(f"paxd init {node_name} --chain-id={CHAIN_ID} --overwrite")

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
CONFIG_TOML = os.path.join(CONFIG_DIR, "config.toml")

if enable_state_sync.lower() == "yes":
    latest_height_json = requests.get("https://rpc-testnet.unigrid.org/block").json()
    latest_height = int(latest_height_json['result']['block']['header']['height'])  # Convert to int
    snapshot_interval = 1000
    additional_offset = 1000
    last_snapshot_height = (latest_height - additional_offset) - ((latest_height - additional_offset) % snapshot_interval)

    snapshot_info_json = requests.get(f"https://rpc-testnet.unigrid.org/block?height={last_snapshot_height}").json()
    snapshot_hash = snapshot_info_json['result']['block_id']['hash']

    statesync_config_updates = {
        "enable": "true",
        "rpc_servers": "tcp://38.242.156.2:26657,tcp://194.233.95.48:26657",
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
genesis_url = "https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/genesis/genesis.json"
run_command(f"wget -O genesis.json {genesis_url}")

checksum_url = "https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/genesis/sha256sum.txt"
run_command(f"wget -O sha256sum.txt {checksum_url}")

with open('sha256sum.txt', 'r') as f:
    checksum_expected = f.read().strip().split()[0]

checksum_actual = hashlib.sha256(open('genesis.json', 'rb').read()).hexdigest()

if checksum_expected != checksum_actual:
    print("Checksum verification failed!")
    exit(1)


# Move genesis.json to the correct location
os.rename('genesis.json', os.path.join(CONFIG_DIR, 'genesis.json'))

print("Script completed.")