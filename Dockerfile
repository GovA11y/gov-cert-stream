# Use an official Python runtime as a parent image
# Use bullseye with Python pre-installed
FROM python:3.9-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy all the things...
ADD . /app/

# Install python packages and remove unnecessary packages
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get autoremove -y gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Make Log file
RUN mkdir -p /app/logs

# Run the command to start things...
CMD ["python", "run.py"]