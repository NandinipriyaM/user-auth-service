##############################
# Stage 1: Builder
##############################
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

##############################
# Stage 2: Runtime
##############################
FROM python:3.11-slim

# Install cron + timezone data
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set timezone to UTC
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Setup cron job
RUN chmod 0644 /app/cron/2fa-cron && \
    crontab /app/cron/2fa-cron

# Create mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

VOLUME ["/data", "/cron"]

EXPOSE 8080

# Start cron + FastAPI server
CMD cron && uvicorn main:app --host 0.0.0.0 --port 8080
