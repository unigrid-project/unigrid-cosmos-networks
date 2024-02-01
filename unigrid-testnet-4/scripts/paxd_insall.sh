#!/bin/bash

# to run this script
# bash -ic "$(wget -4qO- -o- raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/scripts/paxd_insall.sh)" ; source ~/.bashrc

# Define the URL of the Python script
PYTHON_SCRIPT_URL="https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/scripts/paxd_install.py"
PYTHON_SCRIPT_NAME="paxd_install.py"

# Download the Python script
wget "$PYTHON_SCRIPT_URL" -O "$PYTHON_SCRIPT_NAME"

# Check if sudo is installed
if ! command -v sudo &> /dev/null; then
    echo "sudo is not installed."
    read -p "sudo is required to run this script. Would you like to install sudo? (yes/no): " response

    if [[ "$response" == "yes" ]]; then
        echo "Installing sudo. Please enter your password if prompted."
        su -c 'apt-get update && apt-get install sudo'
        echo "sudo installed successfully."
    else
        echo "sudo is required to run this script. Exiting."
        exit 1
    fi
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    read -p "Would you like to install Python 3? (yes/no): " py_response

    if [[ "$py_response" == "yes" ]]; then
        echo "Installing Python 3. This may require your password."
        sudo apt-get update
        sudo apt-get install -y python3
        echo "Python 3 installed successfully."
    else
        echo "Python 3 is required to run this script."
        exit 1
    fi
fi

# Run the Python script with sudo
python3 "$PYTHON_SCRIPT_NAME"

# Optionally, remove the Python script after execution
rm "$PYTHON_SCRIPT_NAME"

# Define the service file content
SERVICE_FILE="/etc/systemd/system/paxd.service"
SERVICE_CONTENT="[Unit]
Description=Unigrid Paxd Service
After=network.target

[Service]
User=$USER
ExecStart=/usr/local/bin/paxd start --hedgehog=https://149.102.147.45:39886 --p2p.seeds \"fe420bfcff68beff824d9777bfe6ce1aa4cf8f43@149.102.133.13:26656,06ed85d8b34ca3a4275072894fc297dce416b708@194.233.95.48:26656,e339ab8163a2774fccbc78ff09ffbf0991adc310@38.242.156.2:26656\"
Restart=always
RestartSec=3
StandardOutput=file:$HOME/.pax/paxd.log
StandardError=file:$HOME/.pax/paxd-error.log

[Install]
WantedBy=multi-user.target"

# Check if the service file exists and create/update it
if [ -f "$SERVICE_FILE" ]; then
    echo "Updating paxd service configuration..."
else
    echo "Creating paxd service configuration..."
fi

echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE"

# Reload systemd, enable and start paxd service
sudo systemctl daemon-reload
sudo systemctl enable paxd.service
sudo systemctl start paxd.service

echo "Installing the manager script..."
sudo bash -ic "$(wget -4qO- -o- raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-4/scripts/install_manager.sh)" ; source ~/.bashrc

echo "Paxd has been installed successfully."
echo "You can safely close this log with Ctrl+C."
echo -e "\n\n"
sleep 5

tail -f "$HOME/.pax/paxd.log"


