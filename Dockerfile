# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y nodejs npm

# Install Newman globally
RUN npm install -g newman

# Install Newman reporter HTML Extra globally
RUN npm install -g newman-reporter-htmlextra

# Copy and install Python dependencies
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV PATH="/app:${PATH}"

# Run app.py when the container launches
CMD ["python", "runner.py"]
