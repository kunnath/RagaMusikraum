"""
MIDI Export Module
Exports detected notes to MIDI files
"""

import numpy as np
from typing import List, Dict, Optional
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import pretty_midi

from .config import MIDI_VELOCITY, MIDI_TEMPO, MIN_NOTE_DURATION, NOTE_NAMES
from .utils import get_logger

logger = get_logger(__name__)


class MidiExporter:
    """Class for exporting detected notes to MIDI format"""
    
    def __init__(self, tempo: int = MIDI_TEMPO, velocity: int = MIDI_VELOCITY):
        """
        Initialize MidiExporter
        
        Args:
            tempo: MIDI tempo in BPM
            velocity: Note velocity (0-127)
        """
        self.tempo = tempo
        self.velocity = velocity
        
    def create_midi_from_notes(self, notes: List[Dict],
                               output_path: str,
                               method: str = 'mido') -> str:
        """
        Create MIDI file from note list
        
        Args:
            notes: List of note dictionaries
            output_path: Path to save MIDI file
            method: Library to use ('mido' or 'pretty_midi')
            
        Returns:
            Path to saved MIDI file
        """
        if len(notes) == 0:
            logger.warning("No notes to export to MIDI")
            return None
        
        if method == 'mido':
            return self._create_midi_mido(notes, output_path)
        elif method == 'pretty_midi':
            return self._create_midi_pretty(notes, output_path)
        else:
            raise ValueError(f"Unknown MIDI export method: {method}")
    
    def _create_midi_mido(self, notes: List[Dict], output_path: str) -> str:
        """
        Create MIDI file using mido library
        
        Args:
            notes: List of note dictionaries
            output_path: Path to save MIDI file
            
        Returns:
            Path to saved MIDI file
        """
        # Create MIDI file and track
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        
        # Add tempo
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.tempo)))
        
        # Add track name
        track.append(MetaMessage('track_name', name='Detected Melody'))
        
        # Add program change (instrument selection)
        track.append(Message('program_change', program=0, time=0))
        
        # Convert notes to MIDI messages
        current_time = 0
        
        for i, note in enumerate(notes):
            # Calculate MIDI note number
            midi_note = self._note_to_midi_number(note['note'], note['octave'])
            
            if midi_note is None:
                continue
            
            # Calculate delta time (time since last event)
            note_time = note['time']
            delta_time = int((note_time - current_time) * 480)  # Convert to ticks
            
            if delta_time < 0:
                delta_time = 0
            
            # Note on
            track.append(Message('note_on', note=midi_note,
                               velocity=self.velocity, time=delta_time))
            
            # Estimate note duration
            if i < len(notes) - 1:
                duration = notes[i + 1]['time'] - note_time
            else:
                duration = MIN_NOTE_DURATION
            
            duration = max(duration, MIN_NOTE_DURATION)
            duration_ticks = int(duration * 480)
            
            # Note off
            track.append(Message('note_off', note=midi_note,
                               velocity=0, time=duration_ticks))
            
            current_time = note_time + duration
        
        # Save MIDI file
        mid.save(output_path)
        logger.info(f"Saved MIDI file (mido) to {output_path}")
        return output_path
    
    def _create_midi_pretty(self, notes: List[Dict], output_path: str) -> str:
        """
        Create MIDI file using pretty_midi library
        
        Args:
            notes: List of note dictionaries
            output_path: Path to save MIDI file
            
        Returns:
            Path to saved MIDI file
        """
        # Create PrettyMIDI object
        pm = pretty_midi.PrettyMIDI(initial_tempo=self.tempo)
        
        # Create instrument
        instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
        
        # Add notes
        for i, note in enumerate(notes):
            # Calculate MIDI note number
            midi_note = self._note_to_midi_number(note['note'], note['octave'])
            
            if midi_note is None:
                continue
            
            # Estimate note duration
            start_time = note['time']
            
            if i < len(notes) - 1:
                end_time = notes[i + 1]['time']
            else:
                end_time = start_time + MIN_NOTE_DURATION
            
            duration = end_time - start_time
            duration = max(duration, MIN_NOTE_DURATION)
            end_time = start_time + duration
            
            # Create note
            midi_note_obj = pretty_midi.Note(
                velocity=self.velocity,
                pitch=midi_note,
                start=start_time,
                end=end_time
            )
            
            instrument.notes.append(midi_note_obj)
        
        # Add instrument to PrettyMIDI object
        pm.instruments.append(instrument)
        
        # Save MIDI file
        pm.write(output_path)
        logger.info(f"Saved MIDI file (pretty_midi) to {output_path}")
        return output_path
    
    def create_midi_from_segments(self, segments: List[Dict],
                                  output_path: str) -> str:
        """
        Create MIDI file from note segments (more accurate timing)
        
        Args:
            segments: List of note segment dictionaries
            output_path: Path to save MIDI file
            
        Returns:
            Path to saved MIDI file
        """
        if len(segments) == 0:
            logger.warning("No segments to export to MIDI")
            return None
        
        # Create PrettyMIDI object
        pm = pretty_midi.PrettyMIDI(initial_tempo=self.tempo)
        
        # Create instrument
        instrument = pretty_midi.Instrument(program=0)
        
        # Add segments as notes
        for segment in segments:
            midi_note = self._note_to_midi_number(segment['note'], segment['octave'])
            
            if midi_note is None:
                continue
            
            # Create note with exact timing from segment
            midi_note_obj = pretty_midi.Note(
                velocity=self.velocity,
                pitch=midi_note,
                start=segment['start_time'],
                end=segment['end_time']
            )
            
            instrument.notes.append(midi_note_obj)
        
        # Add instrument to PrettyMIDI object
        pm.instruments.append(instrument)
        
        # Save MIDI file
        pm.write(output_path)
        logger.info(f"Saved MIDI file from segments to {output_path}")
        return output_path
    
    def _note_to_midi_number(self, note: str, octave: int) -> Optional[int]:
        """
        Convert note name and octave to MIDI note number
        
        Args:
            note: Note name (C, C#, D, etc.)
            octave: Octave number
            
        Returns:
            MIDI note number (0-127) or None if invalid
        """
        if note not in NOTE_NAMES:
            logger.warning(f"Invalid note name: {note}")
            return None
        
        note_index = NOTE_NAMES.index(note)
        midi_note = (octave + 1) * 12 + note_index
        
        # MIDI note range is 0-127
        if midi_note < 0 or midi_note > 127:
            logger.warning(f"MIDI note out of range: {midi_note}")
            return None
        
        return midi_note
    
    def get_midi_info(self, midi_path: str) -> Dict:
        """
        Get information about a MIDI file
        
        Args:
            midi_path: Path to MIDI file
            
        Returns:
            Dictionary with MIDI file information
        """
        try:
            pm = pretty_midi.PrettyMIDI(midi_path)
            
            total_notes = sum(len(instrument.notes) for instrument in pm.instruments)
            duration = pm.get_end_time()
            
            return {
                'duration': duration,
                'tempo': pm.estimate_tempo(),
                'total_notes': total_notes,
                'n_instruments': len(pm.instruments),
                'time_signature_changes': len(pm.time_signature_changes),
                'key_signature_changes': len(pm.key_signature_changes)
            }
        except Exception as e:
            logger.error(f"Error reading MIDI file: {e}")
            return {}
    
    def create_multi_track_midi(self, note_groups: Dict[str, List[Dict]],
                               output_path: str) -> str:
        """
        Create multi-track MIDI file
        
        Args:
            note_groups: Dictionary mapping track names to note lists
            output_path: Path to save MIDI file
            
        Returns:
            Path to saved MIDI file
        """
        # Create PrettyMIDI object
        pm = pretty_midi.PrettyMIDI(initial_tempo=self.tempo)
        
        # Create instrument for each track
        for track_name, notes in note_groups.items():
            instrument = pretty_midi.Instrument(program=0, name=track_name)
            
            for i, note in enumerate(notes):
                midi_note = self._note_to_midi_number(note['note'], note['octave'])
                
                if midi_note is None:
                    continue
                
                start_time = note['time']
                
                if i < len(notes) - 1:
                    end_time = notes[i + 1]['time']
                else:
                    end_time = start_time + MIN_NOTE_DURATION
                
                duration = end_time - start_time
                duration = max(duration, MIN_NOTE_DURATION)
                end_time = start_time + duration
                
                midi_note_obj = pretty_midi.Note(
                    velocity=self.velocity,
                    pitch=midi_note,
                    start=start_time,
                    end=end_time
                )
                
                instrument.notes.append(midi_note_obj)
            
            pm.instruments.append(instrument)
        
        # Save MIDI file
        pm.write(output_path)
        logger.info(f"Saved multi-track MIDI file to {output_path}")
        return output_path
    
    def quantize_notes(self, notes: List[Dict], 
                      grid: float = 0.25) -> List[Dict]:
        """
        Quantize note timings to a grid
        
        Args:
            notes: List of note dictionaries
            grid: Grid size in seconds (e.g., 0.25 for 16th notes at 120 BPM)
            
        Returns:
            List of quantized notes
        """
        quantized_notes = []
        
        for note in notes:
            quantized_note = note.copy()
            # Round to nearest grid point
            quantized_note['time'] = round(note['time'] / grid) * grid
            quantized_notes.append(quantized_note)
        
        logger.info(f"Quantized {len(notes)} notes to {grid}s grid")
        return quantized_notes
