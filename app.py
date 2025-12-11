"""
Streamlit Application for Music Analysis
Web interface for analyzing music and converting to notes
"""

import streamlit as st
import os
import sys
import numpy as np
import json
from datetime import datetime
import tempfile
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.audio_processor import AudioProcessor
from src.pitch_detector import PitchDetector
from src.note_converter import NoteConverter
from src.visualizer import AudioVisualizer
from src.midi_exporter import MidiExporter
from src.song_comparator import SongComparator
from src.config import OUTPUT_DIR, TEMP_DIR
from src.utils import validate_url, format_time, get_file_size_mb
import yt_dlp

# Page configuration
st.set_page_config(
    page_title="Raga Musikraum - Music Analyzer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Music App Theme
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Orbitron:wght@500;700;900&display=swap');
    
    /* Main app background with gradient and music pattern */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #667eea 75%, #764ba2 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Music wave pattern overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(
                90deg,
                rgba(255, 255, 255, 0.03) 0px,
                rgba(255, 255, 255, 0.03) 1px,
                transparent 1px,
                transparent 20px
            ),
            repeating-linear-gradient(
                0deg,
                rgba(255, 255, 255, 0.03) 0px,
                rgba(255, 255, 255, 0.03) 1px,
                transparent 1px,
                transparent 20px
            );
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main content area with glass morphism */
    [data-testid="stAppViewContainer"] > .main {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Headers with glow effect */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #fff, #f093fb, #fff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textGlow 3s ease infinite;
        text-shadow: 0 0 30px rgba(240, 147, 251, 0.5);
        margin-bottom: 1rem;
        letter-spacing: 2px;
    }
    
    @keyframes textGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sub-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        font-weight: 300;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* All text in white with shadow for readability */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    /* =================================
       TABS - MODERN MUSIC STYLE
       ================================= */
    
    /* Tab container */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: linear-gradient(135deg, rgba(30, 30, 60, 0.8) 0%, rgba(50, 50, 90, 0.8) 100%);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 12px 15px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(102, 126, 234, 0.4);
    }
    
    /* Individual tab button */
    .stTabs [data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        height: 75px;
        min-width: 180px;
        background: linear-gradient(135deg, rgba(60, 60, 100, 0.6) 0%, rgba(80, 80, 120, 0.6) 100%);
        border-radius: 16px;
        color: white;
        font-size: 1.3rem;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid rgba(255, 255, 255, 0.1);
        padding: 0 25px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    /* Tab glow effect on hover */
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    /* Hover state */
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%);
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Active/Selected tab */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6), 0 0 40px rgba(240, 147, 251, 0.4) !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-3px) scale(1.08);
        font-weight: 900;
    }
    
    /* Active tab pulse animation */
    @keyframes tabPulse {
        0%, 100% {
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6), 0 0 40px rgba(240, 147, 251, 0.4);
        }
        50% {
            box-shadow: 0 8px 35px rgba(102, 126, 234, 0.8), 0 0 50px rgba(240, 147, 251, 0.6);
        }
    }
    
    .stTabs [aria-selected="true"] {
        animation: tabPulse 2s ease-in-out infinite;
    }
    
    /* Tab emoji/icon spacing */
    .stTabs [data-baseweb="tab"] span {
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Buttons with modern gradient */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px;
        color: white !important;
        font-family: 'Poppins', sans-serif;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* =================================
       SELECTBOX - STANDARD STYLING
       ================================= */
    
    /* Container */
    .stSelectbox {
        width: 100% !important;
    }
    
    .stSelectbox > div {
        width: 100% !important;
    }
    
    .stSelectbox label {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
    }
    
    /* Main selectbox control - SOLID DARK BLUE */
    .stSelectbox [data-baseweb="select"] {
        background-color: #2c3e87 !important;
        border-radius: 10px !important;
        min-height: 55px !important;
    }
    
    /* Control container */
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #2c3e87 !important;
        border: 2px solid #5568c4 !important;
        border-radius: 10px !important;
        min-height: 55px !important;
        padding: 0 1rem !important;
    }
    
    /* Value container - holds the selected text */
    .stSelectbox [data-baseweb="select"] [data-baseweb="value-container"] {
        padding: 0.75rem 0 !important;
    }
    
    /* Selected value text - BRIGHT WHITE */
    .stSelectbox [data-baseweb="select"] [data-baseweb="single-value"] {
        color: #FFFFFF !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Placeholder */
    .stSelectbox [data-baseweb="select"] [data-baseweb="placeholder"] {
        color: rgba(255, 255, 255, 0.6) !important;
        font-size: 1.15rem !important;
    }
    
    /* Dropdown arrow */
    .stSelectbox [data-baseweb="select"] svg {
        fill: #FFFFFF !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* Input (if any) */
    .stSelectbox [data-baseweb="select"] input {
        color: #FFFFFF !important;
        font-size: 1.15rem !important;
    }
    
    /* All text inside select */
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] span {
        color: #FFFFFF !important;
    }
    
    /* =================================
       DROPDOWN MENU - STANDARD STYLING
       ================================= */
    
    /* Dropdown container/popover */
    [data-baseweb="popover"] {
        background-color: #1a2456 !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        border: 2px solid #5568c4 !important;
        z-index: 9999 !important;
    }
    
    /* List container */
    [role="listbox"] {
        background-color: #1a2456 !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }
    
    /* Each dropdown option */
    [role="option"] {
        background-color: #2c3e87 !important;
        color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 0.9rem 1.2rem !important;
        border-radius: 8px !important;
        margin-bottom: 0.4rem !important;
        cursor: pointer !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease !important;
    }
    
    /* Hover state */
    [role="option"]:hover {
        background-color: #4a5fc1 !important;
        color: #FFFFFF !important;
        transform: translateX(4px) !important;
    }
    
    /* Selected/active option */
    [role="option"][aria-selected="true"] {
        background-color: #5568c4 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-left: 4px solid #9ca9ff !important;
    }
    
    /* Menu wrapper */
    [data-baseweb="menu"] {
        background-color: #1a2456 !important;
        border-radius: 10px !important;
    }
    
    [data-baseweb="menu"] li {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        border: 2px dashed rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Sliders */
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #667eea 0%, #f093fb 100%);
    }
    
    .stSlider label {
        color: white !important;
    }
    
    /* Checkboxes and radio buttons */
    .stCheckbox, .stRadio {
        color: white !important;
    }
    
    .stCheckbox label, .stRadio label {
        color: white !important;
    }
    
    .stCheckbox span, .stRadio span {
        color: white !important;
    }
    
    /* Radio button circles */
    [role="radiogroup"] label {
        color: white !important;
    }
    
    /* Success/Info/Warning boxes with glass effect */
    .success-box, .stSuccess {
        padding: 1.5rem;
        background: rgba(76, 175, 80, 0.2) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        color: white !important;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .info-box, .stInfo {
        padding: 1.5rem;
        background: rgba(33, 150, 243, 0.2) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border-left: 5px solid #2196F3;
        color: white !important;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
    }
    
    .stWarning {
        padding: 1.5rem;
        background: rgba(255, 152, 0, 0.2) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border-left: 5px solid #FF9800;
        color: white !important;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);
    }
    
    .stError {
        padding: 1.5rem;
        background: rgba(244, 67, 54, 0.2) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border-left: 5px solid #F44336;
        color: white !important;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
    }
    
    /* Metrics with modern cards */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        color: white !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 0 0 12px 12px;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #f093fb 100%);
        border-radius: 10px;
    }
    
    /* Dataframes and tables */
    .dataframe {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        color: white !important;
    }
    
    /* Plotly charts background */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #f093fb !important;
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(240, 147, 251, 0.6);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Music equalizer animation for header */
    @keyframes equalize {
        0%, 100% { height: 10px; }
        50% { height: 30px; }
    }
    
    /* Add subtle animation to cards */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    [data-testid="stMetric"] {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Footer branding */
    .footer-branding {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(26, 36, 86, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        text-align: center;
        border-top: 2px solid rgba(255, 255, 255, 0.2);
        z-index: 999;
        font-family: 'Poppins', sans-serif;
    }
    
    .footer-branding p {
        margin: 0;
        color: #ffffff;
        font-size: 0.95rem;
    }
    
    .footer-branding a {
        color: #f093fb;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .footer-branding a:hover {
        color: #667eea;
        text-decoration: underline;
    }
    
    .brand-name {
        color: #f093fb;
        font-weight: 700;
    }
    
    /* Add padding to main content to prevent footer overlap */
    .main .block-container {
        padding-bottom: 80px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'results' not in st.session_state:
    st.session_state.results = None


def check_video_accessibility(url):
    """
    Quick check if a YouTube video is accessible for streaming
    
    Returns:
        tuple: (is_accessible, error_message)
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                return True, None
            return False, "Cannot extract video information"
    except Exception as e:
        error_msg = str(e).lower()
        if 'private' in error_msg:
            return False, "Video is private"
        elif 'age' in error_msg or 'restricted' in error_msg:
            return False, "Video is age-restricted or region-locked"
        elif 'not available' in error_msg:
            return False, "Video is not available"
        else:
            return False, f"Cannot access video: {str(e)}"


def main():
    """Main application function"""
    
    # Header with music emojis
    st.markdown('<div class="main-header">🎵 Raga Musikraum 🎶</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">✨ Transform Audio into Musical Notes | Practice Your Voice | Compare Songs ✨</div>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Pitch detection method
        pitch_method = st.selectbox(
            "Pitch Detection Method",
            options=['crepe', 'librosa', 'aubio'],
            help="CREPE is most accurate but slower. Librosa is faster but less accurate."
        )
        
        # Post-processing options
        st.subheader("Post-Processing")
        smooth_pitch = st.checkbox("Smooth pitch contour", value=True)
        remove_outliers = st.checkbox("Remove outliers", value=True)
        
        # Visualization options
        st.subheader("Visualizations")
        show_waveform = st.checkbox("Show waveform", value=True)
        show_spectrogram = st.checkbox("Show spectrogram", value=True)
        show_chromagram = st.checkbox("Show chromagram", value=False)
        
        # Export options
        st.subheader("Export")
        export_midi = st.checkbox("Export to MIDI", value=True)
        export_json = st.checkbox("Export to JSON", value=True)
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This app uses advanced pitch detection algorithms to analyze music and convert it into musical notes.
        
        **🆕 Stream Mode:** 
        For YouTube videos, use "Quick Stream Analysis" to analyze without downloading! Faster and saves disk space (analyzes first 60 seconds).
        
        **Features:**
        - Multiple pitch detection methods
        - Interactive visualizations
        - MIDI export
        - Note statistics
        """)
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "📊 Results", "🔍 Compare Songs", "🎤 Live Mic"])
    
    with tab1:
        st.header("Input Audio")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            options=["URL", "File Upload"],
            horizontal=True
        )
        
        audio_path = None
        
        if input_method == "URL":
            st.subheader("🌐 Enter Audio URL")
            url = st.text_input(
                "Enter YouTube URL or direct audio file URL",
                placeholder="https://www.youtube.com/watch?v=..."
            )
            
            # Add streaming option for YouTube
            is_youtube = url and ('youtube.com' in url or 'youtu.be' in url)
            
            if is_youtube:
                st.info("⚡ **YouTube detected!** You can:\n"
                       "- **Download & Analyze**: Full song analysis (slower, file saved)\n"
                       "- **Quick Stream**: Fast analysis of first 60s (no file saved)")
            
            if is_youtube:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔽 Download and Analyze", key="download_btn"):
                        if not url:
                            st.error("Please enter a URL")
                        elif not validate_url(url):
                            st.error("Invalid URL format")
                        else:
                            analyze_audio(url, pitch_method, smooth_pitch, remove_outliers,
                                        show_waveform, show_spectrogram, show_chromagram,
                                        export_midi, export_json, input_type='url')
                
                with col2:
                    if st.button("⚡ Quick Stream Analysis", key="stream_btn", help="Analyze without downloading (faster, first 60s only)"):
                        if not url:
                            st.error("Please enter a URL")
                        elif not validate_url(url):
                            st.error("Invalid URL format")
                        else:
                            # Quick accessibility check
                            with st.spinner("Checking video accessibility..."):
                                is_accessible, error_msg = check_video_accessibility(url)
                                
                            if not is_accessible:
                                st.error(f"❌ Cannot stream this video: {error_msg}")
                                st.warning("💡 Try using 'Download & Analyze' mode instead, which may work better with restricted videos.")
                            else:
                                analyze_audio(url, pitch_method, smooth_pitch, remove_outliers,
                                            show_waveform, show_spectrogram, show_chromagram,
                                            export_midi, export_json, input_type='stream')
            else:
                if st.button("🔽 Download and Analyze", key="download_btn"):
                    if not url:
                        st.error("Please enter a URL")
                    elif not validate_url(url):
                        st.error("Invalid URL format")
                    else:
                        analyze_audio(url, pitch_method, smooth_pitch, remove_outliers,
                                    show_waveform, show_spectrogram, show_chromagram,
                                    export_midi, export_json, input_type='url')
        
        else:  # File Upload
            st.subheader("📁 Upload Audio File")
            
            # RAW to MP3 Converter Section
            with st.expander("🔧 Convert RAW to MP3", expanded=False):
                st.markdown("""
                Convert RAW audio files to MP3 format for analysis.
                Useful for recordings from microphones or audio devices.
                """)
                
                raw_file = st.file_uploader(
                    "Upload RAW audio file",
                    type=['raw'],
                    key="raw_uploader",
                    help="Upload a RAW audio file to convert to MP3"
                )
                
                if raw_file is not None:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        sample_rate = st.selectbox(
                            "Sample Rate (Hz)",
                            options=[8000, 16000, 22050, 44100, 48000],
                            index=3,  # Default to 44100
                            help="Audio sample rate - usually 44100 Hz"
                        )
                        
                        audio_format = st.selectbox(
                            "Sample Format",
                            options=['s16le', 's24le', 's32le', 'f32le'],
                            index=0,  # Default to s16le (16-bit signed little-endian)
                            help="Audio sample format - s16le is most common"
                        )
                    
                    with col2:
                        channels = st.selectbox(
                            "Channels",
                            options=[1, 2],
                            index=1,  # Default to 2 (stereo)
                            format_func=lambda x: "Mono (1)" if x == 1 else "Stereo (2)",
                            help="Number of audio channels"
                        )
                        
                        bitrate = st.selectbox(
                            "MP3 Bitrate",
                            options=['128k', '192k', '256k', '320k'],
                            index=2,  # Default to 256k
                            help="MP3 output quality"
                        )
                    
                    # Preview/Play RAW audio
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        if st.button("▶️ Preview Audio", key="preview_raw_btn", help="Convert to temporary WAV and play"):
                            with st.spinner("Preparing audio preview..."):
                                try:
                                    import subprocess
                                    
                                    # Save RAW file temporarily
                                    raw_path = os.path.join(TEMP_DIR, f"temp_preview_{raw_file.name}")
                                    with open(raw_path, 'wb') as f:
                                        f.write(raw_file.getbuffer())
                                    
                                    # Convert to WAV for preview
                                    preview_path = os.path.join(TEMP_DIR, "preview_audio.wav")
                                    
                                    cmd = [
                                        'ffmpeg',
                                        '-f', audio_format,
                                        '-ar', str(sample_rate),
                                        '-ac', str(channels),
                                        '-i', raw_path,
                                        '-y',
                                        preview_path
                                    ]
                                    
                                    result = subprocess.run(
                                        cmd,
                                        capture_output=True,
                                        text=True,
                                        timeout=30
                                    )
                                    
                                    if result.returncode == 0:
                                        st.success("✅ Audio ready to play!")
                                        
                                        # Play audio
                                        with open(preview_path, 'rb') as audio_file:
                                            audio_bytes = audio_file.read()
                                            st.audio(audio_bytes, format='audio/wav')
                                        
                                        # Cleanup
                                        if os.path.exists(raw_path):
                                            os.remove(raw_path)
                                        if os.path.exists(preview_path):
                                            os.remove(preview_path)
                                    else:
                                        st.error(f"❌ Preview failed: {result.stderr}")
                                        if os.path.exists(raw_path):
                                            os.remove(raw_path)
                                
                                except subprocess.TimeoutExpired:
                                    st.error("❌ Preview timed out")
                                except FileNotFoundError:
                                    st.error("❌ FFmpeg not found. Install with: brew install ffmpeg")
                                except Exception as e:
                                    st.error(f"❌ Preview error: {str(e)}")
                    
                    with col2:
                        if st.button("🎵 Convert to MP3", key="convert_raw_btn"):
                            with st.spinner("Converting RAW to MP3..."):
                                try:
                                    import subprocess
                                    from datetime import datetime
                                    
                                    # Save RAW file temporarily
                                    raw_path = os.path.join(TEMP_DIR, f"temp_{raw_file.name}")
                                    with open(raw_path, 'wb') as f:
                                        f.write(raw_file.getbuffer())
                                    
                                    # Output MP3 path
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    output_filename = f"converted_{timestamp}.mp3"
                                    output_path = os.path.join(OUTPUT_DIR, output_filename)
                                    
                                    # FFmpeg command
                                    cmd = [
                                        'ffmpeg',
                                        '-f', audio_format,
                                        '-ar', str(sample_rate),
                                        '-ac', str(channels),
                                        '-i', raw_path,
                                        '-b:a', bitrate,
                                        '-y',  # Overwrite output file
                                        output_path
                                    ]
                                    
                                    # Run FFmpeg
                                    result = subprocess.run(
                                        cmd,
                                        capture_output=True,
                                        text=True,
                                        timeout=60
                                    )
                                    
                                    if result.returncode == 0:
                                        st.success(f"✅ Converted successfully: {output_filename}")
                                        
                                        # Provide download button
                                        with open(output_path, 'rb') as f:
                                            st.download_button(
                                                label="📥 Download MP3",
                                                data=f.read(),
                                                file_name=output_filename,
                                                mime="audio/mpeg"
                                            )
                                        
                                        st.info(f"💾 File saved to: outputs/{output_filename}")
                                        st.info("You can now analyze this file using the 'Upload Audio File' option below!")
                                        
                                    else:
                                        st.error(f"❌ Conversion failed: {result.stderr}")
                                    
                                    # Cleanup temp file
                                    if os.path.exists(raw_path):
                                        os.remove(raw_path)
                                        
                                except subprocess.TimeoutExpired:
                                    st.error("❌ Conversion timed out (> 60 seconds)")
                                except FileNotFoundError:
                                    st.error("❌ FFmpeg not found. Please install FFmpeg:\n"
                                           "```\nbrew install ffmpeg\n```")
                                except Exception as e:
                                    st.error(f"❌ Error during conversion: {str(e)}")
            
            st.markdown("---")
            
            uploaded_file = st.file_uploader(
                "Choose an audio file",
                type=['mp3', 'wav', 'flac', 'ogg', 'm4a'],
                help="Supported formats: MP3, WAV, FLAC, OGG, M4A"
            )
            
            if uploaded_file is not None:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    audio_path = tmp_file.name
                
                st.success(f"✅ File uploaded: {uploaded_file.name} ({get_file_size_mb(audio_path):.2f} MB)")
                
                if st.button("🎵 Analyze Audio", key="analyze_btn"):
                    analyze_audio(audio_path, pitch_method, smooth_pitch, remove_outliers,
                                show_waveform, show_spectrogram, show_chromagram,
                                export_midi, export_json, input_type='file')
    
    with tab2:
        if st.session_state.analysis_complete and st.session_state.results:
            display_results(st.session_state.results)
        else:
            st.info("👈 Please input audio from the Input tab to see results here.")
    
    with tab3:
        display_comparison_tab()
    
    with tab4:
        display_microphone_tab()


