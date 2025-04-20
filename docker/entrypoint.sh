#!/bin/bash
set -e

# Define the path for the runtime crontab file
RUNTIME_CRONTAB="/app/runtime.crontab"
# Define the command to be scheduled
SYNC_COMMAND="/usr/local/bin/python /app/sync.py"

# --- Crontab Setup (Dynamic) ---
# Set cron schedule (use default if CRON_SCHEDULE is not set)
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 18 * * *"} # Default: 6:00 PM daily
echo "Generating crontab file with schedule: $CRON_SCHEDULE"

# Create the crontab file for Supercronic
# Note: Supercronic automatically forwards stdout/stderr, no redirection needed
echo "$CRON_SCHEDULE $SYNC_COMMAND" > "$RUNTIME_CRONTAB"
# Add trailing newline (good practice)
echo "" >> "$RUNTIME_CRONTAB"

echo "Runtime crontab content:"
cat "$RUNTIME_CRONTAB" # Optional: Log the generated crontab for debugging

# --- Optional: Initial Sync on Start ---
if [[ "$RUN_ON_STARTUP" == "true" || "$RUN_ON_STARTUP" == "1" ]]; then
    echo "Running initial sync based on RUN_ON_STARTUP flag..."
    $SYNC_COMMAND # Execute the command directly
else
    echo "Skipping initial sync. Set RUN_ON_STARTUP=true in docker-compose to run on startup."
fi

# --- Start Supercronic Service ---
echo "Starting Supercronic scheduler with runtime crontab..."
# Use exec to replace the shell process with supercronic
# Point supercronic to the dynamically generated crontab file
exec /usr/local/bin/supercronic "$RUNTIME_CRONTAB"