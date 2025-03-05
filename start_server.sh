#!/bin/bash
# Start the Flask server using Gunicorn in the background with virtual environment

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

# Check if Gunicorn is already running
if pgrep -f "gunicorn" > /dev/null; then
    echo "⚠️ Gunicorn server is already running!"
    exit 1
fi

# Start the server with Gunicorn (4 workers, binds to localhost)
nohup gunicorn -w 4 -b 127.0.0.1:8000 server_prod:app --daemon &> server.log &
echo "✅ Gunicorn started. Logs are in server.log"

# Deactivate only if we activated it
if [ "$DEACTIVATE" -eq 1 ]; then
    deactivate
fi