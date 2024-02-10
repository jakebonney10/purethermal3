#!/bin/bash

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <MQTT_HOST>"
    exit 1
fi

MQTT_HOST=$1

# Execute the Python script with the MQTT Host argument
python3 purethermal.py --host "$MQTT_HOST"
