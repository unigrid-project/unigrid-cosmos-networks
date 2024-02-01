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
sudo python3 "$PYTHON_SCRIPT_NAME"

# Optionally, remove the Python script after execution
rm "$PYTHON_SCRIPT_NAME"
