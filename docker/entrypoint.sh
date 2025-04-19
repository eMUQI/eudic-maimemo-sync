#!/bin/bash
set -e

# --- Environment Setup ---
echo "Exporting environment variables for cron..."
# Create file with selected env vars for cron job to source
printenv | grep -E 'EUDIC_API_KEY|MOMO_API_KEY|MOMO_NOTEPAD_ID|EUDIC_CATEGORY_ID|TZ|PATH|PYTHONPATH' | sed 's/^\([^=]*\)=\(.*\)$/export \1="\2"/g' > /app/environment.env
# Add python path to PATH
echo "export PATH=$PATH:/usr/local/bin" >> /app/environment.env
# Secure environment file
chmod 600 /app/environment.env

# --- Crontab Setup ---
# Set cron schedule (use default if CRON_SCHEDULE is not set)
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 18 * * *"} # Default: 6:00 PM daily
echo "Generating crontab file with schedule: $CRON_SCHEDULE"

# Create crontab file
echo "$CRON_SCHEDULE root bash -c . /app/environment.env; /usr/local/bin/python /app/sync.py >> /proc/1/fd/1 2>&1" > /etc/cron.d/app-cron
# Add trailing newline (required by cron)
echo "" >> /etc/cron.d/app-cron

# --- Set Crontab Permissions ---
# Set standard permissions for cron file
chmod 0644 /etc/cron.d/app-cron

# --- Optional: Initial Sync on Start ---
echo "Running initial sync..."
# Load env vars and run the script once
. /app/environment.env && /usr/local/bin/python /app/sync.py

# --- Start Cron Service ---
echo "Starting cron daemon in foreground..."
# Run cron in foreground (-f) making it the container's main process
# Allows Docker to manage it and capture logs directly
cron -f