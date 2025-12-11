# API Documentation

Complete API reference for the Music Analyzer modules.

## Table of Contents
- [AudioProcessor](#audioprocessor)
- [PitchDetector](#pitchdetector)
- [NoteConverter](#noteconverter)
- [AudioVisualizer](#audiovisualizer)
- [MidiExporter](#midiexporter)

---

## AudioProcessor

Handles audio loading, downloading, and preprocessing.

### Initialization

```python
from src.audio_processor import AudioProcessor

processor = AudioProcessor(sample_rate=44100)
```

**Parameters:**
- `sample_rate` (int): Target sample rate for audio processing (default: 44100)

### Methods

#### `process_from_url(url)`

Download and process audio from a URL.

```python
audio_data, sr, filepath = processor.process_from_url("https://youtube.com/...")
```

**Parameters:**
- `url` (str): YouTube URL or direct audio file URL

**Returns:**
- `audio_data` (np.ndarray): Audio signal
- `sr` (int): Sample rate
- `filepath` (str): Path to downloaded file

**Raises:**
- `ValueError`: If URL is invalid or download fails

#### `process_from_file(filepath)`

Load and process audio from a local file.

```python
audio_data, sr = processor.process_from_file("song.mp3")
```

**Parameters:**
- `filepath` (str): Path to audio file

**Returns:**
- `audio_data` (np.ndarray): Audio signal
- `sr` (int): Sample rate

#### `normalize_audio(audio_data)`

Normalize audio to [-1, 1] range.

```python
normalized = processor.normalize_audio(audio_data)
```

#### `trim_silence(audio_data, threshold_db=40)`

Remove silence from beginning and end.

```python
trimmed = processor.trim_silence(audio_data, threshold_db=40)
```

**Parameters:**
- `threshold_db` (float): Threshold in dB for silence detection

#### `get_audio_info(filepath)`

Get metadata about an audio file.

```python
info = processor.get_audio_info("song.mp3")
# Returns: {'duration': 180.5, 'sample_rate': 44100, ...}
```

---

## PitchDetector

Detects pitch in audio using multiple algorithms.

### Initialization

```python
from src.pitch_detector import PitchDetector

detector = PitchDetector(sample_rate=44100)
```

### Methods

#### `detect_pitch(audio_data, method='crepe', **kwargs)`

Detect pitch using specified method.

```python
times, frequencies, confidences = detector.detect_pitch(
    audio_data,
    method='crepe'  # or 'librosa', 'aubio'
)
```

**Parameters:**
- `audio_data` (np.ndarray): Audio signal
- `method` (str): Detection method ('crepe', 'librosa', 'aubio')
- `**kwargs`: Method-specific parameters

**CREPE kwargs:**
- `model_capacity` (str): 'tiny', 'small', 'medium', 'large', 'full'
- `viterbi` (bool): Use Viterbi smoothing
- `step_size` (int): Step size in milliseconds

**Librosa kwargs:**
- `fmin` (float): Minimum frequency (Hz)
- `fmax` (float): Maximum frequency (Hz)
- `threshold` (float): Magnitude threshold

**Aubio kwargs:**
- `method` (str): 'yin', 'yinfft', 'mcomb', 'fcomb', 'schmitt'
- `tolerance` (float): Detection tolerance

**Returns:**
- `times` (np.ndarray): Time points (seconds)
- `frequencies` (np.ndarray): Detected frequencies (Hz)
- `confidences` (np.ndarray): Confidence values (0-1)

#### `post_process_pitch(frequencies, confidences, smooth=True, remove_outliers_flag=True, interpolate=True)`

Clean and smooth detected pitch.

```python
processed = detector.post_process_pitch(
    frequencies,
    confidences,
    smooth=True,
    remove_outliers_flag=True,
    interpolate=True
)
```

**Returns:**
- `frequencies` (np.ndarray): Processed frequencies

#### `get_pitch_statistics(frequencies, confidences)`

Get statistics about detected pitch.

```python
stats = detector.get_pitch_statistics(frequencies, confidences)
```

**Returns dict:**
```python
{
    'mean_frequency': 392.5,
    'median_frequency': 380.2,
    'min_frequency': 220.0,
    'max_frequency': 880.0,
    'std_frequency': 45.3,
    'pitch_coverage': 0.85
}
```

#### `compare_methods(audio_data)`

Compare all pitch detection methods.

```python
results = detector.compare_methods(audio_data)
# Returns: {'crepe': (times, freqs, confs), 'librosa': (...), ...}
```

---

## NoteConverter

Converts frequencies to musical notes.

### Initialization

```python
from src.note_converter import NoteConverter

converter = NoteConverter(a4_frequency=440.0)
```

**Parameters:**
- `a4_frequency` (float): Reference frequency for A4 (default: 440.0 Hz)

### Methods

#### `frequency_to_note(frequency, return_cents=False)`

Convert a single frequency to a note.

```python
note, octave, cents = converter.frequency_to_note(440.0, return_cents=True)
# Returns: ('A', 4, 0.0)
```

**Parameters:**
- `frequency` (float): Frequency in Hz
- `return_cents` (bool): Whether to return cents deviation

**Returns:**
- `note` (str): Note name (C, C#, D, etc.)
- `octave` (int): Octave number
- `cents` (float): Cents deviation (if return_cents=True)

#### `frequencies_to_notes(frequencies, times)`

Convert array of frequencies to notes.

```python
notes = converter.frequencies_to_notes(frequencies, times)
```

**Returns list of dicts:**
```python
[
    {
        'time': 0.23,
        'note': 'C',
        'octave': 4,
        'frequency': 261.6,
        'cents_deviation': 5.2,
        'full_note': 'C4'
    },
    ...
]
```

#### `get_note_segments(frequencies, times, min_duration=0.1)`

Group consecutive same notes into segments.

```python
segments = converter.get_note_segments(frequencies, times, min_duration=0.1)
```

**Returns list of dicts:**
```python
[
    {
        'start_time': 0.23,
        'end_time': 0.58,
        'duration': 0.35,
        'note': 'C',
        'octave': 4,
        'full_note': 'C4',
        'avg_frequency': 261.8
    },
    ...
]
```

#### `get_note_statistics(frequencies, times)`

Get statistics about detected notes.

```python
stats = converter.get_note_statistics(frequencies, times)
```

**Returns dict:**
```python
{
    'total_notes': 1523,
    'unique_notes': 24,
    'most_common': [('C4', 145), ('D4', 132), ...],
    'note_distribution': {'C4': 145, 'D4': 132, ...},
    'octave_range': (3, 5),
    'avg_frequency': 392.5
}
```

#### `note_to_frequency(note, octave)`

Convert note to frequency (inverse operation).

```python
freq = converter.note_to_frequency('A', 4)
# Returns: 440.0
```

#### `create_piano_roll_data(frequencies, times, time_resolution=0.1)`

Create piano roll representation.

```python
piano_roll = converter.create_piano_roll_data(frequencies, times)
```

**Returns dict:**
```python
{
    'times': np.array([0.0, 0.1, 0.2, ...]),
    'notes': range(12, 109),  # MIDI note numbers
    'matrix': np.ndarray  # 2D array (notes × time)
}
```

---

## AudioVisualizer

Creates visualizations for audio analysis.

### Initialization

```python
from src.visualizer import AudioVisualizer

visualizer = AudioVisualizer(figsize=(12, 6), dpi=100)
```

**Parameters:**
- `figsize` (tuple): Default figure size
- `dpi` (int): Resolution for saved images

### Methods

#### `plot_waveform(audio_data, sr, title="Audio Waveform", output_path=None)`

Plot audio waveform.

```python
path = visualizer.plot_waveform(
    audio_data,
    sr,
    title="My Song",
    output_path="waveform.png"
)
```

#### `plot_pitch_over_time(times, frequencies, confidences, title="Pitch Detection", output_path=None)`

Plot detected pitch over time.

```python
path = visualizer.plot_pitch_over_time(
    times,
    frequencies,
    confidences,
    output_path="pitch.png"
)
```

#### `plot_notes_over_time(notes, title="Musical Notes", output_path=None)`

Plot musical notes timeline.

```python
path = visualizer.plot_notes_over_time(
    notes,
    output_path="notes.png"
)
```

#### `plot_piano_roll(piano_roll_data, title="Piano Roll", output_path=None)`

Create piano roll visualization.

```python
path = visualizer.plot_piano_roll(
    piano_roll_data,
    output_path="piano_roll.png"
)
```

#### `plot_spectrogram(audio_data, sr, title="Spectrogram", output_path=None)`

Plot frequency spectrogram.

```python
path = visualizer.plot_spectrogram(
    audio_data,
    sr,
    output_path="spectrogram.png"
)
```

#### `plot_note_distribution(note_stats, title="Note Distribution", output_path=None)`

Plot histogram of note occurrences.

```python
path = visualizer.plot_note_distribution(
    note_stats,
    output_path="distribution.png"
)
```

#### `create_summary_dashboard(audio_data, sr, times, frequencies, confidences, notes, note_stats, output_path=None)`

Create comprehensive dashboard with all visualizations.

```python
path = visualizer.create_summary_dashboard(
    audio_data, sr, times, frequencies,
    confidences, notes, note_stats,
    output_path="dashboard.png"
)
```

#### `create_interactive_pitch_plot(times, frequencies, confidences, notes)`

Create interactive Plotly visualization.

```python
fig = visualizer.create_interactive_pitch_plot(
    times, frequencies, confidences, notes
)
fig.show()  # Display in browser
fig.write_html("interactive.html")  # Save to HTML
```

---

## MidiExporter

Exports detected notes to MIDI format.

### Initialization

```python
from src.midi_exporter import MidiExporter

exporter = MidiExporter(tempo=120, velocity=100)
```

**Parameters:**
- `tempo` (int): MIDI tempo in BPM (default: 120)
- `velocity` (int): Note velocity 0-127 (default: 100)

### Methods

#### `create_midi_from_notes(notes, output_path, method='mido')`

Create MIDI file from note list.

```python
path = exporter.create_midi_from_notes(
    notes,
    "output.mid",
    method='pretty_midi'  # or 'mido'
)
```

**Parameters:**
- `notes` (list): List of note dictionaries
- `output_path` (str): Path to save MIDI file
- `method` (str): Library to use ('mido' or 'pretty_midi')

**Returns:**
- Path to saved MIDI file

#### `create_midi_from_segments(segments, output_path)`

Create MIDI file from note segments (more accurate timing).

```python
path = exporter.create_midi_from_segments(
    segments,
    "output.mid"
)
```

**Parameters:**
- `segments` (list): List of segment dictionaries
- `output_path` (str): Path to save MIDI file

#### `quantize_notes(notes, grid=0.25)`

Quantize note timings to a grid.

```python
quantized = exporter.quantize_notes(notes, grid=0.25)
```

**Parameters:**
- `notes` (list): List of note dictionaries
- `grid` (float): Grid size in seconds (0.25 = 16th notes at 120 BPM)

#### `get_midi_info(midi_path)`

Get information about a MIDI file.

```python
info = exporter.get_midi_info("song.mid")
```

**Returns dict:**
```python
{
    'duration': 180.5,
    'tempo': 120.0,
    'total_notes': 523,
    'n_instruments': 1,
    'time_signature_changes': 0,
    'key_signature_changes': 0
}
```

---

## Complete Example

Here's a full example using all modules:

```python
from src.audio_processor import AudioProcessor
from src.pitch_detector import PitchDetector
from src.note_converter import NoteConverter
from src.visualizer import AudioVisualizer
from src.midi_exporter import MidiExporter

# Initialize
audio_processor = AudioProcessor(sample_rate=44100)
pitch_detector = PitchDetector(sample_rate=44100)
note_converter = NoteConverter(a4_frequency=440.0)
visualizer = AudioVisualizer(figsize=(12, 6), dpi=100)
midi_exporter = MidiExporter(tempo=120, velocity=100)

# Load audio
audio_data, sr = audio_processor.process_from_file("song.mp3")

# Preprocess
audio_data = audio_processor.normalize_audio(audio_data)
audio_data = audio_processor.trim_silence(audio_data)

# Detect pitch
times, frequencies, confidences = pitch_detector.detect_pitch(
    audio_data,
    method='crepe',
    model_capacity='full',
    viterbi=True
)

# Post-process
frequencies = pitch_detector.post_process_pitch(
    frequencies,
    confidences,
    smooth=True,
    remove_outliers_flag=True,
    interpolate=True
)

# Convert to notes
notes = note_converter.frequencies_to_notes(frequencies, times)
segments = note_converter.get_note_segments(frequencies, times)
stats = note_converter.get_note_statistics(frequencies, times)
piano_roll = note_converter.create_piano_roll_data(frequencies, times)

# Create visualizations
visualizer.create_summary_dashboard(
    audio_data, sr, times, frequencies, confidences,
    notes, stats,
    output_path="outputs/dashboard.png"
)

visualizer.plot_pitch_over_time(
    times, frequencies, confidences,
    output_path="outputs/pitch.png"
)

visualizer.plot_piano_roll(
    piano_roll,
    output_path="outputs/piano_roll.png"
)

# Export MIDI
midi_exporter.create_midi_from_segments(
    segments,
    "outputs/melody.mid"
)

# Export JSON
import json
with open("outputs/analysis.json", 'w') as f:
    json.dump({
        'statistics': stats,
        'notes': notes,
        'segments': segments
    }, f, indent=2)

print("Analysis complete!")
print(f"Total notes: {stats['total_notes']}")
print(f"Unique notes: {stats['unique_notes']}")
print(f"Most common: {stats['most_common'][:5]}")
```

---

## Error Handling

All modules raise appropriate exceptions:

```python
try:
    audio_data, sr = processor.process_from_url(url)
except ValueError as e:
    print(f"Error: {e}")
    # Handle invalid URL or download failure

try:
    times, freqs, confs = detector.detect_pitch(audio_data, method='crepe')
except ImportError:
    print("CREPE not installed, using librosa instead")
    times, freqs, confs = detector.detect_pitch(audio_data, method='librosa')
```

---

## Configuration

Customize behavior via `src/config.py`:

```python
# Audio settings
SAMPLE_RATE = 44100
HOP_LENGTH = 512
N_FFT = 2048

# Pitch detection settings
PITCH_METHODS = {
    'crepe': {...},
    'librosa': {...},
    'aubio': {...}
}

# MIDI settings
MIDI_VELOCITY = 100
MIDI_TEMPO = 120
MIN_NOTE_DURATION = 0.1
```

---

## Type Hints

All functions include type hints for better IDE support:

```python
def detect_pitch(
    self,
    audio_data: np.ndarray,
    method: str = 'crepe',
    **kwargs
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    ...
```

---

For more examples, see:
- [example.py](example.py) - Simple usage examples
- [test_cases.py](test_cases.py) - Test suite with examples
- [app.py](app.py) - Full Streamlit application
