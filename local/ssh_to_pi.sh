#!/bin/bash

# Usage check
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <ip-file> <username>"
    echo "Example: $0 pi_ip.txt sparsh"
    exit 1
fi

# Parameters
IP_FILE="$2"
USERNAME="$1"

# Check that the IP file exists and is not empty
if [[ ! -f "$IP_FILE" || ! -s "$IP_FILE" ]]; then
    echo "Error: IP file '$IP_FILE' not found or empty."
    exit 1
fi

# Read the IP address or hostname
TARGET=$(head -n 1 "$IP_FILE")

# Run SSH
ssh "${USERNAME}@${TARGET}"
