"""
Real-time Microphone Audio Capture and Analysis
Allows users to record and analyze their voice in real-time
"""

import numpy as np
import sounddevice as sd
import queue
import threading
import time
from typing import Optional, Callable, List, Tuple
import logging

logger = logging.getLogger(__name__)


class MicrophoneRecorder:
    """Record and analyze audio from microphone in real-time"""
    
    def __init__(self, sample_rate: int = 22050, channels: int = 1):
        """
        Initialize microphone recorder
        
        Args:
            sample_rate: Sample rate for recording
            channels: Number of audio channels (1 for mono)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recorded_audio = []
        self.stream = None
        
    def list_devices(self) -> List[dict]:
        """
        List all available audio input devices
        
        Returns:
            List of device dictionaries
        """
        devices = sd.query_devices()
        input_devices = []
        
        for idx, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_devices.append({
                    'index': idx,
                    'name': device['name'],
                    'channels': device['max_input_channels'],
                    'default_samplerate': device['default_samplerate']
                })
        
        return input_devices
    
    def get_default_device(self) -> Optional[dict]:
        """Get the default input device"""
        try:
            default_device = sd.query_devices(kind='input')
            return {
                'index': sd.default.device[0],
                'name': default_device['name'],
                'channels': default_device['max_input_channels'],
                'default_samplerate': default_device['default_samplerate']
            }
        except Exception as e:
            logger.error(f"Error getting default device: {e}")
            return None
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback function for audio stream"""
        if status:
            logger.warning(f"Audio stream status: {status}")
        
        # Copy audio data to queue
        self.audio_queue.put(indata.copy())
    
    def start_recording(self, device: Optional[int] = None, duration: Optional[float] = None):
        """
        Start recording from microphone
        
        Args:
            device: Device index (None for default)
            duration: Maximum duration in seconds (None for unlimited)
        """
        if self.is_recording:
            logger.warning("Already recording")
            return
        
        self.is_recording = True
        self.recorded_audio = []
        
        try:
            # Open audio stream
            self.stream = sd.InputStream(
                device=device,
                channels=self.channels,
                samplerate=self.sample_rate,
                callback=self._audio_callback
            )
            self.stream.start()
            
            logger.info(f"Started recording from device {device or 'default'}")
            
            # If duration specified, record for that time
            if duration:
                time.sleep(duration)
                self.stop_recording()
                
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            self.is_recording = False
            raise
    
    def stop_recording(self) -> np.ndarray:
        """
        Stop recording and return recorded audio
        
        Returns:
            NumPy array with recorded audio data
        """
        if not self.is_recording:
            logger.warning("Not currently recording")
            return np.array([])
        
        self.is_recording = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Collect all audio from queue
        while not self.audio_queue.empty():
            try:
                chunk = self.audio_queue.get_nowait()
                self.recorded_audio.append(chunk)
            except queue.Empty:
                break
        
        # Concatenate all chunks
        if self.recorded_audio:
            audio_data = np.concatenate(self.recorded_audio, axis=0)
            audio_data = audio_data.flatten()  # Ensure 1D array
            logger.info(f"Recording stopped. Duration: {len(audio_data) / self.sample_rate:.2f}s")
            return audio_data
        else:
            logger.warning("No audio data recorded")
            return np.array([])
    
    def record_duration(self, duration: float, device: Optional[int] = None) -> np.ndarray:
        """
        Record for a specific duration
        
        Args:
            duration: Duration in seconds
            device: Device index (None for default)
            
        Returns:
            NumPy array with recorded audio
        """
        logger.info(f"Recording for {duration} seconds...")
        
        try:
            # Record audio
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=device,
                dtype='float32'
            )
            
            # Wait for recording to complete
            sd.wait()
            
            # Flatten to 1D if needed
            if audio_data.ndim > 1:
                audio_data = audio_data.flatten()
            
            logger.info(f"Recorded {len(audio_data) / self.sample_rate:.2f}s of audio")
            return audio_data
            
        except Exception as e:
            logger.error(f"Error during recording: {e}")
            raise
    
    def get_current_audio(self) -> np.ndarray:
        """
        Get currently recorded audio without stopping
        
        Returns:
            NumPy array with audio recorded so far
        """
        current_audio = []
        
        # Collect all audio from queue without blocking
        while not self.audio_queue.empty():
            try:
                chunk = self.audio_queue.get_nowait()
                current_audio.append(chunk)
            except queue.Empty:
                break
        
        if current_audio:
            audio_data = np.concatenate(current_audio, axis=0)
            return audio_data.flatten()
        else:
            return np.array([])
    
    def test_microphone(self, duration: float = 2.0) -> bool:
        """
        Test if microphone is working
        
        Args:
            duration: Test duration in seconds
            
        Returns:
            True if microphone works, False otherwise
        """
        try:
            logger.info("Testing microphone...")
            audio = self.record_duration(duration)
            
            # Check if audio has any signal
            if len(audio) > 0 and np.abs(audio).max() > 0.001:
                logger.info("Microphone test successful")
                return True
            else:
                logger.warning("Microphone test failed - no signal detected")
                return False
                
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False
    
    def get_audio_level(self, audio_data: np.ndarray) -> float:
        """
        Get audio level (RMS) from audio data
        
        Args:
            audio_data: Audio data array
            
        Returns:
            RMS level (0.0 to 1.0)
        """
        if len(audio_data) == 0:
            return 0.0
        
        rms = np.sqrt(np.mean(audio_data ** 2))
        return float(rms)
    
    def is_silent(self, audio_data: np.ndarray, threshold: float = 0.01) -> bool:
        """
        Check if audio is silent
        
        Args:
            audio_data: Audio data array
            threshold: Silence threshold
            
        Returns:
            True if silent, False otherwise
        """
        level = self.get_audio_level(audio_data)
        return level < threshold


class RealTimeAnalyzer:
    """Analyze audio in real-time as it's being recorded"""
    
    def __init__(self, recorder: MicrophoneRecorder, callback: Optional[Callable] = None):
        """
        Initialize real-time analyzer
        
        Args:
            recorder: MicrophoneRecorder instance
            callback: Function to call with analysis results
        """
        self.recorder = recorder
        self.callback = callback
        self.is_analyzing = False
        self.analysis_thread = None
        
    def start_analysis(self, analysis_func: Callable, update_interval: float = 0.5):
        """
        Start real-time analysis
        
        Args:
            analysis_func: Function to analyze audio chunks
            update_interval: How often to analyze (seconds)
        """
        if self.is_analyzing:
            logger.warning("Analysis already running")
            return
        
        self.is_analyzing = True
        
        def analyze_loop():
            while self.is_analyzing:
                # Get current audio
                audio = self.recorder.get_current_audio()
                
                if len(audio) > 0:
                    # Analyze audio
                    try:
                        results = analysis_func(audio)
                        
                        if self.callback:
                            self.callback(results)
                    except Exception as e:
                        logger.error(f"Error during analysis: {e}")
                
                time.sleep(update_interval)
        
        self.analysis_thread = threading.Thread(target=analyze_loop, daemon=True)
        self.analysis_thread.start()
        logger.info("Started real-time analysis")
    
    def stop_analysis(self):
        """Stop real-time analysis"""
        self.is_analyzing = False
        if self.analysis_thread:
            self.analysis_thread.join(timeout=2.0)
        logger.info("Stopped real-time analysis")
