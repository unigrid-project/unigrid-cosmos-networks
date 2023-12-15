## Generate Checksum
sha256sum genesis.json | awk '{print $1}' > sha256sum.txt
