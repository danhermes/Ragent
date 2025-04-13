# Use Raspberry Pi compatible base image
FROM balenalib/raspberrypi3-python:3.9-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install WiringPi
COPY wiringpi-2.61-1-armhf.deb /tmp/
RUN dpkg -i /tmp/wiringpi-2.61-1-armhf.deb

# Copy requirements and install Python dependencies
COPY setup.py system_requirements.txt ./
RUN pip3 install -e .

# Copy application code
COPY picar/ ./picar/
COPY app_control.py ./
COPY main.py ./

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python3", "app_control.py"] 