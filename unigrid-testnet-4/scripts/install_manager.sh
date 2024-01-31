#!/bin/sh

# wget -4qO- -o- raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/scripts/install_manager.sh | bash

# Define the URL of the script to download
SCRIPT_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/scripts/manage_paxd"

# Define the destination filename
DEST_FILENAME="/usr/local/bin/manage_paxd"

# Download the script
curl -o "$DEST_FILENAME" "$SCRIPT_URL"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download successful."
    # Make the script executable
    chmod +x "$DEST_FILENAME"
    echo "Script is now executable and located at $DEST_FILENAME"
else
    echo "Failed to download the script."
fi