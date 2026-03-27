# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Prevent Python from writing .pyc files to disk and disable buffering in logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# System dependencies, usually gcc or git when a pip install needs it
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies (using Docker cache optimizes builds)
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the API code
COPY . /app/

# Expose the default port for the Django API
EXPOSE 8000

# By default, start the server binding to all interfaces
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
