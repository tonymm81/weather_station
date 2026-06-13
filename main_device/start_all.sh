#!/bin/bash

sleep 5

LOGDIR="/var/log/weather_station"
mkdir -p "$LOGDIR"

MQTT="/usr/bin/python3 /home/pi/Desktop/new/new_weatherstation/main_device/connections.py"
SHUTDOWN="/usr/bin/python3 /home/pi/Desktop/new/new_weatherstation/main_device/shutdownServer.py"

echo "Starting weather station backend services..." >> "$LOGDIR/startup.log"

while true; do
    echo "Launching MQTT broker..." >> "$LOGDIR/startup.log"
    $MQTT &
    MQTT_PID=$!

    echo "Launching shutdown server..." >> "$LOGDIR/startup.log"
    $SHUTDOWN &
    SHUTDOWN_PID=$!

    wait -n $MQTT_PID $SHUTDOWN_PID

    echo "One of the backend services crashed, restarting..." >> "$LOGDIR/startup.log"

    kill $MQTT_PID 2>/dev/null
    kill $SHUTDOWN_PID 2>/dev/null

    sleep 2
done
