"""
Configuration file for Music Analyzer application
Contains all constants, settings, and parameters
"""

import os

# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# Create directories if they don't exist
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Audio processing settings
SAMPLE_RATE = 44100  # Hz
N_FFT = 2048
HOP_LENGTH = 512
N_MELS = 128

# Pitch detection settings
PITCH_METHODS = {
    'crepe': {
        'model_capacity': 'full',  # Options: 'tiny', 'small', 'medium', 'large', 'full'
        'viterbi': True,
        'step_size': 10  # milliseconds
    },
    'librosa': {
        'fmin': 80,  # Minimum frequency (Hz) - roughly E2
        'fmax': 1200,  # Maximum frequency (Hz) - roughly D6
        'threshold': 0.1
    },
    'aubio': {
        'method': 'yinfft',  # Options: 'yin', 'yinfft', 'mcomb', 'fcomb', 'schmitt'
        'buf_size': 2048,
        'hop_size': 512,
        'samplerate': SAMPLE_RATE,
        'tolerance': 0.8
    }
}

# Note conversion settings
A4_FREQUENCY = 440.0  # Hz
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
CENTS_TOLERANCE = 50  # Cents within which to snap to nearest note

# MIDI settings
MIDI_VELOCITY = 100  # Default velocity (0-127)
MIDI_TEMPO = 120  # BPM
MIN_NOTE_DURATION = 0.1  # seconds

# Visualization settings
FIGURE_SIZE = (12, 6)
DPI = 100
COLORMAP = 'viridis'

# URL download settings
DOWNLOAD_FORMAT = 'bestaudio/best'
MAX_DOWNLOAD_SIZE = 100 * 1024 * 1024  # 100 MB

# Supported audio formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.wma']

# Error messages
ERROR_MESSAGES = {
    'invalid_url': 'Invalid URL provided. Please check and try again.',
    'download_failed': 'Failed to download audio from URL.',
    'processing_failed': 'Failed to process audio file.',
    'no_pitch_detected': 'No clear pitch detected in the audio. Try a different file.',
    'format_not_supported': f'Audio format not supported. Supported formats: {", ".join(SUPPORTED_FORMATS)}'
}
