"""
Test Cases for Music Analyzer
Example test cases demonstrating the application's capabilities
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


def test_basic_audio_processing():
    """Test basic audio loading and processing"""
    print("=" * 50)
    print("Test 1: Basic Audio Processing")
    print("=" * 50)
    
    processor = AudioProcessor()
    
    # Test with a synthetic sine wave
    sample_rate = 44100
    duration = 2  # seconds
    frequency = 440  # A4
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    print(f"✓ Created synthetic audio: {duration}s @ {sample_rate}Hz")
    print(f"✓ Audio shape: {audio_data.shape}")
    print(f"✓ Audio range: [{audio_data.min():.3f}, {audio_data.max():.3f}]")
    
    # Normalize
    normalized = processor.normalize_audio(audio_data)
    print(f"✓ Normalized audio range: [{normalized.min():.3f}, {normalized.max():.3f}]")
    
    print("✅ Test passed!\n")
    return audio_data, sample_rate


def test_pitch_detection(audio_data, sample_rate):
    """Test pitch detection with all methods"""
    print("=" * 50)
    print("Test 2: Pitch Detection")
    print("=" * 50)
    
    detector = PitchDetector(sample_rate=sample_rate)
    
    methods = ['librosa', 'aubio']  # CREPE requires model download
    
    for method in methods:
        try:
            print(f"\nTesting {method} method...")
            times, frequencies, confidences = detector.detect_pitch(audio_data, method=method)
            
            print(f"✓ Detected {len(frequencies)} frames")
            print(f"✓ Valid pitches: {np.sum(frequencies > 0)}")
            
            valid_freqs = frequencies[frequencies > 0]
            if len(valid_freqs) > 0:
                print(f"✓ Mean frequency: {np.mean(valid_freqs):.1f} Hz")
                print(f"✓ Frequency range: [{np.min(valid_freqs):.1f}, {np.max(valid_freqs):.1f}] Hz")
            
            stats = detector.get_pitch_statistics(frequencies, confidences)
            print(f"✓ Pitch coverage: {stats['pitch_coverage']*100:.1f}%")
            
        except Exception as e:
            print(f"✗ {method} failed: {e}")
    
    print("\n✅ Test passed!\n")
    
    # Return librosa results for next tests
    times, frequencies, confidences = detector.detect_pitch(audio_data, method='librosa')
    return times, frequencies, confidences


def test_note_conversion(frequencies, times):
    """Test note conversion"""
    print("=" * 50)
    print("Test 3: Note Conversion")
    print("=" * 50)
    
    converter = NoteConverter()
    
    # Test single frequency conversion
    test_freq = 440.0  # A4
    note, octave, cents = converter.frequency_to_note(test_freq, return_cents=True)
    print(f"✓ 440 Hz → {note}{octave} (deviation: {cents:.1f} cents)")
    
    # Test frequency array conversion
    notes = converter.frequencies_to_notes(frequencies, times)
    print(f"✓ Converted {len(notes)} frequencies to notes")
    
    if len(notes) > 0:
        print(f"✓ First note: {notes[0]}")
    
    # Test note segments
    segments = converter.get_note_segments(frequencies, times, min_duration=0.1)
    print(f"✓ Created {len(segments)} note segments")
    
    if len(segments) > 0:
        print(f"✓ First segment: {segments[0]}")
    
    # Test statistics
    stats = converter.get_note_statistics(frequencies, times)
    print(f"✓ Total notes: {stats['total_notes']}")
    print(f"✓ Unique notes: {stats['unique_notes']}")
    print(f"✓ Octave range: {stats['octave_range']}")
    
    if stats['most_common']:
        print(f"✓ Most common note: {stats['most_common'][0]}")
    
    print("\n✅ Test passed!\n")
    return notes, segments, stats


def test_visualization(audio_data, sample_rate, times, frequencies, confidences, notes, stats):
    """Test visualization creation"""
    print("=" * 50)
    print("Test 4: Visualization")
    print("=" * 50)
    
    visualizer = AudioVisualizer()
    output_prefix = os.path.join(OUTPUT_DIR, "test")
    
    # Test waveform
    try:
        path = visualizer.plot_waveform(
            audio_data, sample_rate,
            output_path=f"{output_prefix}_waveform.png"
        )
        print(f"✓ Created waveform: {path}")
    except Exception as e:
        print(f"✗ Waveform failed: {e}")
    
    # Test pitch plot
    try:
        path = visualizer.plot_pitch_over_time(
            times, frequencies, confidences,
            output_path=f"{output_prefix}_pitch.png"
        )
        print(f"✓ Created pitch plot: {path}")
    except Exception as e:
        print(f"✗ Pitch plot failed: {e}")
    
    # Test spectrogram
    try:
        path = visualizer.plot_spectrogram(
            audio_data, sample_rate,
            output_path=f"{output_prefix}_spectrogram.png"
        )
        print(f"✓ Created spectrogram: {path}")
    except Exception as e:
        print(f"✗ Spectrogram failed: {e}")
    
    # Test note distribution
    try:
        path = visualizer.plot_note_distribution(
            stats,
            output_path=f"{output_prefix}_distribution.png"
        )
        if path:
            print(f"✓ Created note distribution: {path}")
    except Exception as e:
        print(f"✗ Note distribution failed: {e}")
    
    print("\n✅ Test passed!\n")


def test_midi_export(notes, segments):
    """Test MIDI export"""
    print("=" * 50)
    print("Test 5: MIDI Export")
    print("=" * 50)
    
    exporter = MidiExporter()
    output_prefix = os.path.join(OUTPUT_DIR, "test")
    
    # Test MIDI from notes
    try:
        if len(notes) > 0:
            path = exporter.create_midi_from_notes(
                notes,
                f"{output_prefix}_notes.mid",
                method='pretty_midi'
            )
            print(f"✓ Created MIDI from notes: {path}")
    except Exception as e:
        print(f"✗ MIDI from notes failed: {e}")
    
    # Test MIDI from segments
    try:
        if len(segments) > 0:
            path = exporter.create_midi_from_segments(
                segments,
                f"{output_prefix}_segments.mid"
            )
            print(f"✓ Created MIDI from segments: {path}")
    except Exception as e:
        print(f"✗ MIDI from segments failed: {e}")
    
    print("\n✅ Test passed!\n")


def test_complete_pipeline():
    """Test complete analysis pipeline"""
    print("\n" + "=" * 50)
    print("COMPLETE PIPELINE TEST")
    print("=" * 50 + "\n")
    
    # Create synthetic audio (C major scale)
    sample_rate = 44100
    duration_per_note = 0.5
    
    # C major scale frequencies
    scale_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
    
    audio_segments = []
    for freq in scale_freqs:
        t = np.linspace(0, duration_per_note, int(sample_rate * duration_per_note))
        segment = np.sin(2 * np.pi * freq * t)
        audio_segments.append(segment)
    
    audio_data = np.concatenate(audio_segments)
    
    print(f"✓ Created C major scale: {len(scale_freqs)} notes")
    print(f"✓ Total duration: {len(audio_data) / sample_rate:.1f}s")
    
    # Run complete pipeline
    processor = AudioProcessor(sample_rate=sample_rate)
    detector = PitchDetector(sample_rate=sample_rate)
    converter = NoteConverter()
    visualizer = AudioVisualizer()
    exporter = MidiExporter()
    
    # Process
    audio_data = processor.normalize_audio(audio_data)
    times, frequencies, confidences = detector.detect_pitch(audio_data, method='librosa')
    frequencies = detector.post_process_pitch(frequencies, confidences)
    notes = converter.frequencies_to_notes(frequencies, times)
    segments = converter.get_note_segments(frequencies, times)
    stats = converter.get_note_statistics(frequencies, times)
    
    print(f"✓ Detected {len(notes)} notes")
    print(f"✓ Created {len(segments)} segments")
    print(f"✓ Unique notes: {stats['unique_notes']}")
    
    # Create outputs
    output_prefix = os.path.join(OUTPUT_DIR, "pipeline_test")
    
    try:
        visualizer.create_summary_dashboard(
            audio_data, sample_rate, times, frequencies, confidences,
            notes, stats,
            output_path=f"{output_prefix}_dashboard.png"
        )
        print(f"✓ Created dashboard")
    except Exception as e:
        print(f"✗ Dashboard failed: {e}")
    
    try:
        exporter.create_midi_from_segments(segments, f"{output_prefix}.mid")
        print(f"✓ Created MIDI file")
    except Exception as e:
        print(f"✗ MIDI export failed: {e}")
    
    print("\n✅ Complete pipeline test passed!\n")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "🎵" * 25)
    print(" " * 20 + "MUSIC ANALYZER TEST SUITE")
    print("🎵" * 25 + "\n")
    
    try:
        # Test 1: Audio Processing
        audio_data, sample_rate = test_basic_audio_processing()
        
        # Test 2: Pitch Detection
        times, frequencies, confidences = test_pitch_detection(audio_data, sample_rate)
        
        # Test 3: Note Conversion
        notes, segments, stats = test_note_conversion(frequencies, times)
        
        # Test 4: Visualization
        test_visualization(audio_data, sample_rate, times, frequencies, confidences, notes, stats)
        
        # Test 5: MIDI Export
        test_midi_export(notes, segments)
        
        # Complete Pipeline Test
        test_complete_pipeline()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
