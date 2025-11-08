FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL application code (bao gồm cả thư mục web)
COPY . .

# Expose port
EXPOSE 7862

# Create necessary directories
RUN mkdir -p database logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Verify files are copied
RUN ls -la /app/web/

# Start the application from web directory
CMD ["python", "web/app.py"]