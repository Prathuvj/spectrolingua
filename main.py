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


if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='your-secret-key-here',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.staticfiles',
            'rest_framework',
            'drf_yasg',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
        STATIC_URL='/static/',
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


from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


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
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'audio_file': openapi.Schema(
                type=openapi.TYPE_FILE,
                description="Audio file to convert (supports mp3, mp4, flac, aac, ogg, wma, m4a, aiff)"
            )
        },
        required=['audio_file']
    ),
    responses={
        200: openapi.Response(
            description="WAV file download or message if already WAV"
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        500: openapi.Response(
            description="Conversion failed",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    consumes=['multipart/form-data']
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
@api_view(['GET'])
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
@api_view(['GET'])
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