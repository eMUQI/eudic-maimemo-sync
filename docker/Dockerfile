FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl procps && rm -rf /var/lib/apt/lists/*

# Latest releases available at https://github.com/aptible/supercronic/releases
# Remove the cron installation and add Supercronic
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.33/supercronic-linux-arm64 \
    SUPERCRONIC_SHA1SUM=e0f0c06ebc5627e43b25475711e694450489ab00 \
    SUPERCRONIC=supercronic-linux-arm64

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Copy project files
COPY *.py /app/
COPY requirements.txt /app/
COPY docker/entrypoint.sh /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entry script permissions
RUN chmod +x /app/entrypoint.sh

# Set container startup command
ENTRYPOINT ["/app/entrypoint.sh"]