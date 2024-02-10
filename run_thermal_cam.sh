#!/bin/bash

# Check if two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <MQTT_HOST> <UDP_PORT>"
    exit 1
fi

MQTT_HOST=$1
UDP_PORT=$2

# Get the directory of the current script
SCRIPT_DIR=$(dirname "$0")

# Execute the Python script with the MQTT Host and UDP Port arguments
python3 "$SCRIPT_DIR/purethermal.py" --host "$MQTT_HOST" --port "$UDP_PORT"
