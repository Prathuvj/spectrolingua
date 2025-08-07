import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import path, re_path
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from format_conversion import AudioConverter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='your-secret-key-here',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'rest_framework',
            'drf_yasg',
        ],
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
        ],
        USE_TZ=True,
        REST_FRAMEWORK={
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.AllowAny',
            ],
        },
    )
    django.setup()


schema_view = get_schema_view(
    openapi.Info(
        title="Audio Converter API",
        default_version='v1',
        description="API for converting audio files to WAV format",
        contact=openapi.Contact(email="contact@audioconverter.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


@swagger_auto_schema(
    method='post',
    operation_description="Convert audio file to WAV format",
    manual_parameters=[
        openapi.Parameter(
            'audio_file',
            openapi.IN_FORM,
            description="Audio file to convert (supports mp3, mp4, flac, aac, ogg, wma, m4a, aiff)",
            type=openapi.TYPE_FILE,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="WAV file download",
            schema=openapi.Schema(type=openapi.TYPE_FILE)
        ),
        400: openapi.Response(
            description="Bad request",
            examples={
                "application/json": {
                    "error": "No audio file provided"
                }
            }
        ),
        500: openapi.Response(
            description="Conversion failed",
            examples={
                "application/json": {
                    "error": "Conversion failed"
                }
            }
        )
    },
    consumes=['multipart/form-data'],
    produces=['audio/wav', 'application/json']
)
@csrf_exempt
@require_http_methods(["POST"])
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
    operation_description="Get list of supported audio formats",
    responses={
        200: openapi.Response(
            description="List of supported formats",
            examples={
                "application/json": {
                    "supported_formats": ["mp3", "mp4", "wav", "flac", "aac", "ogg", "wma", "m4a", "aiff"]
                }
            }
        )
    }
)
@require_http_methods(["GET"])
def supported_formats(request):
    formats = AudioConverter.get_supported_formats()
    return JsonResponse({'supported_formats': formats})


@swagger_auto_schema(
    method='get',
    operation_description="Health check endpoint",
    responses={
        200: openapi.Response(
            description="Service is healthy",
            examples={
                "application/json": {
                    "status": "healthy"
                }
            }
        )
    }
)
@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({'status': 'healthy'})


urlpatterns = [
    path('convert/', convert_audio, name='convert_audio'),
    path('formats/', supported_formats, name='supported_formats'),
    path('health/', health_check, name='health_check'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

application = get_wsgi_application()


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    import sys
    
    if len(sys.argv) == 1:
        sys.argv.append('runserver')
        sys.argv.append('8000')
    
    execute_from_command_line(sys.argv)