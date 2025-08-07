import streamlit as st
import requests
import io
import time
from PIL import Image
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Audio Processing Studio",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE_URL = "http://127.0.0.1:8000"

def check_api_health():
    """Check if the Django API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_supported_formats():
    """Get supported audio formats from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/formats/")
        if response.status_code == 200:
            return response.json().get('supported_formats', [])
    except:
        pass
    return ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a']

def get_supported_languages():
    """Get supported transcription languages from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/languages/")
        if response.status_code == 200:
            return response.json().get('supported_languages', {})
    except:
        pass
    return {'en-US': 'English (US)', 'es-ES': 'Spanish (Spain)', 'fr-FR': 'French (France)'}

def convert_audio(audio_file, filename):
    """Convert audio to WAV format"""
    files = {'audio_file': (filename, audio_file, 'audio/*')}
    
    with st.spinner('Converting audio to WAV...'):
        try:
            response = requests.post(f"{API_BASE_URL}/convert/", files=files)
            
            if response.status_code == 200:
                if response.headers.get('content-type') == 'audio/wav':
                    return response.content, None
                else:
                    # JSON response (file already WAV)
                    return None, response.json().get('message', 'File is already in WAV format')
            else:
                error_msg = response.json().get('error', 'Conversion failed')
                return None, f"Error: {error_msg}"
        except Exception as e:
            return None, f"Error: {str(e)}"

def generate_waveform(audio_file, filename):
    """Generate waveform visualization"""
    files = {'audio_file': (filename, audio_file, 'audio/*')}
    
    with st.spinner('Generating waveform...'):
        try:
            response = requests.post(f"{API_BASE_URL}/waveform/", files=files)
            
            if response.status_code == 200:
                return response.content, None
            else:
                error_msg = response.json().get('error', 'Waveform generation failed')
                return None, f"Error: {error_msg}"
        except Exception as e:
            return None, f"Error: {str(e)}"

def generate_spectrogram(audio_file, filename):
    """Generate spectrogram visualization"""
    files = {'audio_file': (filename, audio_file, 'audio/*')}
    
    with st.spinner('Generating spectrogram...'):
        try:
            response = requests.post(f"{API_BASE_URL}/spectrogram/", files=files)
            
            if response.status_code == 200:
                return response.content, None
            else:
                error_msg = response.json().get('error', 'Spectrogram generation failed')
                return None, f"Error: {error_msg}"
        except Exception as e:
            return None, f"Error: {str(e)}"

def transcribe_audio(audio_file, filename, language='en-US'):
    """Transcribe audio to text"""
    files = {'audio_file': (filename, audio_file, 'audio/*')}
    data = {'language': language}
    
    with st.spinner('Transcribing audio...'):
        try:
            response = requests.post(f"{API_BASE_URL}/transcribe/", files=files, data=data)
            
            if response.status_code == 200:
                return response.json(), None
            else:
                error_msg = response.json().get('error', 'Transcription failed')
                return None, f"Error: {error_msg}"
        except Exception as e:
            return None, f"Error: {str(e)}"

def main():
    # Header
    st.title("🎵 Audio Processing Studio")
    st.markdown("### Professional Audio Conversion, Visualization & Transcription")
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ Django API is not running! Please start the backend server first.")
        st.info("Run: `python main.py` to start both backend and frontend")
        st.stop()
    
    st.success("✅ Backend API is running")
    
    # Sidebar
    st.sidebar.header("🎛️ Audio Processing Options")
    
    # Get supported formats and languages
    supported_formats = get_supported_formats()
    supported_languages = get_supported_languages()
    
    # File upload
    st.sidebar.subheader("📁 Upload Audio File")
    uploaded_file = st.sidebar.file_uploader(
        "Choose an audio file",
        type=supported_formats,
        help=f"Supported formats: {', '.join(supported_formats)}"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
        st.sidebar.info(f"📊 File size: {uploaded_file.size / 1024:.1f} KB")
        
        # Operation selection
        st.sidebar.subheader("🔧 Select Operation")
        operation = st.sidebar.selectbox(
            "Choose what you want to do:",
            [
                "🎵 Convert to WAV",
                "📊 Generate Waveform",
                "🔬 Generate Spectrogram", 
                "🎤 Transcribe to Text"
            ]
        )
        
        # Language selection for transcription
        if "Transcribe" in operation:
            st.sidebar.subheader("🌐 Language Settings")
            language_code = st.sidebar.selectbox(
                "Select language:",
                options=list(supported_languages.keys()),
                format_func=lambda x: supported_languages[x],
                index=0
            )
        
        # Process button
        if st.sidebar.button("🚀 Process Audio", type="primary"):
            # Read file content
            audio_content = uploaded_file.read()
            uploaded_file.seek(0)  # Reset file pointer
            
            # Main content area
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.header("📋 Processing Results")
                
                if "Convert" in operation:
                    wav_data, error = convert_audio(io.BytesIO(audio_content), uploaded_file.name)
                    
                    if error:
                        st.error(error)
                    elif wav_data:
                        st.success("✅ Audio converted to WAV successfully!")
                        st.download_button(
                            label="📥 Download WAV File",
                            data=wav_data,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.wav",
                            mime="audio/wav"
                        )
                        
                        # Audio player
                        st.audio(wav_data, format='audio/wav')
                    else:
                        st.info("ℹ️ File is already in WAV format")
                        st.audio(audio_content, format='audio/wav')
                
                elif "Waveform" in operation:
                    waveform_data, error = generate_waveform(io.BytesIO(audio_content), uploaded_file.name)
                    
                    if error:
                        st.error(error)
                    else:
                        st.success("✅ Waveform generated successfully!")
                        
                        # Display waveform image
                        image = Image.open(io.BytesIO(waveform_data))
                        st.image(image, caption="Audio Waveform Visualization", use_column_width=True)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Waveform Image",
                            data=waveform_data,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_waveform.png",
                            mime="image/png"
                        )
                
                elif "Spectrogram" in operation:
                    spectrogram_data, error = generate_spectrogram(io.BytesIO(audio_content), uploaded_file.name)
                    
                    if error:
                        st.error(error)
                    else:
                        st.success("✅ Spectrogram generated successfully!")
                        
                        # Display spectrogram image
                        image = Image.open(io.BytesIO(spectrogram_data))
                        st.image(image, caption="STFT Spectrogram (Log-Frequency Scale)", use_column_width=True)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Spectrogram Image",
                            data=spectrogram_data,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_spectrogram.png",
                            mime="image/png"
                        )
                
                elif "Transcribe" in operation:
                    transcription_result, error = transcribe_audio(
                        io.BytesIO(audio_content), 
                        uploaded_file.name, 
                        language_code
                    )
                    
                    if error:
                        st.error(error)
                    else:
                        st.success("✅ Audio transcribed successfully!")
                        
                        # Display transcription
                        st.subheader("📝 Transcription Result")
                        st.text_area(
                            "Transcribed Text:",
                            value=transcription_result['transcription'],
                            height=200,
                            help="Copy the text from here"
                        )
                        
                        # Metadata
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.info(f"🌐 Language: {supported_languages.get(transcription_result['language'], transcription_result['language'])}")
                        with col_b:
                            st.info(f"📁 File: {transcription_result['filename']}")
                        
                        # Download as text file
                        st.download_button(
                            label="📥 Download Transcription",
                            data=transcription_result['transcription'],
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_transcription.txt",
                            mime="text/plain"
                        )
            
            with col2:
                st.header("ℹ️ File Information")
                st.info(f"**Filename:** {uploaded_file.name}")
                st.info(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
                st.info(f"**Type:** {uploaded_file.type}")
                
                # Original audio player
                st.subheader("🎧 Original Audio")
                st.audio(audio_content)
                
                # API Documentation link
                st.subheader("📚 API Documentation")
                st.markdown(f"[View API Docs]({API_BASE_URL}/docs/)")
    
    else:
        # Welcome screen
        st.header("🎵 Welcome to Audio Processing Studio")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("🎵 Convert")
            st.write("Convert audio files to WAV format with high quality")
            
        with col2:
            st.subheader("📊 Visualize")
            st.write("Generate beautiful waveform visualizations")
            
        with col3:
            st.subheader("🔬 Analyze")
            st.write("Create STFT spectrograms with log-frequency scale")
            
        with col4:
            st.subheader("🎤 Transcribe")
            st.write("Convert speech to text in 35+ languages")
        
        st.markdown("---")
        st.info("👆 Upload an audio file from the sidebar to get started!")
        
        # Supported formats
        st.subheader("📋 Supported Audio Formats")
        format_cols = st.columns(len(supported_formats))
        for i, fmt in enumerate(supported_formats):
            format_cols[i].code(fmt.upper())
        
        # Features
        st.subheader("✨ Features")
        features = [
            "🎵 High-quality audio conversion using librosa",
            "📊 Professional waveform visualizations",
            "🔬 STFT spectrogram analysis with log-frequency scale",
            "🎤 Speech transcription with Google Speech Recognition",
            "🌐 Support for 35+ languages",
            "📱 Responsive web interface",
            "⚡ Fast processing and real-time results",
            "📥 Easy download of processed files"
        ]
        
        for feature in features:
            st.markdown(f"- {feature}")

if __name__ == "__main__":
    main()