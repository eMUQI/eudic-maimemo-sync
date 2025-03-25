#!/bin/bash
set -e

# Start cron service
service cron start

# Execute script once at container startup (optional)
python /app/sync.py

# Keep container running
tail -f /dev/null
