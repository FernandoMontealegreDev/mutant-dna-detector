# Use the official Python 3.12.5 image as base
FROM python:3.12.5-slim

# Update the container and install necessary dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libmariadb-dev \
    pkg-config \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the necessary dependencies inside the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the start script and make it executable
COPY /app/start.sh /app/
RUN chmod +x /app/start.sh

# Copy the rest of the project files into the container
COPY . /app/

# Expose the port where the application will run
EXPOSE 8000

# Use the start script as the command
CMD ["/app/start.sh"]