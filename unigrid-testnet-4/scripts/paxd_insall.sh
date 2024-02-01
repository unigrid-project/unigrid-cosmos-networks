#!/bin/bash

# to run this script
# bash -ic "$(wget -4qO- -o- raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/scripts/paxd_insall.sh)" ; source ~/.bashrc



# Define chain ID and base directory
CHAIN_ID="unigrid-testnet-4"
BASE_DIR="$HOME/.pax"
CONFIG_DIR="$BASE_DIR/config"
LOG_FILE="$BASE_DIR/paxd.log"
# Check if the base directory exists
if [ -d "$BASE_DIR" ]; then
    # Prompt user for a reset
    read -p "Node data found. Do you want to reset the node data? (yes/no): " reset_node

    if [[ $reset_node == "yes" ]]; then
        paxd comet unsafe-reset-all
        echo "Node data has been reset."
    fi
fi

# Remove log file if it exists
if [ -f "$LOG_FILE" ]; then
    rm -rf "$LOG_FILE"
fi

# Download and install paxd
DOWNLOAD_URL=$(curl -s https://api.github.com/repos/unigrid-project/cosmos-daemon/releases/latest | grep "browser_download_url.*paxd" | cut -d '"' -f 4)
echo "Downloading: $DOWNLOAD_URL"
wget $DOWNLOAD_URL
chmod +x paxd
sudo mv paxd /usr/local/bin/

# Prompt for node name and initialize
read -p "Enter node name (moniker): " NODE_NAME
paxd init "$NODE_NAME" --chain-id=$CHAIN_ID

# Ask the user if they want to enable state-sync or fast sync
read -p "Would you like to enable state-sync to get synced in minutes? (yes/no): " enable_state_sync

# Update config.toml with state-sync configuration
CONFIG_TOML="$BASE_DIR/config/config.toml"

if [[ $enable_state_sync == "yes" ]]; then
    # Fetch the latest block height and calculate the last snapshot height
    LATEST_HEIGHT_JSON=$(curl -s https://rpc-testnet.unigrid.org/block)
    LATEST_HEIGHT=$(echo $LATEST_HEIGHT_JSON | jq -r '.result.block.header.height')
    SNAPSHOT_INTERVAL=1000
    LAST_SNAPSHOT_HEIGHT=$((LATEST_HEIGHT - LATEST_HEIGHT % SNAPSHOT_INTERVAL))

    # Fetch the block hash for the last snapshot height
    SNAPSHOT_INFO_JSON=$(curl -s "https://rpc-testnet.unigrid.org/block?height=$LAST_SNAPSHOT_HEIGHT")
    SNAPSHOT_HASH=$(echo $SNAPSHOT_INFO_JSON | jq -r '.result.block_id.hash')

    # Define the new statesync configuration
    NEW_STATESYNC_CONFIG="enable = true
rpc_servers = \"tcp://38.242.156.2:26657,tcp://194.233.95.48:26657\"
trust_height = $LAST_SNAPSHOT_HEIGHT
trust_hash = \"$SNAPSHOT_HASH\"
trust_period = \"168h0m0s\"
discovery_time = \"15s\"
temp_dir = \"\"
chunk_request_timeout = \"10s\"
chunk_fetchers = \"4\""

    # Check if the statesync section exists and replace it
    if grep -q '^\[statesync\]' "$CONFIG_TOML"; then
        # Use sed to replace the statesync section
        sed -i "/^\[statesync\]/,/^\[.*\]/c\\$NEW_STATESYNC_CONFIG" "$CONFIG_TOML"
    else
        # If the statesync section doesn't exist, append it
        echo -e "\n$NEW_STATESYNC_CONFIG" >> "$CONFIG_TOML"
    fi

    echo "State-sync has been enabled with height $LAST_SNAPSHOT_HEIGHT and hash $SNAPSHOT_HASH."
else
    echo "State-sync not enabled. Continuing with regular sync."
fi

sudo apt-get install jq

# Download and verify genesis.json
GENESIS_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/genesis/genesis.json"
wget -O genesis.json $GENESIS_URL

CHECKSUM_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/genesis/sha256sum.txt"
wget -O sha256sum.txt $CHECKSUM_URL

CHECKSUM_EXPECTED=$(cat sha256sum.txt)
CHECKSUM_ACTUAL=$(sha256sum genesis.json | awk '{ print $1 }')

if [ "$CHECKSUM_EXPECTED" != "$CHECKSUM_ACTUAL" ]; then
    echo "Checksum verification failed!"
    exit 1
fi

# Move genesis.json to the correct location
mv genesis.json "$CONFIG_DIR/"

echo "Installing the manager script..."
bash -ic "$(wget -4qO- -o- raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/scripts/install_manager.sh)" ; source ~/.bashrc

# Check if paxd service file exists and create/update it
SERVICE_FILE="/etc/systemd/system/paxd.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "Updating paxd service configuration..."
else
    echo "Creating paxd service configuration..."
fi
echo "[Unit]
Description=Unigrid Paxd Service
After=network.target

[Service]
User=$USER
ExecStart=/usr/local/bin/paxd start --hedgehog=https://149.102.147.45:39886 --p2p.seeds \"8cc2192d6de0936632e0818c3b030a465a40d2dc@149.102.133.13:26656,06ed85d8b34ca3a4275072894fc297dce416b708@194.233.95.48:26656,e339ab8163a2774fccbc78ff09ffbf0991adc310@38.242.156.2:26656\"
Restart=always
RestartSec=3
StandardOutput=file:$HOME/.pax/paxd.log
StandardError=file:$HOME/.pax/paxd-error.log

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE

# Reload systemd, enable and start paxd service
sudo systemctl daemon-reload
sudo systemctl enable paxd.service
sudo systemctl start paxd.service

sleep 2
tail -f "$BASE_DIR/paxd.log"

echo "Script completed."