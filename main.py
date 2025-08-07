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
from api_endpoints import convert_audio, supported_formats, health_check, generate_waveform, generate_spectrogram



urlpatterns = [
    path('convert/', convert_audio, name='convert_audio'),
    path('formats/', supported_formats, name='supported_formats'),
    path('health/', health_check, name='health_check'),
    path('waveform/', generate_waveform, name='generate_waveform'),
    path('spectrogram/', generate_spectrogram, name='generate_spectrogram'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
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