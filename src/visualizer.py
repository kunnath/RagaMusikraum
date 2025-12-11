"""
Visualization Module
Creates graphs and visualizations for audio analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import librosa
import librosa.display
from typing import Optional, List, Dict
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from .config import FIGURE_SIZE, DPI, COLORMAP, SAMPLE_RATE, HOP_LENGTH
from .utils import get_logger, format_time

logger = get_logger(__name__)


class AudioVisualizer:
    """Class for creating audio analysis visualizations"""
    
    def __init__(self, figsize: tuple = FIGURE_SIZE, dpi: int = DPI):
        """
        Initialize AudioVisualizer
        
        Args:
            figsize: Default figure size
            dpi: Default DPI for saving figures
        """
        self.figsize = figsize
        self.dpi = dpi
        
    def plot_waveform(self, audio_data: np.ndarray, sr: int,
                     title: str = "Audio Waveform",
                     output_path: Optional[str] = None) -> str:
        """
        Plot audio waveform
        
        Args:
            audio_data: Audio signal
            sr: Sample rate
            title: Plot title
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        times = np.arange(len(audio_data)) / sr
        ax.plot(times, audio_data, linewidth=0.5)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved waveform plot to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_pitch_over_time(self, times: np.ndarray, frequencies: np.ndarray,
                            confidences: np.ndarray,
                            title: str = "Pitch Detection Over Time",
                            output_path: Optional[str] = None) -> str:
        """
        Plot detected pitch over time
        
        Args:
            times: Time array
            frequencies: Frequency array
            confidences: Confidence array
            title: Plot title
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], self.figsize[1] * 1.5))
        
        # Filter out zero frequencies
        mask = frequencies > 0
        
        # Plot frequencies
        ax1.scatter(times[mask], frequencies[mask], c=confidences[mask],
                   cmap=COLORMAP, alpha=0.6, s=10)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Frequency (Hz)')
        ax1.set_title(title)
        ax1.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(ax1.collections[0], ax=ax1)
        cbar.set_label('Confidence')
        
        # Plot confidence
        ax2.plot(times, confidences, color='blue', linewidth=1)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Confidence')
        ax2.set_title('Detection Confidence')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1])
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved pitch plot to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_notes_over_time(self, notes: List[Dict],
                            title: str = "Musical Notes Over Time",
                            output_path: Optional[str] = None) -> str:
        """
        Plot musical notes over time (piano roll style)
        
        Args:
            notes: List of note dictionaries
            title: Plot title
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        if len(notes) == 0:
            logger.warning("No notes to plot")
            return None
        
        fig, ax = plt.subplots(figsize=(self.figsize[0], 8))
        
        # Create note to y-position mapping
        def note_sort_key(note_str):
            """Extract octave and note name for sorting. Handles notes like C4, C#4, Db3, etc."""
            import re
            # Extract octave number (last digits in the string)
            match = re.search(r'(-?\d+)$', note_str)
            octave = int(match.group(1)) if match else 0
            # Get note name (everything except the octave number)
            note_name = re.sub(r'(-?\d+)$', '', note_str)
            return (octave, note_name)
        
        unique_notes = sorted(set(n['full_note'] for n in notes), key=note_sort_key)
        note_to_y = {note: i for i, note in enumerate(unique_notes)}
        
        # Plot notes
        for note in notes:
            y_pos = note_to_y[note['full_note']]
            ax.scatter(note['time'], y_pos, c='blue', s=20, alpha=0.6)
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Note')
        ax.set_yticks(range(len(unique_notes)))
        ax.set_yticklabels(unique_notes)
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved notes plot to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_piano_roll(self, piano_roll_data: Dict,
                       title: str = "Piano Roll Visualization",
                       output_path: Optional[str] = None) -> str:
        """
        Create piano roll visualization
        
        Args:
            piano_roll_data: Dictionary with times, notes, and matrix
            title: Plot title
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        matrix = piano_roll_data['matrix']
        
        if matrix.size == 0:
            logger.warning("Empty piano roll data")
            return None
        
        fig, ax = plt.subplots(figsize=(self.figsize[0], 10))
        
        # Plot piano roll
        im = ax.imshow(matrix, aspect='auto', origin='lower',
                      cmap='binary', interpolation='nearest')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('MIDI Note')
        ax.set_title(title)
        
        # Set y-axis labels for octaves
        notes = piano_roll_data['notes']
        y_ticks = [i for i in range(0, len(notes), 12)]
        y_labels = [f"C{(note//12)-1}" for i, note in enumerate(notes) if i % 12 == 0]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved piano roll to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_spectrogram(self, audio_data: np.ndarray, sr: int,
                        title: str = "Spectrogram",
                        output_path: Optional[str] = None) -> str:
        """
        Plot spectrogram
        
        Args:
            audio_data: Audio signal
            sr: Sample rate
            title: Plot title
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Compute spectrogram
        D = librosa.amplitude_to_db(
            np.abs(librosa.stft(audio_data, hop_length=HOP_LENGTH)),
            ref=np.max
        )
        
        img = librosa.display.specshow(D, sr=sr, hop_length=HOP_LENGTH,
                                       x_axis='time', y_axis='hz',
                                       cmap=COLORMAP, ax=ax)
        
        ax.set_title(title)
        ax.set_ylabel('Frequency (Hz)')
        ax.set_xlabel('Time (s)')
        
        fig.colorbar(img, ax=ax, format='%+2.0f dB')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved spectrogram to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_chromagram(self, audio_data: np.ndarray, sr: int,
                       title: str = "Chromagram",
                       output_path: Optional[str] = None) -> str:
        """
        Plot chromagram (pitch class representation)
        
        Args:
            audio_data: Audio signal
            sr: Sample rate
            title: Plot title
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Compute chromagram
        chroma = librosa.feature.chroma_cqt(y=audio_data, sr=sr, hop_length=HOP_LENGTH)
        
        img = librosa.display.specshow(chroma, sr=sr, hop_length=HOP_LENGTH,
                                       x_axis='time', y_axis='chroma',
                                       cmap=COLORMAP, ax=ax)
        
        ax.set_title(title)
        ax.set_ylabel('Pitch Class')
        ax.set_xlabel('Time (s)')
        
        fig.colorbar(img, ax=ax)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved chromagram to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_note_distribution(self, note_stats: Dict,
                              title: str = "Note Distribution",
                              output_path: Optional[str] = None) -> str:
        """
        Plot note distribution
        
        Args:
            note_stats: Note statistics dictionary
            title: Plot title
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        if not note_stats.get('note_distribution'):
            logger.warning("No note distribution data")
            return None
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        notes = list(note_stats['note_distribution'].keys())
        counts = list(note_stats['note_distribution'].values())
        
        # Sort by count
        sorted_pairs = sorted(zip(notes, counts), key=lambda x: x[1], reverse=True)
        notes, counts = zip(*sorted_pairs) if sorted_pairs else ([], [])
        
        # Plot top 20
        top_n = min(20, len(notes))
        ax.bar(range(top_n), counts[:top_n])
        ax.set_xticks(range(top_n))
        ax.set_xticklabels(notes[:top_n], rotation=45, ha='right')
        ax.set_xlabel('Note')
        ax.set_ylabel('Count')
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved note distribution to {output_path}")
        
        plt.close()
        return output_path
    
    def create_interactive_pitch_plot(self, times: np.ndarray,
                                     frequencies: np.ndarray,
                                     confidences: np.ndarray,
                                     notes: List[Dict]) -> go.Figure:
        """
        Create interactive pitch plot using Plotly
        
        Args:
            times: Time array
            frequencies: Frequency array
            confidences: Confidence array
            notes: List of note dictionaries
            
        Returns:
            Plotly Figure object
        """
        # Filter valid data
        mask = frequencies > 0
        
        # Create figure with subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Pitch Detection', 'Detection Confidence'),
            vertical_spacing=0.12,
            row_heights=[0.7, 0.3]
        )
        
        # Pitch scatter plot
        fig.add_trace(
            go.Scatter(
                x=times[mask],
                y=frequencies[mask],
                mode='markers',
                marker=dict(
                    size=5,
                    color=confidences[mask],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Confidence", y=0.75)
                ),
                name='Detected Pitch',
                hovertemplate='Time: %{x:.2f}s<br>Frequency: %{y:.1f}Hz<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Add note labels
        if notes:
            note_times = [n['time'] for n in notes[::10]]  # Sample every 10th note
            note_freqs = [n['frequency'] for n in notes[::10]]
            note_labels = [n['full_note'] for n in notes[::10]]
            
            fig.add_trace(
                go.Scatter(
                    x=note_times,
                    y=note_freqs,
                    mode='text',
                    text=note_labels,
                    textfont=dict(size=8),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=1, col=1
            )
        
        # Confidence line plot
        fig.add_trace(
            go.Scatter(
                x=times,
                y=confidences,
                mode='lines',
                line=dict(color='blue', width=1),
                name='Confidence',
                hovertemplate='Time: %{x:.2f}s<br>Confidence: %{y:.2f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Update axes
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_yaxes(title_text="Frequency (Hz)", row=1, col=1)
        fig.update_yaxes(title_text="Confidence", range=[0, 1], row=2, col=1)
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Interactive Pitch Analysis",
            hovermode='closest'
        )
        
        return fig
    
    def create_interactive_piano_roll(self, piano_roll_data: Dict) -> go.Figure:
        """
        Create interactive piano roll using Plotly
        
        Args:
            piano_roll_data: Dictionary with times, notes, and matrix
            
        Returns:
            Plotly Figure object
        """
        matrix = piano_roll_data['matrix']
        
        if matrix.size == 0:
            logger.warning("Empty piano roll data")
            return None
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            colorscale='Blues',
            showscale=False
        ))
        
        # Update layout
        fig.update_layout(
            title='Interactive Piano Roll',
            xaxis_title='Time',
            yaxis_title='MIDI Note',
            height=600
        )
        
        return fig
    
    def create_summary_dashboard(self, audio_data: np.ndarray, sr: int,
                                times: np.ndarray, frequencies: np.ndarray,
                                confidences: np.ndarray, notes: List[Dict],
                                note_stats: Dict,
                                output_path: Optional[str] = None) -> str:
        """
        Create a comprehensive summary dashboard
        
        Args:
            audio_data: Audio signal
            sr: Sample rate
            times: Time array
            frequencies: Frequency array
            confidences: Confidence array
            notes: List of note dictionaries
            note_stats: Note statistics
            output_path: Path to save figure
            
        Returns:
            Path to saved figure
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Waveform
        ax1 = fig.add_subplot(gs[0, :])
        times_wave = np.arange(len(audio_data)) / sr
        ax1.plot(times_wave, audio_data, linewidth=0.5)
        ax1.set_title('Audio Waveform')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True, alpha=0.3)
        
        # Pitch over time
        ax2 = fig.add_subplot(gs[1, 0])
        mask = frequencies > 0
        scatter = ax2.scatter(times[mask], frequencies[mask],
                             c=confidences[mask], cmap=COLORMAP,
                             alpha=0.6, s=10)
        ax2.set_title('Detected Pitch')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Frequency (Hz)')
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax2, label='Confidence')
        
        # Spectrogram
        ax3 = fig.add_subplot(gs[1, 1])
        D = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)
        img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz',
                                       cmap=COLORMAP, ax=ax3)
        ax3.set_title('Spectrogram')
        plt.colorbar(img, ax=ax3, format='%+2.0f dB')
        
        # Note distribution
        ax4 = fig.add_subplot(gs[2, 0])
        if note_stats.get('note_distribution'):
            notes_list = list(note_stats['note_distribution'].keys())
            counts = list(note_stats['note_distribution'].values())
            sorted_pairs = sorted(zip(notes_list, counts), key=lambda x: x[1], reverse=True)
            notes_list, counts = zip(*sorted_pairs) if sorted_pairs else ([], [])
            top_n = min(15, len(notes_list))
            ax4.bar(range(top_n), counts[:top_n])
            ax4.set_xticks(range(top_n))
            ax4.set_xticklabels(notes_list[:top_n], rotation=45, ha='right')
            ax4.set_title('Top 15 Most Common Notes')
            ax4.set_xlabel('Note')
            ax4.set_ylabel('Count')
            ax4.grid(True, alpha=0.3, axis='y')
        
        # Statistics text
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('off')
        stats_text = f"""
        Analysis Summary
        ═══════════════════════════════
        Total Notes Detected: {note_stats.get('total_notes', 0)}
        Unique Notes: {note_stats.get('unique_notes', 0)}
        Octave Range: {note_stats.get('octave_range', 'N/A')}
        Avg Frequency: {note_stats.get('avg_frequency', 0):.1f} Hz
        
        Most Common Notes:
        """
        for note, count in note_stats.get('most_common', [])[:5]:
            stats_text += f"\n  {note}: {count} times"
        
        ax5.text(0.1, 0.9, stats_text, transform=ax5.transAxes,
                fontfamily='monospace', verticalalignment='top', fontsize=10)
        
        plt.suptitle('Music Analysis Dashboard', fontsize=16, fontweight='bold')
        
        if output_path:
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved dashboard to {output_path}")
        
        plt.close()
        return output_path