def analyze_audio(source, pitch_method, smooth_pitch, remove_outliers,
                  show_waveform, show_spectrogram, show_chromagram,
                  export_midi, export_json, input_type='url'):
    """
    Analyze audio and store results
    
    Args:
        source: URL or file path
        pitch_method: Pitch detection method
        smooth_pitch: Whether to smooth pitch
        remove_outliers: Whether to remove outliers
        show_waveform: Whether to show waveform
        show_spectrogram: Whether to show spectrogram
        show_chromagram: Whether to show chromagram
        export_midi: Whether to export MIDI
        export_json: Whether to export JSON
        input_type: 'url' or 'file'
    """
    
    with st.spinner("🎵 Analyzing audio... This may take a minute..."):
        try:
            # Initialize processors
            audio_processor = AudioProcessor()
            pitch_detector = PitchDetector()
            note_converter = NoteConverter()
            visualizer = AudioVisualizer()
            midi_exporter = MidiExporter()
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Load audio
            status_text.text("Loading audio...")
            progress_bar.progress(10)
            
            metadata = None
            if input_type == 'stream':
                # Stream YouTube without downloading
                st.info("⚡ Streaming mode: Analyzing first 60 seconds only (no file saved)")
                
                # Validate it's a YouTube URL
                if not ('youtube.com' in source or 'youtu.be' in source):
                    raise ValueError("Stream mode only works with YouTube URLs. Please use 'Download & Analyze' for other URLs.")
                
                try:
                    audio_data, sr, metadata = audio_processor.stream_youtube_audio(source, duration_limit=60)
                    audio_path = None  # No file saved
                except ValueError:
                    # Re-raise with context
                    raise
                except Exception as e:
                    raise ValueError(
                        f"Streaming failed: {str(e)}\n\n"
                        f"Try using 'Download & Analyze' mode instead."
                    )
            elif input_type == 'url':
                audio_data, sr, audio_path = audio_processor.process_from_url(source)
            else:
                audio_data, sr = audio_processor.process_from_file(source)
                audio_path = source
            
            # Show metadata if available
            if metadata:
                st.success(f"🎬 Streaming: {metadata['title']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Video Duration", f"{metadata['duration']}s")
                with col2:
                    st.metric("Analyzing", "First 60s")
            
            # Normalize and trim
            audio_data = audio_processor.normalize_audio(audio_data)
            audio_data = audio_processor.trim_silence(audio_data)
            
            # Step 2: Detect pitch
            status_text.text(f"Detecting pitch using {pitch_method}...")
            progress_bar.progress(30)
            
            times, frequencies, confidences = pitch_detector.detect_pitch(
                audio_data, method=pitch_method
            )
            
            # Post-process
            if smooth_pitch or remove_outliers:
                frequencies = pitch_detector.post_process_pitch(
                    frequencies, confidences,
                    smooth=smooth_pitch,
                    remove_outliers_flag=remove_outliers
                )
            
            # Step 3: Convert to notes
            status_text.text("Converting to musical notes...")
            progress_bar.progress(50)
            
            notes = note_converter.frequencies_to_notes(frequencies, times)
            note_segments = note_converter.get_note_segments(frequencies, times)
            note_stats = note_converter.get_note_statistics(frequencies, times)
            piano_roll = note_converter.create_piano_roll_data(frequencies, times)
            
            # Step 4: Create visualizations
            status_text.text("Creating visualizations...")
            progress_bar.progress(70)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_prefix = os.path.join(OUTPUT_DIR, f"analysis_{timestamp}")
            
            visualizations = {}
            
            # Dashboard
            dashboard_path = f"{output_prefix}_dashboard.png"
            visualizer.create_summary_dashboard(
                audio_data, sr, times, frequencies, confidences,
                notes, note_stats, output_path=dashboard_path
            )
            visualizations['dashboard'] = dashboard_path
            
            # Pitch plot
            pitch_path = f"{output_prefix}_pitch.png"
            visualizer.plot_pitch_over_time(
                times, frequencies, confidences, output_path=pitch_path
            )
            visualizations['pitch'] = pitch_path
            
            # Notes plot
            notes_path = f"{output_prefix}_notes.png"
            visualizer.plot_notes_over_time(notes, output_path=notes_path)
            visualizations['notes'] = notes_path
            
            # Piano roll
            piano_roll_path = f"{output_prefix}_piano_roll.png"
            visualizer.plot_piano_roll(piano_roll, output_path=piano_roll_path)
            visualizations['piano_roll'] = piano_roll_path
            
            # Optional visualizations
            if show_waveform:
                waveform_path = f"{output_prefix}_waveform.png"
                visualizer.plot_waveform(audio_data, sr, output_path=waveform_path)
                visualizations['waveform'] = waveform_path
            
            if show_spectrogram:
                spec_path = f"{output_prefix}_spectrogram.png"
                visualizer.plot_spectrogram(audio_data, sr, output_path=spec_path)
                visualizations['spectrogram'] = spec_path
            
            if show_chromagram:
                chroma_path = f"{output_prefix}_chromagram.png"
                visualizer.plot_chromagram(audio_data, sr, output_path=chroma_path)
                visualizations['chromagram'] = chroma_path
            
            # Note distribution
            note_dist_path = f"{output_prefix}_note_distribution.png"
            visualizer.plot_note_distribution(note_stats, output_path=note_dist_path)
            visualizations['note_distribution'] = note_dist_path
            
            # Step 5: Export
            status_text.text("Exporting results...")
            progress_bar.progress(90)
            
            exports = {}
            
            if export_midi:
                midi_path = f"{output_prefix}.mid"
                midi_exporter.create_midi_from_segments(note_segments, midi_path)
                exports['midi'] = midi_path
            
            if export_json:
                json_path = f"{output_prefix}_analysis.json"
                json_data = {
                    'metadata': {
                        'timestamp': timestamp,
                        'pitch_method': pitch_method,
                        'sample_rate': sr,
                        'duration': len(audio_data) / sr,
                        'source_type': input_type,
                        'streaming_mode': input_type == 'stream'
                    },
                    'statistics': note_stats,
                    'notes': notes,
                    'segments': note_segments
                }
                if metadata:
                    json_data['metadata']['video_info'] = metadata
                
                with open(json_path, 'w') as f:
                    json.dump(json_data, f, indent=2)
                exports['json'] = json_path
            
            # Complete
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Store results
            st.session_state.results = {
                'audio_path': audio_path,
                'audio_data': audio_data,
                'sr': sr,
                'times': times,
                'frequencies': frequencies,
                'confidences': confidences,
                'notes': notes,
                'note_segments': note_segments,
                'note_stats': note_stats,
                'visualizations': visualizations,
                'exports': exports,
                'pitch_method': pitch_method
            }
            st.session_state.analysis_complete = True
            
            st.success("🎉 Analysis completed successfully! Check the Results tab.")
            st.balloons()
            
        except ValueError as e:
            # Handle streaming errors with helpful message
            error_msg = str(e)
            st.error(f"❌ Error during analysis")
            st.error(error_msg)
            
            # If it's a streaming error, offer fallback
            if input_type == 'stream' and 'Download & Analyze' in error_msg:
                st.warning("💡 **Tip:** Stream mode failed. Try these solutions:")
                st.info("""
                **Option 1: Use Download Mode**
                - More reliable
                - Works with restricted videos
                - Full song analysis
                
                **Option 2: Check the Video**
                - Make sure the video is public
                - Verify it's not age-restricted
                - Try a different video URL
                
                **Option 3: Check Network**
                - Verify internet connection
                - Disable VPN if enabled
                - Try again in a few moments
                """)
                
                # Show button to retry with download mode
                if st.button("🔄 Retry with Download Mode", key="retry_download"):
                    analyze_audio(source, pitch_method, smooth_pitch, remove_outliers,
                                show_waveform, show_spectrogram, show_chromagram,
                                export_midi, export_json, input_type='url')
            else:
                # Show debug info expander
                with st.expander("🐛 Debug Information"):
                    import traceback
                    st.code(traceback.format_exc())
                    
        except Exception as e:
            st.error(f"❌ Unexpected error during analysis: {str(e)}")
            with st.expander("🐛 Debug Information"):
                import traceback
                st.code(traceback.format_exc())
            
            st.warning("💡 **Troubleshooting Tips:**")
            st.info("""
            1. Check your internet connection
            2. Try a different video/audio file
            3. Restart the app if the issue persists
            4. Check that FFmpeg is installed correctly
            """)


