#!/bin/bash
# Setup script for KivySample - works on Ubuntu 22.04+ (Python 3.10+)

set -e

echo "=== KivySample Setup ==="

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Detected: $NAME $VERSION_ID"
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Install system dependencies
echo ""
echo "Installing system dependencies (requires sudo)..."
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

# Install Java 17 (required for Android builds)
echo ""
echo "Installing Java 17..."
sudo apt-get install -y openjdk-17-jdk

# Set JAVA_HOME in profile if not set
JAVA_HOME_PATH="/usr/lib/jvm/java-17-openjdk-amd64"
if [ -d "$JAVA_HOME_PATH" ]; then
    if ! grep -q "JAVA_HOME=" ~/.bashrc; then
        echo "" >> ~/.bashrc
        echo "# Java for Android builds" >> ~/.bashrc
        echo "export JAVA_HOME=$JAVA_HOME_PATH" >> ~/.bashrc
        echo "Added JAVA_HOME to ~/.bashrc"
    fi
    export JAVA_HOME=$JAVA_HOME_PATH
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Removing existing .venv..."
    rm -rf .venv
fi
python3 -m venv .venv

# Activate and install dependencies
echo ""
echo "Installing Python dependencies..."
source .venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate the environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the app:"
echo "  python main.py -m screen:phone_oneplus_6t,portrait,scale=0.5"
echo ""
echo "Or use VS Code tasks (Ctrl+Shift+P -> Tasks: Run Task)"
echo ""
