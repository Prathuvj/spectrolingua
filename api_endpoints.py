from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from format_conversion import AudioConverter
from waveform import WaveformGenerator
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