def display_results(results):
    """
    Display analysis results
    
    Args:
        results: Dictionary with analysis results
    """
    
    st.header("📊 Analysis Results")
    
    # Audio information
    duration = len(results['audio_data']) / results['sr']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Duration", format_time(duration))
    with col2:
        st.metric("Sample Rate", f"{results['sr']} Hz")
    with col3:
        st.metric("Total Notes", results['note_stats']['total_notes'])
    with col4:
        st.metric("Unique Notes", results['note_stats']['unique_notes'])
    
    # Dashboard
    st.subheader("📈 Analysis Dashboard")
    if 'dashboard' in results['visualizations']:
        st.image(results['visualizations']['dashboard'], use_container_width=True)
    
    # Detailed visualizations
    st.subheader("🎼 Detailed Visualizations")
    
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "Pitch Over Time", "Musical Notes", "Piano Roll", "Note Distribution"
    ])
    
    with viz_tab1:
        if 'pitch' in results['visualizations']:
            st.image(results['visualizations']['pitch'], use_container_width=True)
    
    with viz_tab2:
        if 'notes' in results['visualizations']:
            st.image(results['visualizations']['notes'], use_container_width=True)
    
    with viz_tab3:
        if 'piano_roll' in results['visualizations']:
            st.image(results['visualizations']['piano_roll'], use_container_width=True)
    
    with viz_tab4:
        if 'note_distribution' in results['visualizations']:
            st.image(results['visualizations']['note_distribution'], use_container_width=True)
    
    # Optional visualizations
    if 'waveform' in results['visualizations'] or 'spectrogram' in results['visualizations']:
        st.subheader("🔊 Audio Visualizations")
        cols = st.columns(2)
        
        if 'waveform' in results['visualizations']:
            with cols[0]:
                st.image(results['visualizations']['waveform'], use_container_width=True)
        
        if 'spectrogram' in results['visualizations']:
            with cols[1]:
                st.image(results['visualizations']['spectrogram'], use_container_width=True)
    
    # Statistics
    st.subheader("📊 Note Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Most Common Notes:**")
        for note, count in results['note_stats']['most_common'][:10]:
            st.text(f"{note}: {count} times")
    
    with col2:
        st.markdown("**Frequency Statistics:**")
        st.text(f"Average: {results['note_stats']['avg_frequency']:.1f} Hz")
        st.text(f"Octave Range: {results['note_stats']['octave_range']}")
    
    # Export downloads
    if results['exports']:
        st.subheader("💾 Download Exports")
        cols = st.columns(len(results['exports']))
        
        for i, (export_type, export_path) in enumerate(results['exports'].items()):
            with cols[i]:
                with open(export_path, 'rb') as f:
                    btn_label = f"Download {export_type.upper()}"
                    st.download_button(
                        label=btn_label,
                        data=f,
                        file_name=os.path.basename(export_path),
                        mime='application/octet-stream'
                    )
    
    # Raw data
    with st.expander("🔍 View Raw Data"):
        st.json({
            'total_frames': len(results['times']),
            'detected_pitches': len([f for f in results['frequencies'] if f > 0]),
            'pitch_coverage': f"{len([f for f in results['frequencies'] if f > 0]) / len(results['frequencies']) * 100:.1f}%",
            'method': results['pitch_method']
        })



