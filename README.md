# 🎵 Music Analyzer - User Guide

A comprehensive music analysis application with a beautiful modern UI that transforms audio into musical notes. Perfect for musicians, singers, music learners, and anyone who wants to analyze and understand music!

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Features Overview](#-features-overview)
3. [Main Features Guide](#-main-features-guide)
   - [Input Tab](#1--input-tab)
   - [Results Tab](#2--results-tab)
   - [Compare Songs Tab](#3--compare-songs-tab)
   - [Live Microphone Tab](#4--live-microphone-tab)
4. [Advanced Features](#-advanced-features)
5. [Tips & Best Practices](#-tips--best-practices)
6. [Troubleshooting](#-troubleshooting)
7. [Technical Details](#-technical-details)

---

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd music-analyzer
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Launch the app:**
   ```bash
   ./run.sh
   ```

4. **Open your browser:**
   ```
   http://localhost:8501
   ```

That's it! You're ready to analyze music! 🎉

---

## ✨ Features Overview

### 🎯 What Can You Do?

| Feature | Description | Use Case |
|---------|-------------|----------|
| **🌐 URL Analysis** | Analyze YouTube videos or audio URLs | Learn songs from YouTube |
| **📁 File Upload** | Upload your audio files | Analyze your recordings |
| **⚡ Quick Streaming** | Fast YouTube analysis (no download) | Quick previews |
| **🔧 RAW Converter** | Convert RAW audio to MP3 | Process microphone recordings |
| **▶️ Audio Preview** | Listen before converting | Verify recordings |
| **🔍 Song Comparison** | Compare two songs | Check your accuracy |
| **🎤 Live Microphone** | Real-time voice analysis | Practice singing |
| **📊 Visualizations** | Beautiful charts and graphs | Understand your music |
| **🎹 MIDI Export** | Convert to MIDI format | Use in DAW software |

---

## 🎵 Main Features Guide

## 1. 📥 Input Tab

The Input tab is your starting point. Choose how you want to input audio.

### Option A: YouTube URL / Audio URL

**Perfect for:** Learning songs from YouTube, analyzing online music

**How to use:**
1. Select **"URL"** at the top
2. Paste a YouTube URL or direct audio link
3. Choose analysis method:
   - **🔽 Download and Analyze**: Full song, saves file (slower but complete)
   - **⚡ Quick Stream**: First 60 seconds, no file saved (faster preview)

**Example:**
```
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Click: "⚡ Quick Stream Analysis" for fast preview
```

**Tips:**
- Use Quick Stream for previews or learning specific parts
- Use Download for complete analysis and MIDI export
- Private/restricted videos won't work

---

### Option B: File Upload

**Perfect for:** Analyzing your own recordings, local files

**Supported formats:** MP3, WAV, FLAC, OGG, M4A

**How to use:**
1. Select **"File Upload"** at the top
2. Click **"Browse files"** or drag & drop
3. Wait for upload to complete
4. Click **"� Analyze Audio"**

**Tips:**
- Keep files under 100MB for best performance
- WAV and FLAC give best quality
- MP3 works great for most uses

---

### 🔧 RAW to MP3 Converter

**Perfect for:** Converting microphone recordings from RAW format

**Location:** Expand **"🔧 Convert RAW to MP3"** in File Upload section

**How to use:**

1. **Upload RAW file** (.raw extension)

2. **Configure settings:**
   - **Sample Rate**: 44100 Hz (CD quality) - most common
   - **Sample Format**: s16le (16-bit) - standard
   - **Channels**: Stereo (2) or Mono (1)
   - **MP3 Bitrate**: 256k (high quality)

3. **Preview first (recommended):**
   - Click **"▶️ Preview Audio"**
   - Listen to verify settings are correct
   - If sounds wrong, adjust settings and preview again

4. **Convert when ready:**
   - Click **"🎵 Convert to MP3"**
   - Download the converted file
   - Optionally analyze it right away

**Common Settings:**

| Recording Type | Sample Rate | Channels | Format |
|---------------|-------------|----------|--------|
| Voice/Mic | 44100 Hz | Mono (1) | s16le |
| Music Recording | 44100 Hz | Stereo (2) | s16le |
| Professional | 48000 Hz | Stereo (2) | s24le |
| Phone Recording | 16000 Hz | Mono (1) | s16le |

**Example:**
```
1. Upload: recording_20251211.raw
2. Set: 44100 Hz, s16le, Stereo
3. Preview: ▶️ Listen to check
4. Convert: 🎵 Save as MP3
5. Result: converted_20251211_125203.mp3
```

---

## 2. 📊 Results Tab

After analysis completes, view comprehensive results here.

### What You'll See:

#### **Dashboard Metrics**
- 🎵 **Total Notes**: How many notes detected
- ⏱️ **Duration**: Length of audio analyzed
- 🎼 **Note Range**: Lowest to highest note
- 🎯 **Most Common**: Your dominant note

#### **Visualizations**

1. **Notes Over Time**
   - See which notes play when
   - Timeline view of your melody
   - Color-coded by note

2. **Pitch Contour**
   - Your pitch accuracy graph
   - Shows pitch stability
   - Helps identify pitch issues

3. **Note Distribution**
   - Bar chart of note frequency
   - See your vocal/instrument range
   - Identify most-used notes

4. **Piano Roll** (if enabled)
   - Professional DAW-style view
   - Notes on piano keyboard
   - Time-based representation

#### **Export Options**

- **📥 Download MIDI**: Use in music software (FL Studio, Ableton, etc.)
- **📥 Download JSON**: Get raw data with timestamps
- **📥 Download Visualizations**: Save charts as PNG

---

## 3. 🔍 Compare Songs Tab

Compare your performance with the original song!

**Perfect for:**
- Checking singing accuracy
- Learning instrument parts
- Analyzing cover versions
- Vocal practice tracking

### How to Use:

1. **Select Original Song:**
   - Choose from previously analyzed files, OR
   - Upload a JSON file

2. **Select Your Version:**
   - Choose your performance from analyzed files, OR
   - Upload your JSON file

3. **Adjust Settings:**
   - **Time Tolerance**: 0.5s (notes within this window match)
   - Higher = more forgiving matching
   - Lower = stricter comparison

4. **Click "🔍 Compare Songs"**

### Understanding Results:

#### **Overall Score**
- **A (90-100%)**: Excellent! Nearly perfect match
- **B (80-89%)**: Very good! Minor differences
- **C (70-79%)**: Good effort, practice specific parts
- **D (60-69%)**: Getting there, focus on problem areas
- **F (< 60%)**: Keep practicing!

#### **Detailed Analysis**

**Note Distribution:**
- Shows notes in both songs
- **Common Notes**: Notes you both hit ✅
- **Missing Notes**: Notes you didn't hit ❌
- **Extra Notes**: Notes you added ➕

**Note Matching:**
- Matched notes count
- Match percentage
- Time differences (how early/late)
- Frequency differences (how sharp/flat)

**Timing Analysis:**
- Average timing accuracy
- Maximum timing difference
- Consistency score

### Example Workflow:

```
Day 1:
1. Analyze original song → Save as "original_song.json"
2. Record yourself singing → Analyze → "my_version_day1.json"
3. Compare: 75% match (Grade C)
4. Review missing notes: F#4, G#4, A4

Day 7:
1. Record again → "my_version_day7.json"
2. Compare: 89% match (Grade B)
3. Progress: +14% improvement! 🎉
```

---

## 4. � Live Microphone Tab

Real-time voice/instrument analysis using your microphone!

**Perfect for:**
- Vocal practice sessions
- Pitch training exercises
- Checking if you can hit notes
- Real-time feedback while singing

### How to Use:

1. **Select Your Microphone:**
   - Dropdown shows all available devices
   - Choose your mic or audio interface
   - Default device selected automatically

2. **Test Your Setup:**
   - Click **"🔊 Test Microphone"**
   - Records 2 seconds
   - Shows audio level
   - Should be > 0.01 for good quality

3. **Configure Recording:**
   - **Duration**: 5-60 seconds (slider)
   - **Pitch Method**: CREPE (best for voice)
   - **Post-Processing**: Enable smoothing ✅

4. **Record Your Voice:**
   - Click **"🔴 Start Recording"**
   - Countdown appears (3, 2, 1...)
   - Sing or play your instrument
   - Progress bar shows time remaining

5. **View Results:**
   - **Audio Level**: Check if loud enough
   - Click **"🎵 Analyze Recording"**
   - See your notes instantly!

### Understanding Results:

**Good Recording:**
- Audio level: 0.01 - 0.1
- Clear notes detected
- Stable pitch line
- Recognizable melody

**Issues:**
- **Level < 0.01**: Too quiet, sing louder or move closer
- **Level > 0.1**: Too loud, might distort
- **No notes**: Background noise or unclear pitch

### Export Options:

- **💾 Save Recording**: Download as WAV file
- **🎹 Export MIDI**: Convert to MIDI for music software
- **📄 Export JSON**: Get note data

### Practice Tips:

**For Beginners:**
```
1. Duration: 10 seconds
2. Sing: Simple scale (C-D-E-F-G)
3. Check: Did you hit each note?
4. Practice: Repeat until accurate
```

**For Intermediate:**
```
1. Duration: 20 seconds
2. Sing: Melody from favorite song
3. Compare: With original (use Compare tab)
4. Improve: Focus on problem notes
```

**For Advanced:**
```
1. Duration: 30-60 seconds
2. Practice: Difficult passages
3. Analyze: Pitch stability and accuracy
4. Export: MIDI for detailed review
```

---

## 🎛️ Advanced Features

### Sidebar Settings

**Pitch Detection Method:**
- **CREPE**: Most accurate, slower (recommended for vocals)
- **Librosa**: Fast, good enough for most uses
- **Aubio**: Alternative method

**Post-Processing:**
- ✅ **Smooth pitch contour**: Removes jitter (recommended)
- ✅ **Remove outliers**: Removes detection errors (recommended)

**Visualizations:**
- ✅ **Show waveform**: See audio signal
- ✅ **Show spectrogram**: Frequency over time
- ⬜ **Show chromagram**: Note energy (advanced)

**Export:**
- ✅ **Export to MIDI**: Creates .mid file
- ✅ **Export to JSON**: Creates .json file

---

## � Tips & Best Practices

### For Best Results:

#### **Audio Quality**
✅ Use quiet environment
✅ Good microphone positioning (6-12 inches)
✅ Clear, sustained notes (hold at least 1 second)
✅ Avoid background music/noise
✅ Record in WAV or high-quality MP3

#### **Recording Settings**
✅ Sample rate: 44100 Hz for music
✅ Enable noise removal if needed
✅ Use CREPE for vocal analysis
✅ Enable smoothing for cleaner results

#### **Analysis Tips**
✅ Start with short recordings (10-20s)
✅ Test microphone before long recordings
✅ Save your work (export JSON/MIDI)
✅ Compare regularly to track progress

### Common Use Cases:

**Learning a Song:**
```
1. Stream YouTube song (Quick Stream)
2. Note the key notes/melody
3. Record yourself (Microphone tab)
4. Compare both versions
5. Practice problem areas
6. Re-record and compare again
```

**Vocal Practice:**
```
1. Warm up with scales
2. Record in Microphone tab (15s)
3. Check note accuracy
4. Practice specific notes that are off
5. Track improvement daily
```

**Music Production:**
```
1. Hum/sing melody idea
2. Record with microphone
3. Export to MIDI
4. Import to your DAW
5. Add instruments/production
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### **❌ "No microphone devices found"**
**Problem:** System can't detect microphone

**Solutions:**
- Check mic is plugged in (USB mics)
- Grant microphone permissions to browser
- Restart the app
- Check System Preferences → Sound → Input
- Try different microphone device

---

#### **❌ "Very low audio level detected"**
**Problem:** Recording volume too low

**Solutions:**
- Sing/speak louder
- Move closer to microphone (6-12 inches)
- Increase mic volume in System Preferences
- Check mic isn't muted
- Test with different microphone

---

#### **❌ "No clear notes detected"**
**Problem:** Can't identify musical notes

**Solutions:**
- Sing more clearly (avoid mumbling)
- Hold notes longer (at least 1 second each)
- Reduce background noise
- Use CREPE pitch detection
- Check mic is working (use test button)

---

#### **❌ "Failed to stream audio"**
**Problem:** Can't access YouTube video

**Solutions:**
- Check video is public (not private/restricted)
- Try "Download and Analyze" instead
- Check internet connection
- Try different video
- Verify URL is correct

---

#### **❌ "FFmpeg not found"**
**Problem:** RAW converter needs FFmpeg

**Solution:**
```bash
# Install FFmpeg on macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

---

#### **❌ Preview/Conversion sounds wrong**
**Problem:** RAW audio settings incorrect

**Solutions:**

**If audio too fast:**
- Reduce sample rate (try 22050 or 16000)

**If audio too slow:**
- Increase sample rate (try 48000)

**If sounds distorted/noisy:**
- Try different format (s24le, s32le)
- Check source recording quality

**If one channel silent:**
- Switch to Mono (1 channel)
- Or try Stereo if using Mono

---

### Performance Issues

#### **Slow Analysis**
- Use Librosa instead of CREPE (faster)
- Disable Spectrogram/Chromagram
- Use Quick Stream for YouTube
- Reduce audio length

#### **App Crashes**
- File too large (keep under 100MB)
- Restart app: `./run.sh`
- Check system resources
- Update dependencies: `./setup.sh`

---

## 📚 Technical Details

### System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- macOS, Linux, or Windows
- Internet connection (for YouTube)

**Recommended:**
- Python 3.13+
- 8GB+ RAM
- SSD storage
- Good microphone

### Dependencies

**Core:**
- `streamlit` - Web interface
- `librosa` - Audio processing
- `numpy` - Numerical computing
- `scipy` - Scientific computing

**Audio:**
- `sounddevice` - Microphone input
- `soundfile` - Audio I/O
- `pydub` - Audio manipulation
- `ffmpeg-python` - Audio conversion

**Analysis:**
- `crepe` - Pitch detection
- `aubio` - Audio analysis
- `pretty-midi` - MIDI export

**Visualization:**
- `matplotlib` - Plotting
- `plotly` - Interactive charts
- `seaborn` - Statistical plots

**Other:**
- `yt-dlp` - YouTube download
- `requests` - HTTP streaming

### File Structure

```
music-analyzer/
├── app.py                      # Main Streamlit app
├── src/
│   ├── audio_processor.py      # Audio loading/streaming
│   ├── pitch_detector.py       # Pitch detection methods
│   ├── note_converter.py       # Frequency → Note conversion
│   ├── visualizer.py           # Chart generation
│   ├── midi_exporter.py        # MIDI file creation
│   ├── song_comparator.py      # Comparison engine
│   ├── microphone_input.py     # Mic recording
│   └── utils.py                # Helper functions
├── outputs/                    # Saved analyses
├── temp/                       # Temporary files
├── requirements.txt            # Python dependencies
├── setup.sh                    # Installation script
└── run.sh                      # Launch script
```

### Output Files

**Saved to `outputs/` folder:**

1. **MIDI Files** (`*_notes.mid`)
   - Standard MIDI format
   - Piano instrument (track 0)
   - Importable to any DAW

2. **JSON Files** (`*_analysis.json`)
   ```json
   {
     "filename": "song.mp3",
     "duration": 123.45,
     "sample_rate": 22050,
     "notes": [
       {
         "note": "C4",
         "frequency": 261.63,
         "time": 0.5,
         "duration": 0.25,
         "confidence": 0.95
       }
     ],
     "metadata": {...}
   }
   ```

3. **Converted Audio** (`converted_*.mp3`)
   - From RAW converter
   - Specified bitrate
   - Ready for analysis

4. **Visualizations** (PNG images)
   - High resolution (300 DPI)
   - Publication quality
   - All generated charts

---

## 🎨 UI Features

### Modern Music Theme

The app features a beautiful, modern UI inspired by Spotify and Apple Music:

✨ **Animated gradient background** - Smooth color transitions
🎨 **Glass morphism effects** - Transparent, blurred containers
🎵 **Large, modern tabs** - Easy navigation with animations
💫 **Hover effects** - Interactive elements with smooth transitions
🌈 **Color-coded visualizations** - Easy to understand charts
✨ **Glowing buttons** - Prominent call-to-action elements

### Tab Navigation

**Four main tabs:**

1. **📥 Input** - Audio source selection
2. **📊 Results** - Analysis visualization
3. **🔍 Compare Songs** - Performance comparison
4. **🎤 Live Mic** - Real-time recording

**Tab features:**
- 75px height (large and easy to click)
- Hover animations (lift up and scale)
- Active tab pulses with glow effect
- Smooth transitions between tabs

---

## 📖 Additional Guides

For more detailed information, check out these guides:

- **QUICKSTART.md** - 5-minute quick start
- **COMPARISON_GUIDE.md** - Song comparison details
- **MICROPHONE_GUIDE.md** - Complete mic feature guide
- **STREAMING_GUIDE.md** - YouTube streaming details
- **API.md** - Developer API documentation

---

## 🤝 Support & Feedback

### Getting Help

**For bugs or issues:**
1. Check [Troubleshooting](#-troubleshooting) section
2. Review existing documentation
3. Create an issue on GitHub

**For feature requests:**
- Open an issue with `[Feature Request]` tag
- Describe use case and expected behavior

### Tips for Success

✅ **Start simple** - Try short recordings first
✅ **Test your setup** - Use mic test feature
✅ **Compare regularly** - Track your progress
✅ **Export your work** - Save JSON/MIDI files
✅ **Practice daily** - Consistency improves accuracy

---

## 📝 Version History

### Current Version Features

**✨ New in Latest Version:**
- 🎨 Modern music-themed UI
- 🎤 Live microphone input
- 🔍 Song comparison system
- ⚡ YouTube quick streaming
- 🔧 RAW to MP3 converter
- ▶️ Audio preview player
- 💫 Enhanced visualizations
- 🎹 Improved MIDI export
- 📊 Better error handling

---

## 📄 License

MIT License - Feel free to use, modify, and distribute!

---

## 🎉 Quick Reference Card

### Essential Commands

```bash
# Install
./setup.sh

# Run app
./run.sh

# Install FFmpeg (for RAW converter)
brew install ffmpeg

# Stop app
Ctrl+C in terminal
```

### Keyboard Shortcuts

- `R` - Reload app
- `Ctrl+C` - Stop app
- `Cmd+W` - Close browser tab

### Best Settings for Common Tasks

**Singing Practice:**
- Pitch: CREPE
- Duration: 15-30s
- Smooth: ✅ ON
- Outliers: ✅ ON

**Instrument Recording:**
- Pitch: CREPE
- Duration: 30-60s
- Smooth: ✅ ON
- Waveform: ✅ ON

**Quick Preview:**
- Method: Quick Stream
- Pitch: Librosa (faster)
- Duration: 60s max

---

## 🌟 Enjoy Your Music Journey!

Whether you're learning to sing, analyzing songs, or practicing an instrument, Music Analyzer is here to help you understand and improve your musical skills!

🎵 **Happy Analyzing!** 🎶

---

*Made with ❤️ for musicians, singers, and music lovers everywhere!*
- ⚡ **Analyze YouTube videos WITHOUT downloading** (NEW!)
- 🚀 **5-10x faster** than traditional download method
- 💾 **Zero disk space** used - streams directly to memory
- 🎬 Shows **video metadata** (title, duration, uploader)
- ⏱️ Analyzes **first 60 seconds** for quick preview
- 📊 All visualizations and exports still available

### 🆕 Song Comparison
- 🔍 **Compare your song with original** to measure accuracy
- 📊 **Overall similarity score** with letter grade (A-F)
- 🎯 **Note-by-note matching** showing which notes match/differ
- ⏱️ **Timing analysis** with accuracy percentage
- 📝 **Detailed reports** in text and JSON formats
- 💡 **Practice feedback** showing missing and extra notes

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio conversion)
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
```bash
cd music-analyzer
```

2. **Install FFmpeg** (required for audio processing)

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html)

3. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

4. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues with `essentia`, you can skip it. The app works without it.

### Running the Application

**Web Interface (Streamlit):**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**Command Line (Test Cases):**
```bash
python test_cases.py
```

## 📖 Usage Guide

### Web Interface

1. **Launch the application**
   ```bash
   streamlit run app.py
   ```

2. **Choose Input Method**
   - **URL**: Paste a YouTube link or direct audio URL
   - **File Upload**: Upload a local audio file

3. **Configure Settings** (in sidebar)
   - Select pitch detection method
   - Enable/disable post-processing
   - Choose visualizations to generate
   - Select export formats

4. **Analyze**
   - Click "Download and Analyze" (for URLs) or "Analyze Audio" (for files)
   - Wait for processing (typically 30-60 seconds)

5. **View Results**
   - Switch to "Results" tab
   - Explore visualizations
   - Download MIDI/JSON exports

6. **Compare Songs** (New!)
   - Switch to "Compare Songs" tab
   - Select original song and your version
   - Get detailed comparison with scores
   - Download comparison reports

### Song Comparison

**Web Interface:**
1. First analyze both songs (original and your version)
2. Go to "Compare Songs" tab
3. Select both JSON files
4. Click "Compare Songs"
5. View detailed similarity scores and reports

**Command Line:**
```bash
# Compare two analyzed songs
python compare_songs.py original_analysis.json my_song_analysis.json

# With custom settings
python compare_songs.py original.json my_song.json \
    --tolerance 0.5 \
    --output report.txt \
    --json results.json
```

See [COMPARISON_GUIDE.md](COMPARISON_GUIDE.md) for detailed documentation.

### Python API

```python
from src.audio_processor import AudioProcessor
from src.pitch_detector import PitchDetector
from src.note_converter import NoteConverter
from src.visualizer import AudioVisualizer
from src.midi_exporter import MidiExporter

# Initialize components
audio_processor = AudioProcessor()
pitch_detector = PitchDetector()
note_converter = NoteConverter()
visualizer = AudioVisualizer()
midi_exporter = MidiExporter()

# Process audio from URL
audio_data, sr, filepath = audio_processor.process_from_url("YOUR_URL_HERE")

# Or from local file
audio_data, sr = audio_processor.process_from_file("path/to/audio.mp3")

# Detect pitch
times, frequencies, confidences = pitch_detector.detect_pitch(
    audio_data, 
    method='crepe'  # or 'librosa', 'aubio'
)

# Convert to notes
notes = note_converter.frequencies_to_notes(frequencies, times)
note_stats = note_converter.get_note_statistics(frequencies, times)

# Create visualizations
visualizer.create_summary_dashboard(
    audio_data, sr, times, frequencies, confidences,
    notes, note_stats,
    output_path="outputs/dashboard.png"
)

# Export to MIDI
segments = note_converter.get_note_segments(frequencies, times)
midi_exporter.create_midi_from_segments(segments, "outputs/melody.mid")
```

## 📂 Project Structure

```
music-analyzer/
├── app.py                 # Streamlit web application
├── requirements.txt       # Python dependencies
├── test_cases.py         # Test suite
├── README.md             # This file
├── .gitignore            # Git ignore rules
│
├── src/                  # Source code modules
│   ├── __init__.py
│   ├── config.py         # Configuration and constants
│   ├── utils.py          # Utility functions
│   ├── audio_processor.py    # Audio loading and conversion
│   ├── pitch_detector.py     # Pitch detection algorithms
│   ├── note_converter.py     # Frequency to note conversion
│   ├── visualizer.py         # Visualization generation
│   └── midi_exporter.py      # MIDI file export
│
├── outputs/              # Generated files (graphs, MIDI, JSON)
└── temp/                 # Temporary downloaded files
```

## 🧪 Test Cases

Run the test suite to verify installation:

```bash
python test_cases.py
```

The test suite includes:
1. **Basic Audio Processing** - Synthetic waveform generation
2. **Pitch Detection** - All three methods
3. **Note Conversion** - Frequency to note mapping
4. **Visualization** - Graph generation
5. **MIDI Export** - File creation
6. **Complete Pipeline** - End-to-end test with C major scale

## 📊 Example Outputs

### Input
- YouTube URL: `https://www.youtube.com/watch?v=...`
- Local file: `song.mp3`

### Generated Files
```
outputs/
├── analysis_20231210_143022_dashboard.png       # Comprehensive dashboard
├── analysis_20231210_143022_pitch.png           # Pitch over time
├── analysis_20231210_143022_notes.png           # Note timeline
├── analysis_20231210_143022_piano_roll.png      # Piano roll
├── analysis_20231210_143022_spectrogram.png     # Frequency spectrogram
├── analysis_20231210_143022_note_distribution.png  # Note histogram
├── analysis_20231210_143022.mid                 # MIDI file
└── analysis_20231210_143022.json                # JSON data
```

### JSON Output Format
```json
{
  "metadata": {
    "timestamp": "20231210_143022",
    "pitch_method": "crepe",
    "sample_rate": 44100,
    "duration": 180.5
  },
  "statistics": {
    "total_notes": 1523,
    "unique_notes": 24,
    "most_common": [["C4", 145], ["D4", 132], ...],
    "octave_range": [3, 5],
    "avg_frequency": 392.5
  },
  "notes": [
    {
      "time": 0.23,
      "note": "C",
      "octave": 4,
      "frequency": 261.6,
      "full_note": "C4"
    },
    ...
  ],
  "segments": [
    {
      "start_time": 0.23,
      "end_time": 0.58,
      "duration": 0.35,
      "note": "C",
      "octave": 4,
      "full_note": "C4",
      "avg_frequency": 261.8
    },
    ...
  ]
}
```

## ⚙️ Configuration

Edit `src/config.py` to customize:

```python
# Audio processing
SAMPLE_RATE = 44100
HOP_LENGTH = 512

# Pitch detection parameters
PITCH_METHODS = {
    'crepe': {
        'model_capacity': 'full',  # 'tiny', 'small', 'medium', 'large', 'full'
        'viterbi': True,
        'step_size': 10
    },
    'librosa': {
        'fmin': 80,   # Minimum frequency
        'fmax': 1200, # Maximum frequency
        'threshold': 0.1
    },
    'aubio': {
        'method': 'yinfft',
        'tolerance': 0.8
    }
}

# MIDI export
MIDI_VELOCITY = 100
MIDI_TEMPO = 120
MIN_NOTE_DURATION = 0.1
```

## 🔧 Troubleshooting

### Common Issues

**1. FFmpeg not found**
```
Error: FFmpeg not installed
```
**Solution:** Install FFmpeg (see Installation section)

**2. CREPE model download fails**
```
Error: Could not download CREPE model
```
**Solution:** Use `librosa` or `aubio` method instead, or ensure stable internet connection

**3. YouTube download fails**
```
Error: Failed to download audio from URL
```
**Solution:** 
- Check URL validity
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Try a different video

**4. Memory error with large files**
```
MemoryError: Unable to allocate array
```
**Solution:** 
- Process shorter audio clips
- Increase system memory
- Use a smaller `model_capacity` for CREPE

**5. Import errors**
```
ModuleNotFoundError: No module named 'XXX'
```
**Solution:** Reinstall requirements: `pip install -r requirements.txt`

## 🎯 Best Practices

### For Best Results

1. **Audio Quality**
   - Use high-quality audio files (320kbps MP3 or lossless formats)
   - Avoid heavily compressed or low-bitrate files

2. **Pitch Detection**
   - **CREPE**: Best for vocals and solo instruments (slower)
   - **Librosa**: Good for general music (faster)
   - **Aubio**: Good for monophonic signals

3. **Content Type**
   - ✅ **Works best with:**
     - Vocals
     - Solo instruments (flute, violin, guitar)
     - Melodies with clear pitch
   
   - ⚠️ **Challenging for:**
     - Polyphonic music (multiple notes simultaneously)
     - Percussion-heavy tracks
     - Very distorted audio

4. **Performance**
   - Limit audio duration to 3-5 minutes for faster processing
   - Enable post-processing for cleaner results
   - Use GPU if available (CREPE benefits from GPU acceleration)

## 🚀 Future Improvements

Potential enhancements you can add:

1. **Multi-track Analysis**
   - Separate instruments using source separation (spleeter)
   - Analyze each track independently

2. **Advanced Music Theory**
   - Chord detection
   - Key signature detection
   - Scale identification
   - Harmony analysis

3. **Machine Learning**
   - Genre classification
   - Instrument recognition
   - Mood detection

4. **Export Formats**
   - MusicXML for sheet music
   - ABC notation
   - Guitar tabs (TAB format)

5. **Real-time Processing**
   - Live microphone input
   - Real-time pitch detection
   - MIDI output to DAW

6. **UI Enhancements**
   - Interactive audio player
   - Editable piano roll
   - Real-time pitch correction

7. **Performance**
   - Parallel processing
   - GPU acceleration
   - Caching for repeated analyses

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues, questions, or suggestions:
- Open an issue in the repository
- Check existing issues for solutions
- Refer to the troubleshooting section

## 🙏 Acknowledgments

This project uses these excellent libraries:
- **Librosa** - Audio analysis
- **CREPE** - Deep learning pitch detection
- **Aubio** - Real-time audio analysis
- **Streamlit** - Web interface
- **yt-dlp** - YouTube downloading
- **pretty_midi** - MIDI file handling
- **Matplotlib/Plotly** - Visualizations

## 📚 References

- [CREPE Paper](https://arxiv.org/abs/1802.06182)
- [Librosa Documentation](https://librosa.org/)
- [Aubio Documentation](https://aubio.org/)
- [Music Theory Basics](https://en.wikipedia.org/wiki/Music_theory)

---

**Made with ❤️ and 🎵**

*Happy Analyzing!* 🎉
# RagaMusikraum
