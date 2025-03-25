FROM python:3.9-slim

WORKDIR /app

# Install cron service
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY *.py /app/
COPY requirements.txt /app/
COPY docker/entrypoint.sh /app/
COPY docker/crontab /etc/cron.d/app-cron

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set crontab permissions
RUN chmod 0644 /etc/cron.d/app-cron
RUN crontab /etc/cron.d/app-cron

# Set entry script permissions
RUN chmod +x /app/entrypoint.sh

# Set container startup command
ENTRYPOINT ["/app/entrypoint.sh"]
