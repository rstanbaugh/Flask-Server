#!/bin/bash
# Stop the Gunicorn server gracefully (fallback to force if necessary)

# Navigate to the project directory
cd ~/Flask-Server

# Find the PID of the Gunicorn process
PID=$(pgrep -f "gunicorn")

if [ -z "$PID" ]; then
    echo "❌ No Gunicorn server process found!"
    exit 1
fi

# Gracefully stop the Gunicorn process (SIGTERM)
echo "Gracefully stopping Gunicorn server (PID: $PID)..."
kill -15 $PID

# Wait a few seconds for the process to terminate
sleep 5

# Check if the process is still running
if ps -p $PID > /dev/null; then
    echo "❌ Server did not stop gracefully, forcefully killing (SIGKILL)..."
    kill -9 $PID
    echo "✅ Gunicorn server forcefully stopped (PID: $PID)"
else
    echo "✅ Gunicorn server stopped gracefully (PID: $PID)"
fi