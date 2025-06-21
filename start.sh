#!/bin/sh

# This script is the entrypoint for the Docker container.
# It starts both the FastAPI backend and the Nginx web server concurrently.

# Start the Uvicorn server for the FastAPI application in the background.
# First, change the directory to where your main FastAPI app.py is located.
# Based on your structure, it's inside 'backend/vendor_app/'.
cd /app/backend/vendor_app

# Run Uvicorn. 'app:app' refers to the 'app' instance in 'app.py'.
# It listens on all network interfaces (0.0.0.0) on port 8000.
# The '&' sends this command to the background, allowing the script to continue.
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Change back to the root application directory for consistency.
cd /app

# Start the Nginx web server in the foreground.
# The 'daemon off;' command ensures Nginx runs in the foreground,
# which keeps the Docker container alive. If Nginx exits, the container exits.
# Since Uvicorn is running in the background, this script will effectively
# block here and keep the container running as long as Nginx is running.
nginx -g "daemon off;"

