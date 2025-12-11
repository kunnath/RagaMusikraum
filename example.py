"""
Simple Example Script
Demonstrates basic usage of the Music Analyzer
"""

import os
import sys
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.audio_processor import AudioProcessor
from src.pitch_detector import PitchDetector
from src.note_converter import NoteConverter
from src.visualizer import AudioVisualizer
from src.midi_exporter import MidiExporter
from src.config import OUTPUT_DIR


def analyze_audio_file(filepath, output_name="example"):
    """
    Analyze an audio file and generate all outputs
    
    Args:
        filepath: Path to audio file
        output_name: Prefix for output files
    """
    
    print("=" * 60)
    print("🎵 MUSIC ANALYZER - Simple Example")
    print("=" * 60)
    print()
    
    # Initialize components
    print("Initializing components...")
    audio_processor = AudioProcessor()
    pitch_detector = PitchDetector()
    note_converter = NoteConverter()
    visualizer = AudioVisualizer()
    midi_exporter = MidiExporter()
    print("✓ Components initialized")
    print()
    
    # Step 1: Load audio
    print("Step 1: Loading audio file...")
    audio_data, sr = audio_processor.process_from_file(filepath)
    duration = len(audio_data) / sr
    print(f"✓ Loaded audio: {duration:.1f}s @ {sr}Hz")
    print()
    
    # Step 2: Preprocess
    print("Step 2: Preprocessing audio...")
    audio_data = audio_processor.normalize_audio(audio_data)
    audio_data = audio_processor.trim_silence(audio_data)
    print("✓ Audio normalized and trimmed")
    print()
    
    # Step 3: Detect pitch
    print("Step 3: Detecting pitch (using librosa)...")
    times, frequencies, confidences = pitch_detector.detect_pitch(
        audio_data,
        method='librosa'
    )
    print(f"✓ Detected pitch in {len(times)} frames")
    print()
    
    # Step 4: Post-process pitch
    print("Step 4: Post-processing pitch...")
    frequencies = pitch_detector.post_process_pitch(
        frequencies,
        confidences,
        smooth=True,
        remove_outliers_flag=True,
        interpolate=True
    )
    print("✓ Pitch post-processed")
    print()
    
    # Step 5: Convert to notes
    print("Step 5: Converting frequencies to notes...")
    notes = note_converter.frequencies_to_notes(frequencies, times)
    segments = note_converter.get_note_segments(frequencies, times, min_duration=0.1)
    stats = note_converter.get_note_statistics(frequencies, times)
    
    print(f"✓ Converted to {len(notes)} notes")
    print(f"✓ Created {len(segments)} note segments")
    print(f"✓ Found {stats['unique_notes']} unique notes")
    print()
    
    # Display statistics
    print("Note Statistics:")
    print(f"  Total notes: {stats['total_notes']}")
    print(f"  Unique notes: {stats['unique_notes']}")
    print(f"  Octave range: {stats['octave_range']}")
    print(f"  Average frequency: {stats['avg_frequency']:.1f} Hz")
    print()
    
    if stats['most_common']:
        print("Most common notes:")
        for note, count in stats['most_common'][:5]:
            print(f"  {note}: {count} times")
    print()
    
    # Step 6: Create visualizations
    print("Step 6: Creating visualizations...")
    output_prefix = os.path.join(OUTPUT_DIR, output_name)
    
    # Dashboard
    dashboard_path = f"{output_prefix}_dashboard.png"
    visualizer.create_summary_dashboard(
        audio_data, sr, times, frequencies, confidences,
        notes, stats,
        output_path=dashboard_path
    )
    print(f"✓ Created dashboard: {dashboard_path}")
    
    # Individual plots
    pitch_path = f"{output_prefix}_pitch.png"
    visualizer.plot_pitch_over_time(times, frequencies, confidences, output_path=pitch_path)
    print(f"✓ Created pitch plot: {pitch_path}")
    
    notes_path = f"{output_prefix}_notes.png"
    visualizer.plot_notes_over_time(notes, output_path=notes_path)
    print(f"✓ Created notes plot: {notes_path}")
    
    piano_roll = note_converter.create_piano_roll_data(frequencies, times)
    piano_roll_path = f"{output_prefix}_piano_roll.png"
    visualizer.plot_piano_roll(piano_roll, output_path=piano_roll_path)
    print(f"✓ Created piano roll: {piano_roll_path}")
    
    dist_path = f"{output_prefix}_distribution.png"
    visualizer.plot_note_distribution(stats, output_path=dist_path)
    print(f"✓ Created note distribution: {dist_path}")
    print()
    
    # Step 7: Export MIDI
    print("Step 7: Exporting to MIDI...")
    midi_path = f"{output_prefix}.mid"
    midi_exporter.create_midi_from_segments(segments, midi_path)
    print(f"✓ Created MIDI file: {midi_path}")
    print()
    
    # Step 8: Export JSON
    print("Step 8: Exporting to JSON...")
    import json
    json_path = f"{output_prefix}.json"
    json_data = {
        'metadata': {
            'source': filepath,
            'duration': duration,
            'sample_rate': sr
        },
        'statistics': stats,
        'notes': notes[:100],  # First 100 notes
        'segments': segments
    }
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"✓ Created JSON file: {json_path}")
    print()
    
    # Complete
    print("=" * 60)
    print("✅ Analysis complete!")
    print("=" * 60)
    print()
    print("Output files created:")
    print(f"  - Dashboard: {dashboard_path}")
    print(f"  - Pitch plot: {pitch_path}")
    print(f"  - Notes plot: {notes_path}")
    print(f"  - Piano roll: {piano_roll_path}")
    print(f"  - Distribution: {dist_path}")
    print(f"  - MIDI file: {midi_path}")
    print(f"  - JSON data: {json_path}")
    print()


def create_synthetic_example():
    """Create and analyze a synthetic C major scale"""
    
    print("Creating synthetic C major scale example...")
    print()
    
    # Create C major scale
    sample_rate = 44100
    duration_per_note = 0.5
    
    # C4, D4, E4, F4, G4, A4, B4, C5
    scale_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
    
    audio_segments = []
    for freq in scale_freqs:
        t = np.linspace(0, duration_per_note, int(sample_rate * duration_per_note))
        # Add some harmonics for richer sound
        segment = (np.sin(2 * np.pi * freq * t) +
                  0.3 * np.sin(2 * np.pi * 2 * freq * t) +
                  0.1 * np.sin(2 * np.pi * 3 * freq * t))
        # Apply envelope
        envelope = np.exp(-2 * t / duration_per_note)
        segment = segment * envelope
        audio_segments.append(segment)
    
    audio_data = np.concatenate(audio_segments)
    
    # Save to temp file
    import soundfile as sf
    temp_path = os.path.join("temp", "synthetic_scale.wav")
    sf.write(temp_path, audio_data, sample_rate)
    
    print(f"✓ Created synthetic scale: {temp_path}")
    print()
    
    # Analyze it
    analyze_audio_file(temp_path, "synthetic_example")


if __name__ == "__main__":
    print()
    print("🎵 Music Analyzer - Simple Example Script")
    print()
    
    if len(sys.argv) > 1:
        # Analyze provided file
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            analyze_audio_file(filepath)
        else:
            print(f"Error: File not found: {filepath}")
    else:
        # Create and analyze synthetic example
        print("No audio file provided. Creating synthetic example...")
        print()
        create_synthetic_example()
        print()
        print("To analyze your own file, run:")
        print("  python example.py path/to/your/audio.mp3")
        print()
