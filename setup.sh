#!/bin/bash

# Music Analyzer Setup Script
# Automates the installation process

echo "🎵 Music Analyzer - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"

# Check FFmpeg
echo ""
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n1)
    echo "✓ FFmpeg is installed"
else
    echo "⚠️  FFmpeg not found!"
    echo ""
    echo "Please install FFmpeg:"
    echo "  macOS:   brew install ffmpeg"
    echo "  Ubuntu:  sudo apt-get install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Remove and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"

# Install requirements
echo ""
echo "Installing Python packages..."
echo "(This may take several minutes...)"
echo ""

# Install packages one by one to show progress
packages=(
    "numpy"
    "scipy"
    "librosa"
    "soundfile"
    "aubio"
    "matplotlib"
    "plotly"
    "streamlit"
    "yt-dlp"
    "requests"
    "mido"
    "pretty-midi"
    "pandas"
    "pydub"
    "tqdm"
    "crepe"
    "tensorflow"
)

for package in "${packages[@]}"; do
    echo "Installing $package..."
    pip install "$package" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "  ✓ $package installed"
    else
        echo "  ⚠️  $package installation failed (may be optional)"
    fi
done

# Try to install essentia (may fail on some systems)
echo ""
echo "Installing essentia (optional, may fail)..."
pip install essentia > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ essentia installed"
else
    echo "⚠️  essentia installation failed (optional, app will work without it)"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p temp
mkdir -p outputs
echo "✓ Directories created"

# Run tests
echo ""
read -p "Run test suite to verify installation? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running tests..."
    python test_cases.py
fi

# Summary
echo ""
echo "================================"
echo "🎉 Setup Complete!"
echo "================================"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run Streamlit app: streamlit run app.py"
echo ""
echo "Or run tests:"
echo "  python test_cases.py"
echo ""
echo "For more information, see README.md"
echo ""
