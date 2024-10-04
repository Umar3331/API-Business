FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium-driver

# Install Selenium and other dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the display port to avoid crashes
ENV DISPLAY=:99

# Copy the current directory contents into the container
COPY . .

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
