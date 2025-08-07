import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import path
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from format_conversion import AudioConverter


if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='your-secret-key-here',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
        ],
        USE_TZ=True,
    )
    django.setup()


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
        
        response = HttpResponse(wav_data, content_type='audio/wav')
        response['Content-Disposition'] = f'attachment; filename="{audio_file.name.rsplit(".", 1)[0]}.wav"'
        return response
        
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Conversion failed'}, status=500)


@require_http_methods(["GET"])
def supported_formats(request):
    formats = AudioConverter.get_supported_formats()
    return JsonResponse({'supported_formats': formats})


@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({'status': 'healthy'})


urlpatterns = [
    path('convert/', convert_audio, name='convert_audio'),
    path('formats/', supported_formats, name='supported_formats'),
    path('health/', health_check, name='health_check'),
]

application = get_wsgi_application()


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    import sys
    
    if len(sys.argv) == 1:
        sys.argv.append('runserver')
        sys.argv.append('8000')
    
    execute_from_command_line(sys.argv)