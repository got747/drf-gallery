# Dockerfile
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create app directory
RUN mkdir /service_gallery
WORKDIR /service_gallery

# Copy the project files
COPY requirements.txt /service_gallery/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

COPY . /service_gallery/
