#!/bin/bash

# Check if paxd service exists and stop it if it does
if systemctl list-units --full --all | grep -Fq "paxd.service"; then
    sudo systemctl stop paxd.service
fi

# Base directories
BASE_DIR="$HOME/.unigrid-testnet-1"
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

# Edit priv_validator_state.json
JSON_FILE="$DATA_DIR/priv_validator_state.json"
echo '{
  "height": "0",
  "round": 0,
  "step": 0
}' > "$JSON_FILE"

# Download and verify genesis.json
GENESIS_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-1/genesis/genesis.json"
wget -O genesis.json $GENESIS_URL

CHECKSUM_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-1/genesis/sha256sum.txt"
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

# Start or enable paxd service
if systemctl list-units --full --all | grep -Fq "paxd.service"; then
    sudo systemctl start paxd.service
else
    # Initialize and enable paxd service if it doesn't exist
    sudo systemctl enable paxd.service
    sudo systemctl start paxd.service
fi

tail -f "$LOG_FILE"

echo "Script completed."
