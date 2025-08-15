# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium
RUN python -m playwright install-deps

# Copy the entire application
COPY . .

# Install frontend dependencies and build
RUN cd openoperator-ui && npm install && npm run build

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV NODE_ENV=production

# Start command
CMD ["python", "backend_server.py"]