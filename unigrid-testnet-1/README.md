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

> Add `unigrid-testnet-1` to keplr: <https://docs.unigrid.org/unigrid-cosmos-networks/>


🚰 Faucet
The unigrid-testnet-1 testnet faucet is available via our [discord server](https://docs.unigrid.org/docs/testnet/jointestnet/)

If you are a validator and in need of more funds, you can request them via this [form](https://forms.gle/Ubv2u6T1AWgWkTRS9).

## Chaim params
| Params          | Value                                                                                                                                                                                                          |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Validator min_self_delegation: |        1000000000000           |
| Decimals:                      |        8                       |
| Denom:                         |        ugd                     |
| Gov min_deposit amount:        |        5000000000              |
 

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
ExecStart=/usr/local/bin/paxd start --home=/home/<username>/.unigrid-testnet-1 --hedgehog=https://82.208.23.218:39886 --p2p.seeds "8f278bf57932e1f808aefc7c82aaaf130470e2bd@194.233.95.48:26656,e339ab8163a2774fccbc78ff09ffbf0991adc310@38.242.156.2:26656"
Restart=always
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

## Generate Keys

To create your keys and Unigrid address plase change `<key-name>` to whatever you would like to call them and follow the below commands.

```bash
# Create new keypair
paxd keys add <key-name> --home=/home/$USER/.unigrid-testnet-1

# Restore existing wallet with mnemonic seed phrase.
paxd keys add <key-name> --recover --home=/home/$USER/.unigrid-testnet-1

# Query the keystore for your public address
paxd keys show <key-name> -a --home=/home/$USER/.unigrid-testnet-1

# Show all keys
paxd keys list --home=/home/$USER/.unigrid-testnet-1
```


## Monitoring
To monitor the logs of `paxd`:
```bash
tail -f /home/<username>/.unigrid-testnet-1/paxd.log
```
