"""
Audio Processing Module
Handles downloading, loading, and converting audio files
"""

import os
import tempfile
from typing import Optional, Tuple
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
import yt_dlp
import requests
from pathlib import Path

from .config import (
    SAMPLE_RATE, TEMP_DIR, SUPPORTED_FORMATS,
    MAX_DOWNLOAD_SIZE, ERROR_MESSAGES
)
from .utils import get_logger, validate_url, clean_filename, get_file_size_mb

logger = get_logger(__name__)


class AudioProcessor:
    """Class for processing audio files"""
    
    def __init__(self, sample_rate: int = SAMPLE_RATE):
        """
        Initialize AudioProcessor
        
        Args:
            sample_rate: Target sample rate for audio processing
        """
        self.sample_rate = sample_rate
        self.temp_dir = TEMP_DIR
        
    def process_from_url(self, url: str) -> Tuple[np.ndarray, int, str]:
        """
        Download and process audio from URL
        
        Args:
            url: URL to download audio from
            
        Returns:
            Tuple of (audio_data, sample_rate, filepath)
            
        Raises:
            ValueError: If URL is invalid or download fails
        """
        if not validate_url(url):
            raise ValueError(ERROR_MESSAGES['invalid_url'])
        
        logger.info(f"Processing audio from URL: {url}")
        
        # Determine if it's a YouTube URL or direct audio file
        if 'youtube.com' in url or 'youtu.be' in url:
            filepath = self._download_youtube(url)
        else:
            filepath = self._download_direct(url)
        
        # Load and process the audio
        audio_data, sr = self.load_audio(filepath)
        
        return audio_data, sr, filepath
    
    def process_from_file(self, filepath: str) -> Tuple[np.ndarray, int]:
        """
        Load and process audio from local file
        
        Args:
            filepath: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        file_ext = Path(filepath).suffix.lower()
        if file_ext not in SUPPORTED_FORMATS:
            raise ValueError(ERROR_MESSAGES['format_not_supported'])
        
        logger.info(f"Processing audio from file: {filepath}")
        return self.load_audio(filepath)
    
    def load_audio(self, filepath: str, mono: bool = True) -> Tuple[np.ndarray, int]:
        """
        Load audio file and convert to target format
        
        Args:
            filepath: Path to audio file
            mono: Whether to convert to mono
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            # Load with librosa
            audio_data, sr = librosa.load(
                filepath,
                sr=self.sample_rate,
                mono=mono
            )
            
            logger.info(f"Loaded audio: duration={len(audio_data)/sr:.2f}s, sr={sr}Hz")
            return audio_data, sr
            
        except Exception as e:
            logger.error(f"Error loading audio: {e}")
            raise ValueError(ERROR_MESSAGES['processing_failed'])
    
    def _download_youtube(self, url: str) -> str:
        """
        Download audio from YouTube URL
        
        Args:
            url: YouTube URL
            
        Returns:
            Path to downloaded file
        """
        output_path = os.path.join(self.temp_dir, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info("Downloading from YouTube...")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # Change extension to .wav since we're extracting audio
                filepath = os.path.splitext(filename)[0] + '.wav'
                
                if not os.path.exists(filepath):
                    raise FileNotFoundError("Download completed but file not found")
                
                logger.info(f"Downloaded to: {filepath}")
                return filepath
                
        except Exception as e:
            logger.error(f"YouTube download failed: {e}")
            raise ValueError(ERROR_MESSAGES['download_failed'])
    
    def _download_direct(self, url: str) -> str:
        """
        Download audio file directly from URL
        
        Args:
            url: Direct URL to audio file
            
        Returns:
            Path to downloaded file
        """
        try:
            logger.info("Downloading audio file...")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check file size
            content_length = int(response.headers.get('content-length', 0))
            if content_length > MAX_DOWNLOAD_SIZE:
                raise ValueError(f"File too large: {content_length / (1024*1024):.1f} MB")
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            ext = self._get_extension_from_content_type(content_type)
            
            # Save to temp file
            filepath = os.path.join(self.temp_dir, f"downloaded_audio{ext}")
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Direct download failed: {e}")
            raise ValueError(ERROR_MESSAGES['download_failed'])
    
    def _get_extension_from_content_type(self, content_type: str) -> str:
        """
        Get file extension from content type
        
        Args:
            content_type: HTTP content type
            
        Returns:
            File extension with dot
        """
        mapping = {
            'audio/mpeg': '.mp3',
            'audio/mp3': '.mp3',
            'audio/wav': '.wav',
            'audio/wave': '.wav',
            'audio/x-wav': '.wav',
            'audio/flac': '.flac',
            'audio/ogg': '.ogg',
            'audio/mp4': '.m4a',
        }
        return mapping.get(content_type.lower(), '.mp3')
    
    def save_audio(self, audio_data: np.ndarray, filepath: str, 
                   sample_rate: Optional[int] = None) -> None:
        """
        Save audio data to file
        
        Args:
            audio_data: Audio data array
            filepath: Output filepath
            sample_rate: Sample rate (uses default if not specified)
        """
        sr = sample_rate or self.sample_rate
        sf.write(filepath, audio_data, sr)
        logger.info(f"Saved audio to: {filepath}")
    
    def normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Normalize audio to [-1, 1] range
        
        Args:
            audio_data: Input audio data
            
        Returns:
            Normalized audio data
        """
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val
        return audio_data
    
    def trim_silence(self, audio_data: np.ndarray, 
                     threshold_db: float = 40) -> np.ndarray:
        """
        Trim silence from beginning and end of audio
        
        Args:
            audio_data: Input audio data
            threshold_db: Threshold in dB below which to consider silence
            
        Returns:
            Trimmed audio data
        """
        trimmed, _ = librosa.effects.trim(
            audio_data,
            top_db=threshold_db
        )
        logger.info(f"Trimmed audio from {len(audio_data)} to {len(trimmed)} samples")
        return trimmed
    
    def get_audio_info(self, filepath: str) -> dict:
        """
        Get information about audio file
        
        Args:
            filepath: Path to audio file
            
        Returns:
            Dictionary with audio information
        """
        try:
            audio_data, sr = librosa.load(filepath, sr=None)
            duration = len(audio_data) / sr
            
            return {
                'duration': duration,
                'sample_rate': sr,
                'samples': len(audio_data),
                'channels': 1 if audio_data.ndim == 1 else audio_data.shape[0],
                'file_size_mb': get_file_size_mb(filepath)
            }
        except Exception as e:
            logger.error(f"Error getting audio info: {e}")
            return {}
    
    def stream_youtube_audio(self, url: str, duration_limit: Optional[int] = None) -> Tuple[np.ndarray, int, dict]:
        """
        Stream audio from YouTube without saving to disk (memory-only processing)
        
        Args:
            url: YouTube URL
            duration_limit: Optional duration limit in seconds (for quick analysis)
            
        Returns:
            Tuple of (audio_data, sample_rate, metadata)
        """
        import io
        
        logger.info(f"Streaming audio from YouTube (no download): {url}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info without downloading
                try:
                    info = ydl.extract_info(url, download=False)
                except Exception as e:
                    logger.error(f"Failed to extract video info: {e}")
                    raise ValueError(
                        f"Cannot access video. Possible reasons:\n"
                        f"  • Video is private or restricted\n"
                        f"  • Age-restricted content\n"
                        f"  • Geographical restrictions\n"
                        f"  • Invalid URL\n"
                        f"Try using 'Download & Analyze' mode instead."
                    )
                
                if not info:
                    raise ValueError("No video information available")
                
                # Get audio URL
                audio_url = info.get('url')
                if not audio_url:
                    raise ValueError("Cannot extract audio stream URL. Try 'Download & Analyze' mode.")
                
                metadata = {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0)
                }
                
                logger.info(f"Video: {metadata['title']} ({metadata['duration']}s)")
                
                # Stream audio data
                try:
                    response = requests.get(audio_url, stream=True, timeout=30)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to stream audio: {e}")
                    raise ValueError(
                        f"Cannot download audio stream.\n"
                        f"  • Network connection issue\n"
                        f"  • Stream URL expired\n"
                        f"Try using 'Download & Analyze' mode instead."
                    )
                
                audio_bytes = io.BytesIO()
                
                # Download to memory (with size limit)
                max_size = 50 * 1024 * 1024  # 50 MB limit
                downloaded = 0
                
                try:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            downloaded += len(chunk)
                            if downloaded > max_size:
                                logger.warning("Reached download size limit")
                                break
                            audio_bytes.write(chunk)
                except Exception as e:
                    logger.error(f"Error during streaming: {e}")
                    if downloaded == 0:
                        raise ValueError("Failed to download any audio data")
                    logger.warning(f"Partial download: {downloaded / 1024 / 1024:.1f} MB")
                
                if audio_bytes.tell() == 0:
                    raise ValueError("No audio data downloaded")
                
                audio_bytes.seek(0)
                
                # Save to temp file (required for librosa/ffmpeg)
                import tempfile
                tmp_path = None
                try:
                    with tempfile.NamedTemporaryFile(suffix='.m4a', delete=False) as tmp:
                        tmp.write(audio_bytes.read())
                        tmp_path = tmp.name
                    
                    if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                        raise ValueError("Temporary file is empty")
                    
                    # Load audio with optional duration limit
                    try:
                        if duration_limit:
                            audio_data, sr = librosa.load(
                                tmp_path,
                                sr=self.sample_rate,
                                mono=True,
                                duration=duration_limit
                            )
                        else:
                            audio_data, sr = librosa.load(
                                tmp_path,
                                sr=self.sample_rate,
                                mono=True
                            )
                    except Exception as e:
                        logger.error(f"Failed to load audio: {e}")
                        raise ValueError(
                            f"Cannot process audio file.\n"
                            f"  • Audio format may not be supported\n"
                            f"  • File may be corrupted\n"
                            f"Try using 'Download & Analyze' mode instead."
                        )
                    
                    if len(audio_data) == 0:
                        raise ValueError("Loaded audio is empty")
                    
                    logger.info(f"Streamed {len(audio_data)/sr:.1f}s of audio")
                    return audio_data, sr, metadata
                    
                finally:
                    # Clean up temp file
                    if tmp_path and os.path.exists(tmp_path):
                        try:
                            os.unlink(tmp_path)
                        except Exception as e:
                            logger.warning(f"Failed to delete temp file: {e}")
                
        except ValueError:
            # Re-raise ValueError with our custom messages
            raise
        except Exception as e:
            logger.error(f"Unexpected error streaming audio: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise ValueError(
                f"Streaming failed: {str(e)}\n\n"
                f"Please try 'Download & Analyze' mode instead."
            )
