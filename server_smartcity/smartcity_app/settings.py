from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']


# INSTALLED APPS
INSTALLED_APPS = [
    # DJANGO DEFAULT APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD PARTY APPS
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'django_scalar',

    # APP KAMU
    'main_app',
    'about',
    'contacts',
    'usermanagement_24782050',
    'dashboard_24782050',
]


# MIDDLEWARE
MIDDLEWARE = [
    # CORS MIDDLEWARE HARUS DI ATAS COMMON MIDDLEWARE
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ROOT URL
ROOT_URLCONF = 'smartcity_app.urls'


# TEMPLATE SETTINGS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # GLOBAL TEMPLATE
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI
WSGI_APPLICATION = 'smartcity_app.wsgi.application'


# DATABASE POSTGRESQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartcity_db',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# CUSTOM USER MODEL
AUTH_USER_MODEL = 'usermanagement_24782050.CustomUser'


# AUTH REDIRECT
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# STATIC FILES
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'


# DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DJANGO REST FRAMEWORK + JWT AUTHENTICATION + OPENAPI SCHEMA
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


# OPENAPI DOCUMENTATION SETTINGS
SPECTACULAR_SETTINGS = {
    'TITLE': 'Smart City Portal API',
    'DESCRIPTION': 'Dokumentasi REST API resmi untuk Portal Pelaporan Laporan Warga',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


# CORS SETTINGS
# Mengizinkan frontend SPA dari domain berbeda seperti GitHub Pages mengakses backend Django
CORS_ALLOW_ALL_ORIGINS = True