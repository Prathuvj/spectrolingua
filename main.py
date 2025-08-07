import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.urls import path, re_path


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


from swagger_config import schema_view
from api_endpoints import convert_audio, supported_formats, health_check, generate_waveform, generate_spectrogram, transcribe_audio, supported_languages



urlpatterns = [
    path('convert/', convert_audio, name='convert_audio'),
    path('formats/', supported_formats, name='supported_formats'),
    path('health/', health_check, name='health_check'),
    path('waveform/', generate_waveform, name='generate_waveform'),
    path('spectrogram/', generate_spectrogram, name='generate_spectrogram'),
    path('transcribe/', transcribe_audio, name='transcribe_audio'),
    path('languages/', supported_languages, name='supported_languages'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

application = get_wsgi_application()


if __name__ == '__main__':
    import sys
    import subprocess
    import time
    import os
    import signal
    from django.core.management import execute_from_command_line
    
    # Check if we're being called to run Django directly
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        execute_from_command_line(sys.argv)
    else:
        print("🎵 Audio Processing Studio - Starting Backend & Frontend")
        print("=" * 60)
        
        # Start Django API server
        print("🚀 Starting Django API server on http://127.0.0.1:8000")
        django_process = subprocess.Popen([
            sys.executable, 'main.py', 'runserver', '8000'
        ])
        
        # Wait a moment for Django to start
        time.sleep(3)
        
        # Start Streamlit frontend
        print("🎨 Starting Streamlit frontend on http://localhost:8501")
        streamlit_process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
            '--server.port', '8501',
            '--server.headless', 'false',
            '--browser.gatherUsageStats', 'false'
        ])
        
        print("\n✅ Both services are starting...")
        print("📱 Frontend: http://localhost:8501")
        print("� API Docsn: http://127.0.0.1:8000/docs/")
        print("\n💡 Press Ctrl+C to stop both services")
        
        try:
            # Wait for both processes
            django_process.wait()
            streamlit_process.wait()
        except KeyboardInterrupt:
            print("\n👋 Shutting down Audio Processing Studio...")
            
            # Terminate both processes
            django_process.terminate()
            streamlit_process.terminate()
            
            # Wait for clean shutdown
            try:
                django_process.wait(timeout=5)
                streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                django_process.kill()
                streamlit_process.kill()
            
            print("✅ Services stopped successfully")
            sys.exit(0)