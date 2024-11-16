# Use Python slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies and utilities
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    cmake \
    git \
    libgtk2.0-0 \
    libcanberra-gtk-module \
    libglu1-mesa \
    libpng-dev \
    libcairo2-dev \
    libboost-all-dev \
    qt5-qmake qtbase5-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and extract OpenSCAD source
RUN wget https://github.com/openscad/openscad/releases/download/openscad-2021.01/openscad-2021.01.src.tar.gz && \
    tar -xvzf openscad-2021.01.src.tar.gz && \
    cd openscad-2021.01 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install

# Copy your application code into the Docker container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Set environment variable for OpenSCAD binary
ENV PATH="/usr/local/bin:${PATH}"

# Expose the port your app runs on
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "app.py"]
