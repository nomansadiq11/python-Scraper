# Use an official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY ./app/ .

# Set environment variables (if needed)
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "main.app"]
