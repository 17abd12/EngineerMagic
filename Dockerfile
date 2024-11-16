# Use Python slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies and utilities
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    libgtk2.0-0 \
    libcanberra-gtk-module \
    libglu1-mesa \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Download and install OpenSCAD from source
RUN wget https://github.com/openscad/openscad/releases/download/openscad-2021.01/openscad-2021.01.src.tar.gz && \
    tar -xvzf openscad-2021.01.src.tar.gz && \
    cd openscad-2021.01 && \
    cmake . && \
    make && \
    make install

# Copy application code to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Set environment variables (if necessary for your app)
ENV PATH="/usr/local/bin:${PATH}"

# Run your application (adjust this based on your app's entry point)
CMD ["python", "app.py"]
