#!/bin/bash

# to run this script
# wget -4qO- -o- raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-devnet-1/scripts/pax_reset.sh | bash

# Check if paxd service exists and stop it if it does
if systemctl list-units --full --all | grep -Fq "paxd.service"; then
    sudo systemctl stop paxd.service
fi

# Base directories
BASE_DIR="$HOME/.pax"
DATA_DIR="$BASE_DIR/data"
CONFIG_DIR="$BASE_DIR/config"
LOG_FILE="$BASE_DIR/paxd.log"

# Create necessary directories if they don't exist
mkdir -p "$DATA_DIR"
mkdir -p "$CONFIG_DIR"

# Directories to remove
DIRS=("application.db" "blockstore.db" "cs.wal" "evidence.db" "snapshots" "state.db" "tx_index.db")

# Remove log file if it exists
if [ -f "$LOG_FILE" ]; then
    rm -rf "$LOG_FILE"
fi

# Remove data directories if they exist
for dir in "${DIRS[@]}"; do
    if [ -d "$DATA_DIR/$dir" ]; then
        rm -rf "$DATA_DIR/$dir"
    fi
done

JSON_FILE="$DATA_DIR/priv_validator_state.json"

sudo apt-get install jq

# Update the JSON file with new values for height, round, and step
jq '.height = "0" | .round = 0 | .step = 0' "$JSON_FILE" > temp.json && mv temp.json "$JSON_FILE"

# Download and verify genesis.json
GENESIS_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-devnet-1/genesis/genesis.json"
wget -O genesis.json $GENESIS_URL

CHECKSUM_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-devnet-1/genesis/sha256sum.txt"
wget -O sha256sum.txt $CHECKSUM_URL

CHECKSUM_EXPECTED=$(cat sha256sum.txt)
CHECKSUM_ACTUAL=$(sha256sum genesis.json | awk '{ print $1 }')

if [ "$CHECKSUM_EXPECTED" != "$CHECKSUM_ACTUAL" ]; then
    echo "Checksum verification failed!"
    exit 1
fi

# Move genesis.json to the correct location
mv genesis.json "$CONFIG_DIR/"

# Download and install paxd
DOWNLOAD_URL=$(curl -s https://api.github.com/repos/unigrid-project/cosmos-daemon/releases/latest | grep "browser_download_url.*paxd" | cut -d '"' -f 4)
echo "Downloading: $DOWNLOAD_URL"
wget $DOWNLOAD_URL
chmod +x paxd
sudo mv paxd /usr/local/bin/

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
ExecStart=/usr/local/bin/paxd start --hedgehog=https://173.212.208.212:40001 --p2p.seeds "cd5b5504e29dc48878c740eedd5b65088bb9df2b@173.212.208.212:26656,1d4612ebac1d5cf4a3874381264799772e17c7b5@149.102.147.45:26656"
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
tail -f "$LOG_FILE"

echo "Script completed."
