# 🎵 Audio Processing Studio

A comprehensive audio processing API with a modern web interface for audio conversion, visualization, and transcription.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-v4.2.7-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28.1-red.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

### 🎵 Audio Format Conversion
- Convert between multiple audio formats (MP3, MP4, WAV, FLAC, AAC, OGG, WMA, M4A, AIFF)
- High-quality conversion using librosa
- Automatic format detection and smart handling
- Download converted files instantly

### 📊 Audio Visualization
- **Waveform Generation**: Create professional waveform visualizations
- **Spectrogram Analysis**: Generate STFT spectrograms with log-frequency scale
- High-resolution PNG output (150 DPI)
- Professional styling with grids, labels, and colorbars

### 🎤 Speech Transcription
- Convert speech to text using Google Speech Recognition API
- Support for 35+ languages and dialects
- Automatic audio format conversion for transcription
- Language detection and customization

### 🌐 Modern Web Interface
- Intuitive Streamlit-based frontend
- Real-time processing with progress indicators
- Interactive audio players
- One-click file downloads
- Responsive design

### 🔧 Developer-Friendly API
- RESTful API design
- Comprehensive Swagger/OpenAPI documentation
- Organized endpoint categories
- Detailed error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd spectrolingua
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   - **Web Interface**: http://localhost:8501
   - **API Documentation**: http://127.0.0.1:8000/docs/
   - **Alternative Docs**: http://127.0.0.1:8000/redoc/

## 📖 Usage

### Web Interface

1. **Upload Audio File**: Use the sidebar to upload any supported audio format
2. **Select Operation**: Choose from conversion, waveform, spectrogram, or transcription
3. **Configure Options**: Set language for transcription (optional)
4. **Process**: Click "Process Audio" to start
5. **Download Results**: Get your processed files instantly

### API Endpoints

#### Audio Conversion
```bash
# Convert audio to WAV
curl -X POST http://127.0.0.1:8000/convert/ \
  -F "audio_file=@your_audio.mp3"
```

#### Waveform Generation
```bash
# Generate waveform visualization
curl -X POST http://127.0.0.1:8000/waveform/ \
  -F "audio_file=@your_audio.wav"
```

#### Spectrogram Analysis
```bash
# Generate STFT spectrogram
curl -X POST http://127.0.0.1:8000/spectrogram/ \
  -F "audio_file=@your_audio.wav"
```

#### Speech Transcription
```bash
# Transcribe speech to text
curl -X POST http://127.0.0.1:8000/transcribe/ \
  -F "audio_file=@your_speech.wav" \
  -F "language=en-US"
```

#### Information Endpoints
```bash
# Get supported audio formats
curl http://127.0.0.1:8000/formats/

# Get supported languages
curl http://127.0.0.1:8000/languages/

# Health check
curl http://127.0.0.1:8000/health/
```

## 🏗️ Architecture

### Project Structure
```
spectrolingua/
├── main.py                 # Main application entry point
├── api_endpoints.py        # API endpoint implementations
├── swagger_config.py       # API documentation configuration
├── streamlit_app.py        # Web interface frontend
├── format_conversion.py    # Audio format conversion logic
├── waveform.py            # Waveform generation logic
├── spectrogram.py         # Spectrogram generation logic
├── transcribe.py          # Speech transcription logic
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License file
├── install_ffmpeg.md      # FFmpeg installation guide
└── README.md             # This file
```

### Technology Stack

#### Backend
- **Django**: Web framework and API server
- **Django REST Framework**: RESTful API development
- **drf-yasg**: Swagger/OpenAPI documentation

#### Audio Processing
- **librosa**: Audio analysis and processing
- **soundfile**: Audio file I/O
- **matplotlib**: Visualization generation
- **SpeechRecognition**: Speech-to-text conversion

#### Frontend
- **Streamlit**: Web interface framework
- **Pillow**: Image processing
- **requests**: HTTP client for API communication

