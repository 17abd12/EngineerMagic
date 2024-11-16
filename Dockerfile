# Use a Python base image from Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies for OpenSCAD and your app
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    wget \
    libgtk2.0-0 \
    libcanberra-gtk-module \
    libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

# Install OpenSCAD Nightly (change URL to the latest version)
RUN wget https://github.com/openscad/openscad/releases/download/nightly/OpenSCAD-nightly-2024.0-rc-1-x86_64-linux.tar.xz && \
    tar -xf OpenSCAD-nightly-2024.0-rc-1-x86_64-linux.tar.xz && \
    mv OpenSCAD-nightly-2024.0-rc-1-x86_64-linux /usr/local/bin/openscad

# Copy the application code to the container
COPY . /app

# Install Python dependencies (make sure you have a requirements.txt in the project)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
