#!/bin/bash
# Start the Flask server in the background with virtual environment

# Navigate to the project directory
cd ~/Flask-Server

# Activate the virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    source ./flask/bin/activate
    DEACTIVATE=1
else
    echo "Virtual environment already active: $VIRTUAL_ENV"
    DEACTIVATE=0
fi

# Check if the server is already running
if ps aux | grep -v grep | grep "python server_prod.py" > /dev/null; then
    echo "Server is already running!"
    exit 1
fi

# Start the server with nohup
nohup python server_prod.py &> server.log &
echo "Server started. Logs are in server.log"

# Deactivate only if we activated it
if [ "$DEACTIVATE" -eq 1 ]; then
    deactivate
fi