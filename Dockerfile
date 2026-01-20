# Use specific platform for AMD Linux (x86_64)
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

# Install system dependencies and verify tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Expose ports (3000 for App, 11434 for Ollama if needed)
EXPOSE 3000

# Set entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
