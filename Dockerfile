# Python image as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Git and clean up to minimize image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . .

# Command to run the bot
CMD ["python", "bot.py"]