#!/bin/bash

# --- Usage Check ---
if [[ $# -ne 4 ]]; then
    echo "Usage: $0 <pi-user> <pi-ip-file> <remote-photo-dir> <local-dest-dir>"
    echo "Example: $0 pi pi_ip.txt /home/pi/photos ~/Downloads/from-pi"
    exit 1
fi

PI_USER="$1"
PI_IP_FILE="$2"
REMOTE_DIR="$3"
LOCAL_DIR="$4"

# --- Read IP address from file ---
if [[ ! -f "$PI_IP_FILE" ]]; then
    echo "Error: IP address file '$PI_IP_FILE' does not exist."
    exit 2
fi

PI_HOST=$(head -n 1 "$PI_IP_FILE")
PI_ADDR="${PI_USER}@${PI_HOST}"

# --- Ensure local destination exists ---
mkdir -p "$LOCAL_DIR"

# --- Find and copy recent image files from Pi ---
ssh "$PI_ADDR" "find '$REMOTE_DIR' -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \)" | while read -r file; do
    echo "Copying $file from $PI_ADDR..."
    scp "$PI_ADDR:$(printf '%q' "$file")" "$LOCAL_DIR/"
done
