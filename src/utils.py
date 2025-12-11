"""
Utility functions for the Music Analyzer application
"""

import os
import logging
from typing import Optional, Tuple
import numpy as np

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)

def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL
    
    Args:
        url: String to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    return url.startswith(('http://', 'https://', 'www.'))

def clean_filename(filename: str) -> str:
    """
    Clean filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def format_time(seconds: float) -> str:
    """
    Format time in seconds to MM:SS format
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Result of division or default
    """
    if denominator == 0:
        return default
    return numerator / denominator

def get_file_size_mb(filepath: str) -> float:
    """
    Get file size in MB
    
    Args:
        filepath: Path to file
        
    Returns:
        File size in MB
    """
    if not os.path.exists(filepath):
        return 0.0
    return os.path.getsize(filepath) / (1024 * 1024)

def smooth_array(data: np.ndarray, window_size: int = 5) -> np.ndarray:
    """
    Smooth an array using a moving average
    
    Args:
        data: Input array
        window_size: Size of smoothing window
        
    Returns:
        Smoothed array
    """
    if window_size < 2:
        return data
    
    if len(data) < window_size:
        return data
    
    kernel = np.ones(window_size) / window_size
    return np.convolve(data, kernel, mode='same')

def remove_outliers(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    """
    Remove outliers from data using z-score method
    
    Args:
        data: Input array
        threshold: Z-score threshold
        
    Returns:
        Array with outliers removed (replaced with median)
    """
    if len(data) == 0:
        return data
    
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    
    if mad == 0:
        return data
    
    modified_z_scores = 0.6745 * (data - median) / mad
    filtered_data = data.copy()
    filtered_data[np.abs(modified_z_scores) > threshold] = median
    
    return filtered_data

def create_timestamp_array(duration: float, hop_length: int, sr: int) -> np.ndarray:
    """
    Create array of timestamps for audio frames
    
    Args:
        duration: Audio duration in seconds
        hop_length: Hop length in samples
        sr: Sample rate
        
    Returns:
        Array of timestamps
    """
    n_frames = int(duration * sr / hop_length)
    return np.linspace(0, duration, n_frames)

def get_dominant_frequencies(frequencies: np.ndarray, magnitudes: np.ndarray, 
                            top_n: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get the top N dominant frequencies
    
    Args:
        frequencies: Array of frequencies
        magnitudes: Array of corresponding magnitudes
        top_n: Number of top frequencies to return
        
    Returns:
        Tuple of (top frequencies, top magnitudes)
    """
    if len(frequencies) == 0:
        return np.array([]), np.array([])
    
    top_indices = np.argsort(magnitudes)[-top_n:][::-1]
    return frequencies[top_indices], magnitudes[top_indices]

def interpolate_gaps(data: np.ndarray, max_gap: int = 5) -> np.ndarray:
    """
    Interpolate small gaps in data (where values are 0 or NaN)
    
    Args:
        data: Input array
        max_gap: Maximum gap size to interpolate
        
    Returns:
        Array with gaps interpolated
    """
    result = data.copy()
    mask = (result == 0) | np.isnan(result)
    
    if not np.any(mask):
        return result
    
    indices = np.arange(len(result))
    valid_indices = indices[~mask]
    valid_values = result[~mask]
    
    if len(valid_values) == 0:
        return result
    
    result[mask] = np.interp(indices[mask], valid_indices, valid_values)
    
    return result
