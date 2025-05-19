# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# COPY the rest of the code 
COPY . .

# Expose the port 
EXPOSE 8000

# Default command to run the app
CMD ["python", "start.py"]