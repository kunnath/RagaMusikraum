# 🎵 Music Analyzer - Command Cheat Sheet

Quick reference for common commands and operations.

---

## 🚀 Setup & Installation

```bash
# Install FFmpeg (required)
brew install ffmpeg                    # macOS
sudo apt-get install ffmpeg           # Ubuntu/Debian

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate              # macOS/Linux
venv\Scripts\activate                 # Windows

# Install dependencies
pip install -r requirements.txt

# Run setup script (macOS/Linux)
chmod +x setup.sh && ./setup.sh
```

---

## 🎮 Running the Application

```bash
# Start Streamlit web app
streamlit run app.py

# Run on custom port
streamlit run app.py --server.port 8080

# Run for network access
streamlit run app.py --server.address 0.0.0.0

# Run tests
python test_cases.py

# Run example script
python example.py

# Analyze specific file
python example.py path/to/song.mp3
```

---

## 💻 Python API Usage

### Basic Analysis
```python
from src.audio_processor import AudioProcessor
from src.pitch_detector import PitchDetector
from src.note_converter import NoteConverter

# Load audio
processor = AudioProcessor()
audio, sr = processor.process_from_file("song.mp3")

# Detect pitch
detector = PitchDetector()
times, freqs, confs = detector.detect_pitch(audio, method='librosa')

# Convert to notes
converter = NoteConverter()
notes = converter.frequencies_to_notes(freqs, times)
```

### Create Visualizations
```python
from src.visualizer import AudioVisualizer

visualizer = AudioVisualizer()
visualizer.plot_pitch_over_time(times, freqs, confs, output_path="pitch.png")
```

### Export MIDI
```python
from src.midi_exporter import MidiExporter

exporter = MidiExporter()
segments = converter.get_note_segments(freqs, times)
exporter.create_midi_from_segments(segments, "output.mid")
```

---

## 🔧 Configuration

### Edit Settings
```bash
# Open configuration file
nano src/config.py
```

### Common Settings
```python
# Audio settings
SAMPLE_RATE = 44100
HOP_LENGTH = 512

# Pitch detection
PITCH_METHODS['crepe']['model_capacity'] = 'full'  # tiny/small/medium/large/full
PITCH_METHODS['librosa']['fmin'] = 80
PITCH_METHODS['librosa']['fmax'] = 1200

# MIDI export
MIDI_TEMPO = 120
MIDI_VELOCITY = 100
```

---

## 📦 Package Management

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Install specific package
pip install package_name

# Install optional packages
pip install essentia  # May require system dependencies

# Uninstall package
pip uninstall package_name

# List installed packages
pip list

# Check for outdated packages
pip list --outdated
```

---

## 🐳 Docker Commands

```bash
# Build image
docker build -t music-analyzer .

# Run container
docker run -p 8501:8501 music-analyzer

# Run with volume mounts
docker run -p 8501:8501 \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/temp:/app/temp \
  music-analyzer

# Use docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 🌐 Deployment Commands

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
heroku logs --tail
```

### Google Cloud
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/music-analyzer
gcloud run deploy --image gcr.io/PROJECT_ID/music-analyzer
```

### AWS EC2
```bash
ssh -i key.pem ubuntu@your-ec2-ip
sudo systemctl start music-analyzer
sudo systemctl status music-analyzer
```

---

## 🧪 Testing Commands

```bash
# Run all tests
python test_cases.py

# Run with verbose output
python -v test_cases.py

# Test specific module
python -c "from src.pitch_detector import PitchDetector; print('✓ Import successful')"

# Check imports
python -c "import librosa, aubio, crepe, streamlit; print('✓ All imports OK')"
```

---

## 📊 File Operations

```bash
# List outputs
ls -lh outputs/

# Remove old outputs
rm outputs/*.png outputs/*.mid outputs/*.json

# Clean temp files
rm temp/*

# Check disk usage
du -sh outputs/ temp/

# Find large files
find . -type f -size +10M
```

---

## 🔍 Debugging

```bash
# Check Python version
python --version

# Check installed packages
pip show librosa
pip show streamlit

# Verify FFmpeg
ffmpeg -version
which ffmpeg

# Check port usage
lsof -i :8501

# View logs
tail -f app.log

# Python debugger
python -m pdb app.py
```

---

## 🛠️ Maintenance

```bash
# Update yt-dlp (for YouTube downloads)
pip install --upgrade yt-dlp

# Clear pip cache
pip cache purge

# Recreate virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Update all packages
pip list --outdated | awk '{print $1}' | xargs pip install -U
```

---

## 📝 Git Operations

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit"

# Create .gitignore
echo "venv/" >> .gitignore
echo "outputs/*.png" >> .gitignore
echo "temp/*" >> .gitignore

# Push to GitHub
git remote add origin YOUR_REPO_URL
git push -u origin main

# Update and commit
git add .
git commit -m "Your message"
git push
```

---

## 🎵 Example Workflows

### Analyze YouTube Video
```bash
# 1. Start app
streamlit run app.py

# 2. In browser:
#    - Select "URL" input
#    - Paste YouTube URL
#    - Choose pitch method
#    - Click "Download and Analyze"
#    - View results in Results tab
```

### Process Local File
```bash
# Command line
python example.py path/to/song.mp3

# Or in Python
python
>>> from src.audio_processor import AudioProcessor
>>> processor = AudioProcessor()
>>> audio, sr = processor.process_from_file("song.mp3")
```

### Batch Process Files
```python
# Create batch_process.py
import os
from src.audio_processor import AudioProcessor
from src.pitch_detector import PitchDetector

processor = AudioProcessor()
detector = PitchDetector()

for filename in os.listdir("input_folder"):
    if filename.endswith(".mp3"):
        audio, sr = processor.process_from_file(f"input_folder/{filename}")
        times, freqs, confs = detector.detect_pitch(audio)
        # Process results...
```

---

## 🔗 Useful URLs

```bash
# Local app
http://localhost:8501

# Network access
http://YOUR_LOCAL_IP:8501

# Health check
http://localhost:8501/_stcore/health
```

---

## 📚 Quick Reference Links

- **Documentation**: See [README.md](README.md)
- **API Reference**: See [API.md](API.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 💡 Tips & Tricks

```bash
# Run in background (Linux/macOS)
nohup streamlit run app.py &

# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Monitor resource usage
top | grep python
htop  # If installed

# Generate requirements from current env
pip freeze > requirements.txt

# Create alias for quick start (add to ~/.bashrc or ~/.zshrc)
alias music-analyzer='cd ~/music-analyzer && source venv/bin/activate && streamlit run app.py'
```

---

## 🚨 Emergency Commands

```bash
# App won't start
pkill -f streamlit
rm -rf ~/.streamlit
streamlit cache clear

# Out of memory
# Reduce CREPE model size in src/config.py
# Or use librosa method instead

# Dependencies broken
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Nuclear option - fresh start
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

**Keep this cheat sheet handy for quick reference!** 📋

*Last updated: December 2025*
