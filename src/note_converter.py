"""
Note Conversion Module
Converts frequencies to musical notes
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from collections import Counter

from .config import A4_FREQUENCY, NOTE_NAMES, CENTS_TOLERANCE
from .utils import get_logger

logger = get_logger(__name__)


class NoteConverter:
    """Class for converting frequencies to musical notes"""
    
    def __init__(self, a4_frequency: float = A4_FREQUENCY):
        """
        Initialize NoteConverter
        
        Args:
            a4_frequency: Reference frequency for A4 (default 440 Hz)
        """
        self.a4_frequency = a4_frequency
        self.note_names = NOTE_NAMES
        
    def frequency_to_note(self, frequency: float, 
                         return_cents: bool = False) -> Tuple[Optional[str], Optional[int], Optional[float]]:
        """
        Convert a frequency to a musical note
        
        Args:
            frequency: Frequency in Hz
            return_cents: Whether to return cents deviation
            
        Returns:
            Tuple of (note_name, octave, cents_deviation)
            Returns (None, None, None) if frequency is 0 or invalid
        """
        if frequency <= 0 or np.isnan(frequency):
            return (None, None, None)
        
        # Calculate the number of half steps from A4
        half_steps_from_a4 = 12 * np.log2(frequency / self.a4_frequency)
        
        # Round to nearest half step
        nearest_half_step = round(half_steps_from_a4)
        
        # Calculate cents deviation
        cents_deviation = 100 * (half_steps_from_a4 - nearest_half_step)
        
        # Calculate note index and octave
        # A4 is MIDI note 69 (octave 4, note index 9)
        midi_note = 69 + nearest_half_step
        octave = (midi_note // 12) - 1
        note_index = midi_note % 12
        
        note_name = self.note_names[note_index]
        
        if return_cents:
            return (note_name, int(octave), cents_deviation)
        else:
            return (note_name, int(octave), None)
    
    def frequencies_to_notes(self, frequencies: np.ndarray,
                            times: np.ndarray) -> List[Dict]:
        """
        Convert array of frequencies to notes with timing
        
        Args:
            frequencies: Array of frequencies
            times: Array of corresponding timestamps
            
        Returns:
            List of note dictionaries with time, note, octave, frequency
        """
        notes = []
        
        for time, freq in zip(times, frequencies):
            note_name, octave, cents = self.frequency_to_note(freq, return_cents=True)
            
            if note_name is not None:
                notes.append({
                    'time': float(time),
                    'note': note_name,
                    'octave': octave,
                    'frequency': float(freq),
                    'cents_deviation': cents,
                    'full_note': f"{note_name}{octave}"
                })
        
        logger.info(f"Converted {len(notes)} frequencies to notes")
        return notes
    
    def get_note_segments(self, frequencies: np.ndarray,
                         times: np.ndarray,
                         min_duration: float = 0.1) -> List[Dict]:
        """
        Group consecutive same notes into segments
        
        Args:
            frequencies: Array of frequencies
            times: Array of corresponding timestamps
            min_duration: Minimum duration for a segment (seconds)
            
        Returns:
            List of note segment dictionaries
        """
        if len(frequencies) == 0:
            return []
        
        segments = []
        current_note = None
        current_octave = None
        start_time = None
        start_freq = []
        
        for i, (time, freq) in enumerate(zip(times, frequencies)):
            note_name, octave, _ = self.frequency_to_note(freq)
            
            if note_name is None:
                # Gap in notes
                if current_note is not None:
                    duration = time - start_time
                    if duration >= min_duration:
                        segments.append({
                            'start_time': start_time,
                            'end_time': time,
                            'duration': duration,
                            'note': current_note,
                            'octave': current_octave,
                            'full_note': f"{current_note}{current_octave}",
                            'avg_frequency': np.mean(start_freq)
                        })
                    current_note = None
                    current_octave = None
                    start_freq = []
            else:
                if note_name != current_note or octave != current_octave:
                    # Note changed
                    if current_note is not None:
                        duration = time - start_time
                        if duration >= min_duration:
                            segments.append({
                                'start_time': start_time,
                                'end_time': time,
                                'duration': duration,
                                'note': current_note,
                                'octave': current_octave,
                                'full_note': f"{current_note}{current_octave}",
                                'avg_frequency': np.mean(start_freq)
                            })
                    
                    # Start new segment
                    current_note = note_name
                    current_octave = octave
                    start_time = time
                    start_freq = [freq]
                else:
                    # Same note continues
                    start_freq.append(freq)
        
        # Add final segment
        if current_note is not None and len(times) > 0:
            duration = times[-1] - start_time
            if duration >= min_duration:
                segments.append({
                    'start_time': start_time,
                    'end_time': times[-1],
                    'duration': duration,
                    'note': current_note,
                    'octave': current_octave,
                    'full_note': f"{current_note}{current_octave}",
                    'avg_frequency': np.mean(start_freq)
                })
        
        logger.info(f"Created {len(segments)} note segments")
        return segments
    
    def get_note_statistics(self, frequencies: np.ndarray,
                           times: np.ndarray) -> Dict:
        """
        Get statistics about detected notes
        
        Args:
            frequencies: Array of frequencies
            times: Array of timestamps
            
        Returns:
            Dictionary of note statistics
        """
        notes = self.frequencies_to_notes(frequencies, times)
        
        if len(notes) == 0:
            return {
                'total_notes': 0,
                'unique_notes': 0,
                'most_common': [],
                'note_distribution': {},
                'octave_range': None
            }
        
        # Count note occurrences
        full_notes = [n['full_note'] for n in notes]
        note_counter = Counter(full_notes)
        
        # Get octave range
        octaves = [n['octave'] for n in notes]
        octave_range = (min(octaves), max(octaves))
        
        # Get most common notes
        most_common = note_counter.most_common(10)
        
        return {
            'total_notes': len(notes),
            'unique_notes': len(note_counter),
            'most_common': most_common,
            'note_distribution': dict(note_counter),
            'octave_range': octave_range,
            'avg_frequency': float(np.mean([n['frequency'] for n in notes]))
        }
    
    def note_to_frequency(self, note: str, octave: int) -> float:
        """
        Convert a note name and octave to frequency
        
        Args:
            note: Note name (C, C#, D, etc.)
            octave: Octave number
            
        Returns:
            Frequency in Hz
        """
        if note not in self.note_names:
            raise ValueError(f"Invalid note: {note}")
        
        # Calculate MIDI note number
        note_index = self.note_names.index(note)
        midi_note = (octave + 1) * 12 + note_index
        
        # Calculate frequency
        # MIDI note 69 = A4 = 440 Hz
        half_steps_from_a4 = midi_note - 69
        frequency = self.a4_frequency * (2 ** (half_steps_from_a4 / 12))
        
        return frequency
    
    def get_scale_notes(self, root: str, scale_type: str = 'major') -> List[str]:
        """
        Get notes in a musical scale
        
        Args:
            root: Root note
            scale_type: Type of scale ('major', 'minor', 'chromatic')
            
        Returns:
            List of note names in scale
        """
        if root not in self.note_names:
            raise ValueError(f"Invalid root note: {root}")
        
        root_index = self.note_names.index(root)
        
        # Scale intervals (in half steps)
        intervals = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'chromatic': list(range(12))
        }
        
        if scale_type not in intervals:
            raise ValueError(f"Unknown scale type: {scale_type}")
        
        scale_notes = []
        for interval in intervals[scale_type]:
            note_index = (root_index + interval) % 12
            scale_notes.append(self.note_names[note_index])
        
        return scale_notes
    
    def detect_key(self, frequencies: np.ndarray, times: np.ndarray) -> Dict:
        """
        Attempt to detect the musical key of the piece
        
        Args:
            frequencies: Array of frequencies
            times: Array of timestamps
            
        Returns:
            Dictionary with detected key information
        """
        notes = self.frequencies_to_notes(frequencies, times)
        
        if len(notes) == 0:
            return {'detected_key': None, 'confidence': 0}
        
        # Count note occurrences (without octave)
        note_names = [n['note'] for n in notes]
        note_counter = Counter(note_names)
        
        # Find most common note (likely tonic or dominant)
        most_common_note = note_counter.most_common(1)[0][0]
        
        # Simple key detection: assume most common note is tonic
        # In reality, this would need more sophisticated analysis
        return {
            'detected_key': most_common_note,
            'confidence': 0.5,  # Low confidence without proper key detection
            'note_distribution': dict(note_counter)
        }
    
    def create_piano_roll_data(self, frequencies: np.ndarray,
                               times: np.ndarray,
                               time_resolution: float = 0.1) -> Dict:
        """
        Create piano roll representation
        
        Args:
            frequencies: Array of frequencies
            times: Array of timestamps
            time_resolution: Time resolution in seconds
            
        Returns:
            Dictionary with piano roll data
        """
        if len(frequencies) == 0 or len(times) == 0:
            return {'times': [], 'notes': [], 'matrix': np.array([])}
        
        # Create time bins
        max_time = times[-1]
        time_bins = np.arange(0, max_time + time_resolution, time_resolution)
        
        # Create note index mapping (C0 to C8, MIDI notes 12-108)
        note_range = range(12, 109)  # MIDI notes
        
        # Initialize piano roll matrix
        piano_roll = np.zeros((len(note_range), len(time_bins)))
        
        # Fill piano roll
        for time, freq in zip(times, frequencies):
            note_name, octave, _ = self.frequency_to_note(freq)
            
            if note_name is not None:
                # Calculate MIDI note
                note_index = self.note_names.index(note_name)
                midi_note = (octave + 1) * 12 + note_index
                
                if midi_note in note_range:
                    # Find time bin
                    time_bin = int(time / time_resolution)
                    if time_bin < len(time_bins):
                        note_position = midi_note - 12
                        piano_roll[note_position, time_bin] = 1
        
        return {
            'times': time_bins,
            'notes': note_range,
            'matrix': piano_roll
        }
