# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose default port
ENV PORT=8080
EXPOSE 8080

# Start with gunicorn, binding to PORT env
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:$PORT app:app"]