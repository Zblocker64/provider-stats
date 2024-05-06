# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY app/requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app/ .

# Specify the command to run on container start
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "app:app"]