def display_comparison_tab():
    """Display the song comparison interface"""
    st.header("🔍 Compare Two Songs")
    st.markdown("""
    Compare your song with an original to see how similar they are!
    
    Upload or select JSON analysis files from both songs to get:
    - **Overall similarity score** with letter grade
    - **Note-by-note comparison** showing which notes match
    - **Timing analysis** showing how accurate your timing is
    - **Missing notes** that you didn't hit
    - **Extra notes** that weren't in the original
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Original Song")
        
        # Option to select from analyzed files
        output_files = []
        if os.path.exists(OUTPUT_DIR):
            output_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('_analysis.json')]
        
        original_method = st.radio(
            "Select original song:",
            options=["From analyzed files", "Upload JSON file"],
            key="original_method"
        )
        
        original_json = None
        if original_method == "From analyzed files":
            if output_files:
                selected_original = st.selectbox(
                    "Choose analyzed song:",
                    options=output_files,
                    key="original_select"
                )
                if selected_original:
                    original_json = os.path.join(OUTPUT_DIR, selected_original)
            else:
                st.warning("No analyzed songs found. Analyze a song first!")
        else:
            uploaded_original = st.file_uploader(
                "Upload original song JSON",
                type=['json'],
                key="original_upload"
            )
            if uploaded_original:
                # Save temporarily
                original_json = os.path.join(TEMP_DIR, "original_temp.json")
                with open(original_json, 'wb') as f:
                    f.write(uploaded_original.getbuffer())
        
        if original_json and os.path.exists(original_json):
            st.success(f"✅ Original loaded: {os.path.basename(original_json)}")
            # Show preview
            with open(original_json, 'r') as f:
                orig_data = json.load(f)
                st.info(f"📊 Notes: {len(orig_data.get('notes', []))}")
    
    with col2:
        st.subheader("🎤 Your Song")
        
        comparison_method = st.radio(
            "Select your song:",
            options=["From analyzed files", "Upload JSON file"],
            key="comparison_method"
        )
        
        comparison_json = None
        if comparison_method == "From analyzed files":
            if output_files:
                selected_comparison = st.selectbox(
                    "Choose analyzed song:",
                    options=output_files,
                    key="comparison_select"
                )
                if selected_comparison:
                    comparison_json = os.path.join(OUTPUT_DIR, selected_comparison)
            else:
                st.warning("No analyzed songs found. Analyze a song first!")
        else:
            uploaded_comparison = st.file_uploader(
                "Upload your song JSON",
                type=['json'],
                key="comparison_upload"
            )
            if uploaded_comparison:
                # Save temporarily
                comparison_json = os.path.join(TEMP_DIR, "comparison_temp.json")
                with open(comparison_json, 'wb') as f:
                    f.write(uploaded_comparison.getbuffer())
        
        if comparison_json and os.path.exists(comparison_json):
            st.success(f"✅ Your song loaded: {os.path.basename(comparison_json)}")
            # Show preview
            with open(comparison_json, 'r') as f:
                comp_data = json.load(f)
                st.info(f"📊 Notes: {len(comp_data.get('notes', []))}")
    
    # Comparison settings
    st.markdown("---")
    st.subheader("⚙️ Comparison Settings")
    time_tolerance = st.slider(
        "Time tolerance (seconds)",
        min_value=0.1,
        max_value=2.0,
        value=0.5,
        step=0.1,
        help="Notes within this time window will be considered as matching"
    )
    
    # Compare button
    if st.button("🔍 Compare Songs", key="compare_btn"):
        if not original_json or not comparison_json:
            st.error("❌ Please select both songs to compare")
        elif not os.path.exists(original_json) or not os.path.exists(comparison_json):
            st.error("❌ One or both JSON files not found")
        else:
            with st.spinner("Analyzing similarities..."):
                try:
                    # Create comparator
                    comparator = SongComparator(time_tolerance=time_tolerance)
                    
                    # Compare songs
                    comparison_results = comparator.compare_songs(original_json, comparison_json)
                    
                    # Display results
                    st.success("✅ Comparison complete!")
                    
                    # Overall Score
                    st.markdown("---")
                    st.markdown("## 🎯 Overall Score")
                    
                    score = comparison_results['overall_score']
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Overall Similarity", f"{score['overall_similarity_score']}%")
                    with col2:
                        st.metric("Grade", score['grade'])
                    with col3:
                        st.metric("Note Match", f"{score['note_matching_score']}%")
                    with col4:
                        st.metric("Timing", f"{score['timing_accuracy_score']}%")
                    
                    # Progress bar for overall score
                    st.progress(score['overall_similarity_score'] / 100)
                    
                    # Detailed breakdown
                    st.markdown("---")
                    st.markdown("## 📊 Detailed Analysis")
                    
                    tab_dist, tab_match, tab_timing = st.tabs(["Note Distribution", "Note Matching", "Timing Analysis"])
                    
                    with tab_dist:
                        dist = comparison_results['note_distribution']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Notes", dist['total_notes_original'])
                        with col2:
                            st.metric("Your Notes", dist['total_notes_comparison'])
                        with col3:
                            st.metric("Common Notes", dist['common_notes_count'])
                        
                        st.markdown("### Common Notes")
                        st.info(", ".join(dist['common_notes']))
                        
                        if dist['notes_only_in_original']:
                            st.markdown("### ❌ Missing Notes (in original but not in yours)")
                            st.warning(", ".join(dist['notes_only_in_original']))
                        
                        if dist['notes_only_in_comparison']:
                            st.markdown("### ➕ Extra Notes (in yours but not in original)")
                            st.info(", ".join(dist['notes_only_in_comparison']))
                    
                    with tab_match:
                        match = comparison_results['note_matching']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Matched Notes", match['matching_notes_count'])
                        with col2:
                            st.metric("Match %", f"{match['match_percentage']}%")
                        with col3:
                            st.metric("Unmatched", match['unmatched_original_count'])
                        
                        st.markdown("### Matched Notes Sample")
                        if match['matching_notes']:
                            match_data = []
                            for m in match['matching_notes'][:20]:
                                match_data.append({
                                    'Note': m['note'],
                                    'Original Time': f"{m['original_time']:.2f}s",
                                    'Your Time': f"{m['comparison_time']:.2f}s",
                                    'Time Diff': f"{m['time_difference']:.3f}s",
                                    'Freq Diff': f"{m['frequency_difference_hz']:.1f}Hz"
                                })
                            st.dataframe(match_data, use_container_width=True)
                        
                        if match['unmatched_in_original']:
                            st.markdown("### Missing Notes Details")
                            with st.expander("Show missing notes"):
                                for note in match['unmatched_in_original'][:20]:
                                    st.text(f"❌ {note['note']} @ {note['time']:.2f}s")
                    
                    with tab_timing:
                        timing = comparison_results['timing_analysis']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Avg Time Diff", f"{timing['average_time_difference']:.3f}s")
                        with col2:
                            st.metric("Timing Accuracy", f"{timing['timing_accuracy_percentage']:.1f}%")
                        with col3:
                            st.metric("Max Time Diff", f"{timing['max_time_difference']:.3f}s")
                        
                        st.info(f"""
                        **Timing Statistics:**
                        - Minimum difference: {timing['min_time_difference']:.3f}s
                        - Standard deviation: {timing['std_time_difference']:.3f}s
                        
                        Lower values indicate better timing accuracy!
                        """)
                    
                    # Generate and download report
                    st.markdown("---")
                    st.markdown("## 📄 Download Report")
                    
                    report = comparator.generate_comparison_report(comparison_results)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download Text Report",
                            data=report,
                            file_name=f"comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        st.download_button(
                            label="📥 Download JSON Report",
                            data=json.dumps(comparison_results, indent=2),
                            file_name=f"comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    # Show text report in expander
                    with st.expander("📄 View Text Report"):
                        st.text(report)
                    
                except Exception as e:
                    st.error(f"❌ Error during comparison: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())


def display_microphone_tab():
    """Display the live microphone recording interface"""
    from src.microphone_input import MicrophoneRecorder
    
    st.header("🎤 Live Microphone Analysis")
    st.markdown("""
    Record your voice directly and see the musical notes in real-time!
    Perfect for vocal practice and checking your pitch accuracy.
    """)
    
    # Initialize session state for microphone
    if 'mic_recorded_audio' not in st.session_state:
        st.session_state.mic_recorded_audio = None
    if 'mic_sample_rate' not in st.session_state:
        st.session_state.mic_sample_rate = None
    
    # Microphone settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Recording Settings")
        
        # Get available devices
        try:
            recorder = MicrophoneRecorder()
            devices = recorder.list_devices()
            default_device = recorder.get_default_device()
            
            if devices:
                device_names = [f"{d['name']} ({d['index']})" for d in devices]
                default_idx = 0
                
                if default_device:
                    try:
                        default_idx = next(i for i, d in enumerate(devices) if d['index'] == default_device['index'])
                    except StopIteration:
                        pass
                
                selected_device_name = st.selectbox(
                    "🎙️ Select Microphone",
                    options=device_names,
                    index=default_idx
                )
                
                # Extract device index from selection
                selected_device_idx = devices[[d['name'] in selected_device_name for d in devices].index(True)]['index']
                
                st.success(f"✅ Using: {selected_device_name}")
            else:
                st.error("❌ No microphone devices found!")
                selected_device_idx = None
                
        except Exception as e:
            st.error(f"❌ Error detecting microphones: {str(e)}")
            selected_device_idx = None
        
        recording_duration = st.slider(
            "⏱️ Recording Duration (seconds)",
            min_value=5,
            max_value=60,
            value=10,
            step=5,
            help="How long to record your voice"
        )
        
        # Test microphone button
        if st.button("🔊 Test Microphone", help="Quick 2-second test to verify mic is working"):
            if selected_device_idx is not None:
                with st.spinner("Testing microphone..."):
                    try:
                        test_recorder = MicrophoneRecorder()
                        is_working = test_recorder.test_microphone(duration=2.0)
                        
                        if is_working:
                            st.success("✅ Microphone is working! You can start recording.")
                        else:
                            st.warning("⚠️ Microphone detected but no sound detected. Check your mic volume.")
                    except Exception as e:
                        st.error(f"❌ Microphone test failed: {str(e)}")
            else:
                st.error("Please select a microphone first")
    
    with col2:
        st.subheader("🎵 Analysis Options")
        
        # Analysis settings (same as other input methods)
        mic_pitch_method = st.selectbox(
            "Pitch Detection Method",
            options=['crepe', 'librosa', 'aubio'],
            key="mic_pitch_method",
            help="CREPE is most accurate for vocals"
        )
        
        mic_smooth = st.checkbox("Smooth pitch", value=True, key="mic_smooth")
        mic_remove_outliers = st.checkbox("Remove outliers", value=True, key="mic_outliers")
        
        st.info("💡 **Tip:** Sing clearly into the mic for best results!")
    
    # Recording section
    st.markdown("---")
    st.subheader("🎙️ Record Your Voice")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔴 Start Recording", type="primary", use_container_width=True):
            if selected_device_idx is not None:
                with st.spinner(f"Recording for {recording_duration} seconds... 🎤"):
                    try:
                        mic_recorder = MicrophoneRecorder()
                        
                        # Show countdown
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Record with progress updates
                        import sounddevice as sd
                        audio_data = sd.rec(
                            int(recording_duration * mic_recorder.sample_rate),
                            samplerate=mic_recorder.sample_rate,
                            channels=1,
                            device=selected_device_idx,
                            dtype='float32'
                        )
                        
                        # Show progress
                        for i in range(recording_duration):
                            progress_bar.progress((i + 1) / recording_duration)
                            status_text.text(f"Recording... {i + 1}/{recording_duration} seconds")
                            time.sleep(1)
                        
                        sd.wait()
                        
                        audio_data = audio_data.flatten()
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Recording complete!")
                        
                        # Store in session state
                        st.session_state.mic_recorded_audio = audio_data
                        st.session_state.mic_sample_rate = mic_recorder.sample_rate
                        
                        # Show audio info
                        st.success(f"✅ Recorded {len(audio_data) / mic_recorder.sample_rate:.1f} seconds")
                        
                        # Show audio level
                        rms = np.sqrt(np.mean(audio_data ** 2))
                        st.metric("Audio Level", f"{rms:.4f}")
                        
                        if rms < 0.001:
                            st.warning("⚠️ Very low audio level detected. Speak louder or adjust mic volume.")
                        
                    except Exception as e:
                        st.error(f"❌ Recording failed: {str(e)}")
                        st.info("💡 Try: Check mic permissions, volume, or select a different device")
            else:
                st.error("Please select a microphone device first")
    
    with col2:
        # Show playback option if audio is recorded
        if st.session_state.mic_recorded_audio is not None:
            st.download_button(
                label="💾 Save Recording",
                data=st.session_state.mic_recorded_audio.tobytes(),
                file_name=f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.raw",
                mime="application/octet-stream",
                use_container_width=True
            )
    
    with col3:
        if st.session_state.mic_recorded_audio is not None:
            if st.button("🎵 Analyze Recording", type="primary", use_container_width=True):
                # Analyze the recorded audio
                audio_data = st.session_state.mic_recorded_audio
                sr = st.session_state.mic_sample_rate
                
                with st.spinner("Analyzing your voice... 🎵"):
                    try:
                        # Use the same analysis pipeline
                        audio_processor = AudioProcessor()
                        pitch_detector = PitchDetector()
                        note_converter = NoteConverter()
                        visualizer = AudioVisualizer()
                        
                        # Normalize audio
                        audio_data = audio_processor.normalize_audio(audio_data)
                        audio_data = audio_processor.trim_silence(audio_data)
                        
                        if len(audio_data) == 0:
                            st.error("❌ No audio detected after silence removal. Please record again and speak/sing louder.")
                            return
                        
                        # Detect pitch
                        times, frequencies, confidences = pitch_detector.detect_pitch(
                            audio_data, method=mic_pitch_method
                        )
                        
                        # Post-process
                        if mic_smooth or mic_remove_outliers:
                            frequencies = pitch_detector.post_process_pitch(
                                frequencies, confidences,
                                smooth=mic_smooth,
                                remove_outliers_flag=mic_remove_outliers
                            )
                        
                        # Convert to notes
                        notes = note_converter.frequencies_to_notes(frequencies, times)
                        
                        if not notes:
                            st.warning("⚠️ No clear notes detected. Try singing louder or clearer.")
                            return
                        
                        note_stats = note_converter.get_note_statistics(frequencies, times)
                        
                        # Display results in real-time
                        st.success(f"✅ Detected {len(notes)} notes!")
                        
                        # Show note statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Notes", note_stats['total_notes'])
                        with col2:
                            st.metric("Unique Notes", note_stats['unique_notes'])
                        with col3:
                            st.metric("Avg Frequency", f"{note_stats['avg_frequency']:.1f} Hz")
                        
                        # Show most common notes
                        st.subheader("🎵 Your Most Common Notes")
                        top_notes = note_stats['most_common'][:10]
                        
                        # Create a nice display
                        note_cols = st.columns(min(len(top_notes), 5))
                        for i, (note, count) in enumerate(top_notes[:5]):
                            with note_cols[i]:
                                st.metric(note, f"{count}x")
                        
                        # Visualize notes over time
                        st.subheader("📈 Your Notes Over Time")
                        
                        # Create visualization
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_prefix = os.path.join(OUTPUT_DIR, f"mic_recording_{timestamp}")
                        
                        notes_path = f"{output_prefix}_notes.png"
                        visualizer.plot_notes_over_time(notes, output_path=notes_path)
                        st.image(notes_path, use_container_width=True)
                        
                        # Show pitch plot
                        pitch_path = f"{output_prefix}_pitch.png"
                        visualizer.plot_pitch_over_time(
                            times, frequencies, confidences, output_path=pitch_path
                        )
                        st.image(pitch_path, use_container_width=True)
                        
                        # Show note distribution
                        st.subheader("📊 Note Distribution")
                        dist_path = f"{output_prefix}_distribution.png"
                        visualizer.plot_note_distribution(note_stats, output_path=dist_path)
                        st.image(dist_path, use_container_width=True)
                        
                        # Export options
                        st.markdown("---")
                        st.subheader("💾 Export Your Recording")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Export MIDI
                            note_segments = note_converter.get_note_segments(frequencies, times)
                            midi_exporter = MidiExporter()
                            midi_path = f"{output_prefix}.mid"
                            midi_exporter.create_midi_from_segments(note_segments, midi_path)
                            
                            with open(midi_path, 'rb') as f:
                                st.download_button(
                                    label="🎹 Download MIDI",
                                    data=f,
                                    file_name=os.path.basename(midi_path),
                                    mime="audio/midi"
                                )
                        
                        with col2:
                            # Export JSON
                            json_path = f"{output_prefix}_analysis.json"
                            json_data = {
                                'metadata': {
                                    'timestamp': timestamp,
                                    'source': 'microphone',
                                    'duration': len(audio_data) / sr,
                                    'pitch_method': mic_pitch_method
                                },
                                'statistics': note_stats,
                                'notes': notes,
                                'segments': note_segments
                            }
                            
                            with open(json_path, 'w') as f:
                                json.dump(json_data, f, indent=2)
                            
                            with open(json_path, 'rb') as f:
                                st.download_button(
                                    label="📄 Download JSON",
                                    data=f,
                                    file_name=os.path.basename(json_path),
                                    mime="application/json"
                                )
                        
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        with st.expander("Debug Info"):
                            import traceback
                            st.code(traceback.format_exc())
    
    # Tips section
    st.markdown("---")
    st.subheader("💡 Tips for Best Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Recording Tips:**
        - 🎤 Position mic 6-12 inches from mouth
        - 🔇 Record in quiet environment
        - 📢 Sing clearly and steadily
        - 🎵 Try scales or single notes first
        - ✅ Test mic before recording
        """)
    
    with col2:
        st.success("""
        **What You'll See:**
        - 🎵 Musical notes you sang
        - 📊 Note frequency distribution
        - 📈 Pitch accuracy over time
        - 🎹 MIDI file of your performance
        - 📄 Detailed analysis data
        """)
    
    # Footer branding
    st.markdown("""
    <div class="footer-branding">
        <p>
            <span class="brand-name">Raga Musikraum</span> | 
            Developed by: <a href="https://www.dinexora.de" target="_blank">Dinexora</a> | 
            © 2025 | 🎵 Empowering Music Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
