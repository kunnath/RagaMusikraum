"""
Pitch Detection Module
Implements multiple pitch detection algorithms
"""

import numpy as np
import librosa
from typing import Tuple, Optional, Dict
import warnings

# Optional imports
try:
    from aubio import pitch as aubio_pitch
    AUBIO_AVAILABLE = True
except ImportError:
    AUBIO_AVAILABLE = False
    
try:
    import crepe
    CREPE_AVAILABLE = True
except ImportError:
    CREPE_AVAILABLE = False

from .config import (
    SAMPLE_RATE, HOP_LENGTH, N_FFT,
    PITCH_METHODS, ERROR_MESSAGES
)
from .utils import (
    get_logger, smooth_array, remove_outliers,
    create_timestamp_array, interpolate_gaps
)

logger = get_logger(__name__)

# Suppress warnings
warnings.filterwarnings('ignore')


class PitchDetector:
    """Class for detecting pitch in audio using multiple methods"""
    
    def __init__(self, sample_rate: int = SAMPLE_RATE):
        """
        Initialize PitchDetector
        
        Args:
            sample_rate: Sample rate of audio
        """
        self.sample_rate = sample_rate
        self.hop_length = HOP_LENGTH
        self.n_fft = N_FFT
        
    def detect_pitch(self, audio_data: np.ndarray, 
                     method: str = 'librosa',
                     **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Detect pitch using specified method
        
        Args:
            audio_data: Audio signal
            method: Pitch detection method ('crepe', 'librosa', 'aubio')
            **kwargs: Additional arguments for specific methods
            
        Returns:
            Tuple of (times, frequencies, confidences)
        """
        logger.info(f"Detecting pitch using {method} method...")
        
        if method == 'crepe':
            if not CREPE_AVAILABLE:
                logger.warning("CREPE not available, falling back to librosa")
                return self._detect_pitch_librosa(audio_data, **kwargs)
            return self._detect_pitch_crepe(audio_data, **kwargs)
        elif method == 'librosa':
            return self._detect_pitch_librosa(audio_data, **kwargs)
        elif method == 'aubio':
            if not AUBIO_AVAILABLE:
                logger.warning("Aubio not available, falling back to librosa")
                return self._detect_pitch_librosa(audio_data, **kwargs)
            return self._detect_pitch_aubio(audio_data, **kwargs)
        else:
            raise ValueError(f"Unknown pitch detection method: {method}")
    
    def _detect_pitch_crepe(self, audio_data: np.ndarray,
                           model_capacity: str = 'full',
                           viterbi: bool = True,
                           step_size: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Detect pitch using CREPE (Convolutional Representation for Pitch Estimation)
        
        Args:
            audio_data: Audio signal
            model_capacity: Model size ('tiny', 'small', 'medium', 'large', 'full')
            viterbi: Whether to use Viterbi decoding
            step_size: Step size in milliseconds
            
        Returns:
            Tuple of (times, frequencies, confidences)
        """
        try:
            import crepe
            
            # CREPE expects audio in range [-1, 1]
            audio_data = audio_data / np.max(np.abs(audio_data)) if np.max(np.abs(audio_data)) > 0 else audio_data
            
            time, frequency, confidence, activation = crepe.predict(
                audio_data,
                self.sample_rate,
                model_capacity=model_capacity,
                viterbi=viterbi,
                step_size=step_size,
                verbose=0
            )
            
            # Filter out low confidence predictions
            mask = confidence > 0.5
            frequency[~mask] = 0
            
            logger.info(f"CREPE detected {np.sum(mask)} pitch frames with confidence > 0.5")
            return time, frequency, confidence
            
        except ImportError:
            logger.error("CREPE not installed. Install with: pip install crepe")
            raise
        except Exception as e:
            logger.error(f"CREPE pitch detection failed: {e}")
            raise ValueError(ERROR_MESSAGES['processing_failed'])
    
    def _detect_pitch_librosa(self, audio_data: np.ndarray,
                             fmin: float = 80,
                             fmax: float = 1200,
                             threshold: float = 0.1) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Detect pitch using librosa's piptrack
        
        Args:
            audio_data: Audio signal
            fmin: Minimum frequency (Hz)
            fmax: Maximum frequency (Hz)
            threshold: Magnitude threshold
            
        Returns:
            Tuple of (times, frequencies, confidences)
        """
        try:
            # Compute pitch using piptrack
            pitches, magnitudes = librosa.piptrack(
                y=audio_data,
                sr=self.sample_rate,
                hop_length=self.hop_length,
                fmin=fmin,
                fmax=fmax,
                threshold=threshold
            )
            
            # Extract the pitch with highest magnitude at each time frame
            n_frames = pitches.shape[1]
            frequencies = np.zeros(n_frames)
            confidences = np.zeros(n_frames)
            
            for i in range(n_frames):
                index = magnitudes[:, i].argmax()
                frequencies[i] = pitches[index, i]
                confidences[i] = magnitudes[index, i]
            
            # Normalize confidences
            max_conf = np.max(confidences)
            if max_conf > 0:
                confidences = confidences / max_conf
            
            # Create time array
            times = librosa.frames_to_time(
                np.arange(n_frames),
                sr=self.sample_rate,
                hop_length=self.hop_length
            )
            
            # Filter out zero frequencies
            mask = frequencies > 0
            logger.info(f"Librosa detected {np.sum(mask)} non-zero pitch frames")
            
            return times, frequencies, confidences
            
        except Exception as e:
            logger.error(f"Librosa pitch detection failed: {e}")
            raise ValueError(ERROR_MESSAGES['processing_failed'])
    
    def _detect_pitch_aubio(self, audio_data: np.ndarray,
                           method: str = 'yinfft',
                           buf_size: int = 2048,
                           hop_size: int = 512,
                           tolerance: float = 0.8) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Detect pitch using aubio
        
        Args:
            audio_data: Audio signal
            method: Aubio pitch detection method
            buf_size: Buffer size
            hop_size: Hop size
            tolerance: Tolerance parameter
            
        Returns:
            Tuple of (times, frequencies, confidences)
        """
        try:
            # Initialize aubio pitch detector
            pitch_detector = aubio_pitch(
                method,
                buf_size,
                hop_size,
                self.sample_rate
            )
            pitch_detector.set_unit("Hz")
            pitch_detector.set_tolerance(tolerance)
            
            # Process audio in chunks
            n_frames = len(audio_data) // hop_size
            frequencies = np.zeros(n_frames)
            confidences = np.zeros(n_frames)
            
            for i in range(n_frames):
                start = i * hop_size
                end = start + buf_size
                if end > len(audio_data):
                    chunk = np.pad(audio_data[start:], (0, end - len(audio_data)))
                else:
                    chunk = audio_data[start:end]
                
                # Convert to float32
                chunk = chunk.astype(np.float32)
                
                # Detect pitch
                pitch_value = pitch_detector(chunk)[0]
                confidence = pitch_detector.get_confidence()
                
                frequencies[i] = pitch_value
                confidences[i] = confidence
            
            # Create time array
            times = create_timestamp_array(
                len(audio_data) / self.sample_rate,
                hop_size,
                self.sample_rate
            )[:len(frequencies)]
            
            # Filter out low confidence
            mask = confidences > 0.5
            frequencies[~mask] = 0
            
            logger.info(f"Aubio detected {np.sum(mask)} pitch frames with confidence > 0.5")
            return times, frequencies, confidences
            
        except Exception as e:
            logger.error(f"Aubio pitch detection failed: {e}")
            raise ValueError(ERROR_MESSAGES['processing_failed'])
    
    def post_process_pitch(self, frequencies: np.ndarray,
                          confidences: np.ndarray,
                          smooth: bool = True,
                          remove_outliers_flag: bool = True,
                          interpolate: bool = True) -> np.ndarray:
        """
        Post-process detected pitch
        
        Args:
            frequencies: Detected frequencies
            confidences: Confidence values
            smooth: Whether to smooth the pitch contour
            remove_outliers_flag: Whether to remove outliers
            interpolate: Whether to interpolate gaps
            
        Returns:
            Processed frequencies
        """
        processed = frequencies.copy()
        
        # Remove low-confidence detections
        processed[confidences < 0.5] = 0
        
        # Remove outliers
        if remove_outliers_flag:
            non_zero_mask = processed > 0
            if np.any(non_zero_mask):
                processed[non_zero_mask] = remove_outliers(processed[non_zero_mask])
        
        # Interpolate small gaps
        if interpolate:
            processed = interpolate_gaps(processed, max_gap=5)
        
        # Smooth the contour
        if smooth:
            non_zero_mask = processed > 0
            if np.any(non_zero_mask):
                processed[non_zero_mask] = smooth_array(processed[non_zero_mask], window_size=5)
        
        return processed
    
    def get_pitch_statistics(self, frequencies: np.ndarray,
                            confidences: np.ndarray) -> Dict[str, float]:
        """
        Get statistics about detected pitch
        
        Args:
            frequencies: Detected frequencies
            confidences: Confidence values
            
        Returns:
            Dictionary of statistics
        """
        valid_frequencies = frequencies[(frequencies > 0) & (confidences > 0.5)]
        
        if len(valid_frequencies) == 0:
            return {
                'mean_frequency': 0,
                'median_frequency': 0,
                'min_frequency': 0,
                'max_frequency': 0,
                'std_frequency': 0,
                'pitch_coverage': 0
            }
        
        return {
            'mean_frequency': float(np.mean(valid_frequencies)),
            'median_frequency': float(np.median(valid_frequencies)),
            'min_frequency': float(np.min(valid_frequencies)),
            'max_frequency': float(np.max(valid_frequencies)),
            'std_frequency': float(np.std(valid_frequencies)),
            'pitch_coverage': float(len(valid_frequencies) / len(frequencies))
        }
    
    def compare_methods(self, audio_data: np.ndarray) -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """
        Compare all pitch detection methods
        
        Args:
            audio_data: Audio signal
            
        Returns:
            Dictionary mapping method names to (times, frequencies, confidences)
        """
        results = {}
        
        methods = ['crepe', 'librosa', 'aubio']
        for method in methods:
            try:
                logger.info(f"Testing {method} method...")
                times, freqs, confs = self.detect_pitch(audio_data, method=method)
                results[method] = (times, freqs, confs)
            except Exception as e:
                logger.error(f"Method {method} failed: {e}")
                results[method] = None
        
        return results
