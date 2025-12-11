# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

**On macOS:**
```bash
# Install FFmpeg
brew install ffmpeg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**On Ubuntu/Debian:**
```bash
# Install FFmpeg
sudo apt-get update
sudo apt-get install ffmpeg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**On Windows:**
```powershell
# Install FFmpeg from https://ffmpeg.org/download.html

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**Or use the setup script (macOS/Linux):**
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Run the Application

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start the web app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Analyze Your First Song

1. **Choose Input Method:**
   - **URL**: Paste a YouTube link
   - **File**: Upload an MP3/WAV file

2. **Configure Settings** (sidebar):
   - Pitch method: Start with "librosa" (fastest)
   - Enable post-processing
   - Select visualizations

3. **Click Analyze!**
   - Wait 30-60 seconds
   - View results in the Results tab
   - Download MIDI/JSON files

### 4. Try the Examples

**Run test suite:**
```bash
python test_cases.py
```

**Analyze a synthetic scale:**
```bash
python example.py
```

**Analyze your own file:**
```bash
python example.py path/to/your/song.mp3
```

## 📋 Command Reference

```bash
# Start web app
streamlit run app.py

# Run tests
python test_cases.py

# Analyze file via command line
python example.py your_audio.mp3

# Install additional dependencies
pip install package_name

# Update packages
pip install --upgrade -r requirements.txt
```

## 🎯 Tips for Best Results

1. **Audio Quality**: Use high-quality files (320kbps or lossless)
2. **Content Type**: Works best with vocals and solo instruments
3. **Pitch Method**: 
   - CREPE = Most accurate (slow)
   - Librosa = Fast and good
   - Aubio = Good for monophonic
4. **Duration**: Keep under 5 minutes for faster processing

## ❓ Common Issues

**"FFmpeg not found"**
→ Install FFmpeg (see step 1)

**"Module not found"**
→ Run: `pip install -r requirements.txt`

**"YouTube download failed"**
→ Update: `pip install --upgrade yt-dlp`

**"Out of memory"**
→ Use shorter audio clips or smaller CREPE model

## 📚 Next Steps

- Read the [full README](README.md) for detailed documentation
- Explore the [example script](example.py) for API usage
- Check [test_cases.py](test_cases.py) for code examples
- Customize [config.py](src/config.py) for your needs

---

**Need help?** Check the [README](README.md) troubleshooting section!
