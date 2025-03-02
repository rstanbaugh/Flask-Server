#!/bin/bash
# Stop the Flask server (server_prod.py)

# Navigate to the project directory
cd ~/Flask-Server

# Find the PID of the server process
PID=$(ps aux | grep -v grep | grep "python server_prod.py" | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "No server process found!"
    exit 1
fi

# Kill the process
kill -9 $PID
echo "Server stopped (PID: $PID)"