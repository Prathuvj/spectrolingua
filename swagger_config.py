from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


schema_view = get_schema_view(
    openapi.Info(
        title="Audio Converter & Waveform Generator API",
        default_version='v1',
        description="""
        A comprehensive audio processing API that provides:
        
        🎵 **Audio Format Conversion**: Convert various audio formats to WAV
        📊 **Waveform Visualization**: Generate beautiful waveform images from audio files
        🔬 **Spectrogram Analysis**: Create STFT spectrograms with log-frequency scale
        🎤 **Speech Transcription**: Convert speech to text using Google Speech Recognition
        ✅ **Format Support**: MP3, MP4, WAV, FLAC, AAC, OGG, WMA, M4A, AIFF
        
        ## Features
        - High-quality audio conversion using librosa
        - Professional waveform visualizations with matplotlib
        - Automatic file downloads with proper naming
        - Smart detection for files already in target format
        - RESTful API design with comprehensive documentation
        
        ## Usage
        1. **Convert Audio**: Upload any supported audio file to `/convert/` to get WAV output
        2. **Generate Waveform**: Upload audio to `/waveform/` to get PNG visualization
        3. **Generate Spectrogram**: Upload audio to `/spectrogram/` to get STFT analysis
        4. **Transcribe Speech**: Upload audio to `/transcribe/` to get text transcription
        5. **Check Formats**: Use `/formats/` to see all supported audio formats
        6. **Check Languages**: Use `/languages/` to see supported transcription languages
        7. **Health Check**: Use `/health/` to verify API status
        
        ## Endpoints Overview
        
        ### Audio Conversion
        - `POST /convert/` - Convert audio files to WAV format
        
        ### Audio Visualization  
        - `POST /waveform/` - Generate waveform visualizations
        - `POST /spectrogram/` - Generate STFT spectrogram analysis
        
        ### Audio Processing
        - `POST /transcribe/` - Transcribe speech to text using Google Speech Recognition
        
        ### Information
        - `GET /formats/` - List supported audio formats
        - `GET /languages/` - List supported transcription languages
        - `GET /health/` - API health check
        
        ### Documentation
        - `GET /docs/` - Interactive API documentation (Swagger UI)
        - `GET /redoc/` - Alternative documentation (ReDoc)
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(
            name="Audio API Support",
            email="support@audioapi.local",
            url="https://www.example.com/contact/"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)