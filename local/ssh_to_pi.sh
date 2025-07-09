#!/bin/bash

# File containing the IP address or hostname (one line)
IP_FILE="$1"

# Check that the file exists and is not empty
if [[ ! -f "$IP_FILE" || ! -s "$IP_FILE" ]]; then
    echo "Error: IP file '$IP_FILE' not found or empty."
    exit 1
fi

# Read the IP address or hostname
TARGET=$(head -n 1 "$IP_FILE")

# Run SSH
ssh "sparsh@${TARGET}"
