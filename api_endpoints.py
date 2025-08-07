from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from format_conversion import AudioConverter
from waveform import WaveformGenerator
from spectrogram import SpectrogramGenerator
from transcribe import AudioTranscriber
from swagger_config import *


@swagger_auto_schema(
    method='post',
    operation_summary="Convert Audio to WAV",
    operation_description="""
    Convert any supported audio file to WAV format with high quality.
    
    **Supported Input Formats:**
    - MP3, MP4, FLAC, AAC, OGG, WMA, M4A, AIFF
    
    **Behavior:**
    - If input is already WAV: Returns JSON message
    - If input is other format: Converts and returns WAV file for download
    
    **Output:**
    - WAV file with same name as input (extension changed to .wav)
    - Proper Content-Disposition headers for automatic download
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'audio_file': openapi.Schema(
                type=openapi.TYPE_FILE,
                description="Audio file to convert. Supports: mp3, mp4, wav, flac, aac, ogg, wma, m4a, aiff"
            )
        },
        required=['audio_file']
    ),
    responses={
        200: openapi.Response(
            description="Success - WAV file download or message if already WAV",
            examples={
                "application/json": {
                    "message": "The file is already in .wav format"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request - Missing or invalid file",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="No audio file provided"
                    )
                }
            )
        ),
        500: openapi.Response(
            description="Internal Server Error - Conversion failed",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Conversion failed"
                    )
                }
            )
        )
    },
    consumes=['multipart/form-data'],
    tags=['Audio Conversion']
)
@api_view(['POST'])
def convert_audio(request):
    try:
        if 'audio_file' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio_file']
        
        if not audio_file.name:
            return JsonResponse({'error': 'Invalid file'}, status=400)
        
        file_extension = audio_file.name.split('.')[-1].lower()
        
        if file_extension == 'wav':
            return JsonResponse({'message': 'The file is already in .wav format'})
        
        wav_data = AudioConverter.convert_to_wav(audio_file, audio_file.name)
        
        filename = audio_file.name.rsplit(".", 1)[0] + ".wav"
        response = HttpResponse(wav_data, content_type='audio/wav')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(wav_data)
        response['Cache-Control'] = 'no-cache'
        return response
        
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Conversion failed'}, status=500)


@swagger_auto_schema(
    method='get',
    operation_summary="Get Supported Audio Formats",
    operation_description="""
    Retrieve a comprehensive list of all audio formats supported by this API.
    
    **Use this endpoint to:**
    - Check format compatibility before uploading
    - Validate file extensions programmatically
    - Display supported formats in your application
    
    **Returns:** Array of supported file extensions (without dots)
    """,
    responses={
        200: openapi.Response(
            description="Successfully retrieved supported formats",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'supported_formats': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        example=["mp3", "mp4", "wav", "flac", "aac", "ogg", "wma", "m4a", "aiff"]
                    )
                }
            ),
            examples={
                "application/json": {
                    "supported_formats": ["mp3", "mp4", "wav", "flac", "aac", "ogg", "wma", "m4a", "aiff"]
                }
            }
        )
    },
    tags=['Information']
)
@api_view(['GET'])
def supported_formats(request):
    formats = AudioConverter.get_supported_formats()
    return JsonResponse({'supported_formats': formats})


@swagger_auto_schema(
    method='get',
    operation_summary="API Health Check",
    operation_description="""
    Verify that the API service is running and responsive.
    
    **Use this endpoint for:**
    - Service monitoring and uptime checks
    - Load balancer health probes
    - Application startup verification
    - API availability testing
    
    **Returns:** Simple status confirmation
    """,
    responses={
        200: openapi.Response(
            description="API is healthy and operational",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="healthy"
                    )
                }
            ),
            examples={
                "application/json": {
                    "status": "healthy"
                }
            }
        )
    },
    tags=['Information']
)
@api_view(['GET'])
def health_check(request):
    return JsonResponse({'status': 'healthy'})


@swagger_auto_schema(
    method='post',
    operation_summary="Generate Audio Waveform Visualization",
    operation_description="""
    Create a professional waveform visualization from any supported audio file.
    
    **Features:**
    - High-resolution PNG output (150 DPI)
    - Time axis in seconds with amplitude visualization
    - Professional styling with grid and labels
    - Automatic filename generation (original_name_waveform.png)
    
    **Supported Input Formats:**
    - All formats: MP3, MP4, WAV, FLAC, AAC, OGG, WMA, M4A, AIFF
    
    **Output:**
    - PNG image file ready for download
    - Dimensions: 12x6 inches at 150 DPI
    - Includes title, axis labels, and grid for professional appearance
    
    **Use Cases:**
    - Audio analysis and visualization
    - Music production and editing
    - Educational content creation
    - Audio quality assessment
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'audio_file': openapi.Schema(
                type=openapi.TYPE_FILE,
                description="Audio file to visualize. Accepts all supported formats: mp3, mp4, wav, flac, aac, ogg, wma, m4a, aiff"
            )
        },
        required=['audio_file']
    ),
    responses={
        200: openapi.Response(
            description="Success - PNG waveform image ready for download",
            headers={
                'Content-Type': openapi.Schema(type=openapi.TYPE_STRING, example='image/png'),
                'Content-Disposition': openapi.Schema(type=openapi.TYPE_STRING, example='attachment; filename="audio_waveform.png"')
            }
        ),
        400: openapi.Response(
            description="Bad Request - Missing or invalid audio file",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="No audio file provided"
                    )
                }
            )
        ),
        500: openapi.Response(
            description="Internal Server Error - Waveform generation failed",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Waveform generation failed"
                    )
                }
            )
        )
    },
    consumes=['multipart/form-data'],
    tags=['Audio Visualization']
)
@api_view(['POST'])
def generate_waveform(request):
    try:
        if 'audio_file' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio_file']
        
        if not audio_file.name:
            return JsonResponse({'error': 'Invalid file'}, status=400)
        
        waveform_data = WaveformGenerator.generate_waveform_from_file(audio_file, audio_file.name)
        
        filename = audio_file.name.rsplit(".", 1)[0] + "_waveform.png"
        response = HttpResponse(waveform_data, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(waveform_data)
        response['Cache-Control'] = 'no-cache'
        return response
        
    except Exception as e:
        return JsonResponse({'error': 'Waveform generation failed'}, status=500)


@swagger_auto_schema(
    method='post',
    operation_summary="Generate Audio Spectrogram Visualization",
    operation_description="""
    Create a professional STFT spectrogram visualization with log-frequency scale from any supported audio file.
    
    **Features:**
    - High-resolution PNG output (150 DPI)
    - STFT (Short-Time Fourier Transform) analysis
    - Log-frequency scale for better frequency resolution
    - Professional styling with colorbar and labels
    - Automatic filename generation (original_name_spectrogram.png)
    
    **Technical Details:**
    - FFT Size: 2048 samples
    - Hop Length: 512 samples
    - Frequency Range: 20 Hz to Nyquist frequency
    - Color Scale: Viridis colormap with dB magnitude
    
    **Supported Input Formats:**
    - All formats: MP3, MP4, WAV, FLAC, AAC, OGG, WMA, M4A, AIFF
    
    **Output:**
    - PNG image file ready for download
    - Dimensions: 14x8 inches at 150 DPI
    - Includes title, axis labels, colorbar, and grid for professional appearance
    
    **Use Cases:**
    - Audio frequency analysis
    - Music production and mastering
    - Sound engineering and acoustics
    - Educational content for signal processing
    - Audio quality assessment and debugging
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'audio_file': openapi.Schema(
                type=openapi.TYPE_FILE,
                description="Audio file to analyze. Accepts all supported formats: mp3, mp4, wav, flac, aac, ogg, wma, m4a, aiff"
            )
        },
        required=['audio_file']
    ),
    responses={
        200: openapi.Response(
            description="Success - PNG spectrogram image ready for download",
            headers={
                'Content-Type': openapi.Schema(type=openapi.TYPE_STRING, example='image/png'),
                'Content-Disposition': openapi.Schema(type=openapi.TYPE_STRING, example='attachment; filename="audio_spectrogram.png"')
            }
        ),
        400: openapi.Response(
            description="Bad Request - Missing or invalid audio file",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="No audio file provided"
                    )
                }
            )
        ),
        500: openapi.Response(
            description="Internal Server Error - Spectrogram generation failed",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Spectrogram generation failed"
                    )
                }
            )
        )
    },
    consumes=['multipart/form-data'],
    tags=['Audio Visualization']
)
@api_view(['POST'])
def generate_spectrogram(request):
    try:
        if 'audio_file' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio_file']
        
        if not audio_file.name:
            return JsonResponse({'error': 'Invalid file'}, status=400)
        
        spectrogram_data = SpectrogramGenerator.generate_spectrogram_from_file(audio_file, audio_file.name)
        
        filename = audio_file.name.rsplit(".", 1)[0] + "_spectrogram.png"
        response = HttpResponse(spectrogram_data, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(spectrogram_data)
        response['Cache-Control'] = 'no-cache'
        return response
        
    except Exception as e:
        return JsonResponse({'error': 'Spectrogram generation failed'}, status=500)


@swagger_auto_schema(
    method='post',
    operation_summary="Transcribe Audio to Text",
    operation_description="""
    Convert speech in audio files to text using Google Speech Recognition API.
    
    **Features:**
    - High-accuracy speech recognition using Google's API
    - Support for 35+ languages and dialects
    - Automatic audio format conversion to WAV for processing
    - Real-time transcription with error handling
    - Language detection and customization options
    
    **Supported Input Formats:**
    - All formats: MP3, MP4, WAV, FLAC, AAC, OGG, WMA, M4A, AIFF
    
    **Language Support:**
    - English (US/UK), Spanish, French, German, Italian
    - Portuguese, Russian, Japanese, Korean, Chinese
    - Arabic, Hindi, Thai, Vietnamese, Dutch, Swedish
    - And many more (35+ languages total)
    
    **Technical Details:**
    - Uses Google Speech Recognition API
    - Automatic audio preprocessing and format conversion
    - Handles various audio qualities and lengths
    - Error handling for unclear speech or API issues
    
    **Use Cases:**
    - Voice note transcription
    - Meeting and interview transcription
    - Accessibility applications
    - Content creation and documentation
    - Language learning and analysis
    - Automated subtitling and captioning
    """,
    manual_parameters=[
        openapi.Parameter(
            'audio_file',
            openapi.IN_FORM,
            description="Audio file containing speech to transcribe. Accepts all supported formats: mp3, mp4, wav, flac, aac, ogg, wma, m4a, aiff",
            type=openapi.TYPE_FILE,
            required=True
        ),
        openapi.Parameter(
            'language',
            openapi.IN_FORM,
            description="Language code for speech recognition (e.g., 'en-US', 'es-ES', 'fr-FR'). Defaults to 'en-US'",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(
            description="Success - Transcribed text returned",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'transcription': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Hello, this is a sample transcription of the audio file."
                    ),
                    'language': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="en-US"
                    ),
                    'filename': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="audio_sample.mp3"
                    )
                }
            ),
            examples={
                "application/json": {
                    "transcription": "Hello, this is a sample transcription of the audio file.",
                    "language": "en-US",
                    "filename": "audio_sample.mp3"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request - Missing file or transcription error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Could not understand audio - speech may be unclear or not present"
                    )
                }
            )
        ),
        500: openapi.Response(
            description="Internal Server Error - Transcription service failed",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Transcription failed"
                    )
                }
            )
        )
    },
    consumes=['multipart/form-data'],
    tags=['Audio Processing']
)
@api_view(['POST'])
def transcribe_audio(request):
    try:
        if 'audio_file' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio_file']
        
        if not audio_file.name:
            return JsonResponse({'error': 'Invalid file'}, status=400)
        
        language = request.POST.get('language', 'en-US')
        
        transcription = AudioTranscriber.transcribe_audio_from_file(audio_file, audio_file.name, language)
        
        return JsonResponse({
            'transcription': transcription,
            'language': language,
            'filename': audio_file.name
        })
        
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Transcription failed'}, status=500)


@swagger_auto_schema(
    method='get',
    operation_summary="Get Supported Languages for Transcription",
    operation_description="""
    Retrieve a comprehensive list of all languages supported by the speech recognition API.
    
    **Use this endpoint to:**
    - Check language support before transcription
    - Display available languages in your application
    - Validate language codes programmatically
    - Build language selection interfaces
    
    **Returns:** Dictionary mapping language codes to human-readable names
    
    **Language Coverage:**
    - Major world languages (English, Spanish, French, German, etc.)
    - Asian languages (Chinese, Japanese, Korean, Hindi, etc.)
    - European languages (Italian, Portuguese, Russian, etc.)
    - Regional dialects and variants
    """,
    responses={
        200: openapi.Response(
            description="Successfully retrieved supported languages",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'supported_languages': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        example={
                            "en-US": "English (US)",
                            "en-GB": "English (UK)",
                            "es-ES": "Spanish (Spain)",
                            "fr-FR": "French (France)",
                            "de-DE": "German (Germany)"
                        }
                    )
                }
            ),
            examples={
                "application/json": {
                    "supported_languages": {
                        "en-US": "English (US)",
                        "en-GB": "English (UK)",
                        "es-ES": "Spanish (Spain)",
                        "es-MX": "Spanish (Mexico)",
                        "fr-FR": "French (France)",
                        "de-DE": "German (Germany)",
                        "it-IT": "Italian (Italy)",
                        "pt-BR": "Portuguese (Brazil)",
                        "ru-RU": "Russian (Russia)",
                        "ja-JP": "Japanese (Japan)",
                        "ko-KR": "Korean (South Korea)",
                        "zh-CN": "Chinese (Simplified)"
                    }
                }
            }
        )
    },
    tags=['Information']
)
@api_view(['GET'])
def supported_languages(request):
    languages = AudioTranscriber.get_supported_languages()
    return JsonResponse({'supported_languages': languages})