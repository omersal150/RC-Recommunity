# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt to container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Command to run the Flask application
CMD ["flask", "run"]
