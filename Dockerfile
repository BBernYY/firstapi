# Start from the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Copy your application code into the Docker image (if you have any)
COPY main.py /app/
COPY build.sql /app/
COPY start_all_programs.sh /app/
COPY token.env /app/

WORKDIR /app/

# Expose the port MariaDB is running on
EXPOSE 5000

# Set up server
RUN apt update && \
  apt install -y && \
  apt install -y python3 && \
  apt install -y python3-venv && \
  apt install -y mariadb-server

# Set up MariaDB (optional: you can customize this as needed)
# This example assumes a basic setup with a default configuration.
# You might need additional configuration for production use.
RUN service mariadb start && \
    mariadb -e "$(cat build.sql)"

# Set up Python
RUN python3 -m venv . && \
    bin/pip install flask mysql-connector

# Set the entrypoint (this is optional and depends on your use case)
# For a typical use case, you might start MariaDB and then run a Python script
# You could use a script to start both services if needed
CMD ["bash", "/app/start_all_programs.sh"]
