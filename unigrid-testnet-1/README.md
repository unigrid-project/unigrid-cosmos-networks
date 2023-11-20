# Unigrid Testnet Setup

## Automated Setup Using Script (recommended)

### Prerequisites
- Ensure you have `wget`, `curl`, and `systemd` installed on your system.
- `git` is required if you plan to download the latest version of `paxd` from the repository.

### Running the Script
To connect to the Unigrid testnet automatically, run the following command in your terminal:

```bash
wget -4qO- -o- https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-1/scripts/pax_reset.sh | bash
```

This script will:
- Stop the existing `paxd` service (if it exists).
- Clear existing data and log files.
- Download and verify the `genesis.json` file.
- Download and set up the `paxd` binary.
- Set up and start the `paxd` service.

**Note:** The script will tail the `paxd` log file at the end. You can exit the log view by pressing `Ctrl+C` and access it again anytime with the command `tail -f ~/.unigrid-testnet-1/paxd.log`.

## System Commands

### Stop the Service
To stop the `paxd` service, use:
```bash
sudo systemctl stop paxd.service
```

### Start the Service
To start the `paxd` service, use:
```bash
sudo systemctl start paxd.service
```

### Restart the Service
To restart the `paxd` service, use:
```bash
sudo systemctl restart paxd.service
```

### Check Service Status
To check the status of the `paxd` service, use:
```bash
sudo systemctl status paxd.service
```

### Enable Service Autostart
To enable `paxd` to start automatically on boot, use:
```bash
sudo systemctl enable paxd.service
```

### Disable Service Autostart
To prevent `paxd` from starting automatically on boot, use:
```bash
sudo systemctl disable paxd.service
```

## Manual Setup

### Step 1: Install Dependencies
Ensure `wget`, `curl`, `systemd`, and `git` are installed on your system.

### Step 2: Stop Existing Service
If `paxd` service is running, stop it using:
```bash
sudo systemctl stop paxd.service
```

### Step 3: Clear Data and Logs
Remove existing data and log files from `~/.unigrid-testnet-1/data` directory.

### Step 4: Download and Verify Genesis File
Download the `genesis.json`:
```bash
wget -O genesis.json https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-1/genesis/genesis.json
```
Verify the checksum:
```bash
wget -O sha256sum.txt https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-1/genesis/sha256sum.txt
sha256sum -c sha256sum.txt
```

### Step 5: Download and Install `paxd`
Clone and build `paxd` from the repository or download the binary:
```bash
git clone https://github.com/unigrid-project/cosmos-daemon.git
cd cosmos-daemon
# Follow the build instructions
```

### Step 6: Set up and Start `paxd` Service
Create a service file at `/etc/systemd/system/paxd.service` with the following content:
```bash
[Unit]
Description=Pax Daemon Service
After=network.target

[Service]
User=<username>
ExecStart=/usr/local/bin/paxd start --home=/home/<username>/.unigrid-testnet-1 --hedgehog=https://82.208.23.218:39886 --p2p.seeds "e5e85ef8eaa493c566108823519bd2c89b3a7803@194.233.95.48:26656,666d2cc217a5aef8b6b7fc8608706df76640b42a@38.242.156.2:26656"
Restart=always
RestartSec=3
StandardOutput=file:/home/<username>/.unigrid-testnet-1/paxd.log
StandardError=file:/home/<username>/.unigrid-testnet-1/paxd-error.log

[Install]
WantedBy=multi-user.target
```
Replace `<username>` with your username. Then enable and start the service:
```bash
sudo systemctl enable paxd.service
sudo systemctl start paxd.service
```

## Monitoring
To monitor the logs of `paxd`:
```bash
tail -f /home/<username>/.unigrid-testnet-1/paxd.log
```