## 🎯 Supported Formats

### Audio Formats
- **MP3** - MPEG Audio Layer III
- **MP4** - MPEG-4 Audio
- **WAV** - Waveform Audio File Format
- **FLAC** - Free Lossless Audio Codec
- **AAC** - Advanced Audio Coding
- **OGG** - Ogg Vorbis
- **WMA** - Windows Media Audio
- **M4A** - MPEG-4 Audio
- **AIFF** - Audio Interchange File Format

### Transcription Languages
- **English**: US, UK variants
- **Spanish**: Spain, Mexico variants
- **French**: France variant
- **German**: Germany variant
- **Italian**: Italy variant
- **Portuguese**: Brazil variant
- **Russian**: Russia variant
- **Japanese**: Japan variant
- **Korean**: South Korea variant
- **Chinese**: Simplified, Traditional variants
- **Arabic**: Saudi Arabia variant
- **Hindi**: India variant
- And 20+ more languages...

## ⚙️ Configuration

### Environment Variables
```bash
# Optional: Set custom ports
DJANGO_PORT=8000
STREAMLIT_PORT=8501

# Optional: Configure API settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Advanced Configuration

#### Audio Processing Settings
- **Sample Rate**: Configurable in conversion functions
- **FFT Size**: 2048 samples (spectrogram)
- **Hop Length**: 512 samples (spectrogram)
- **Image DPI**: 150 DPI for visualizations

#### API Settings
- **CORS**: Configured for cross-origin requests
- **File Upload**: Supports multipart/form-data
- **Rate Limiting**: Not implemented (add as needed)

## 🔧 Development

### Running in Development Mode

1. **Start Django API only**
   ```bash
   python main.py runserver 8000
   ```

2. **Start Streamlit frontend only**
   ```bash
   streamlit run streamlit_app.py --server.port 8501
   ```

3. **Start both services**
   ```bash
   python main.py
   ```

### Adding New Features

1. **New API Endpoint**:
   - Add function to `api_endpoints.py`
   - Add URL pattern to `main.py`
   - Update Swagger documentation

2. **New Audio Processing**:
   - Create new module (e.g., `new_feature.py`)
   - Import in `api_endpoints.py`
   - Add corresponding frontend UI

3. **Frontend Enhancement**:
   - Modify `streamlit_app.py`
   - Add new UI components
   - Update API integration

### Testing

```bash
# Test API endpoints
curl http://127.0.0.1:8000/health/

# Test with sample files
curl -X POST http://127.0.0.1:8000/convert/ \
  -F "audio_file=@sample.mp3"
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

#### 2. Port Already in Use
```bash
# Solution: Kill existing processes
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### 3. Audio Processing Errors
```bash
# Solution: Install system audio libraries
# Ubuntu/Debian
sudo apt-get install libsndfile1 ffmpeg

# macOS
brew install libsndfile ffmpeg

# Windows
# Download ffmpeg from https://ffmpeg.org/
```

#### 4. Transcription API Errors
- Check internet connection
- Verify audio file contains speech
- Try different language codes
- Ensure audio quality is sufficient

### Performance Optimization

#### For Large Files
- Consider implementing chunked processing
- Add progress tracking for long operations
- Implement caching for repeated operations

#### For High Traffic
- Add Redis caching
- Implement rate limiting
- Use production WSGI server (gunicorn)
- Add load balancing

## 📊 API Documentation

### Interactive Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/swagger.json

### Response Formats

#### Success Response (File Download)
```
Content-Type: audio/wav | image/png
Content-Disposition: attachment; filename="output.wav"
Content-Length: <file-size>
```

#### Success Response (JSON)
```json
{
  "transcription": "Hello, this is a sample transcription.",
  "language": "en-US",
  "filename": "sample.wav"
}
```

#### Error Response
```json
{
  "error": "Detailed error message"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to new functions
- Update documentation for new features
- Test thoroughly before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.