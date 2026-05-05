from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔥 SECURITY
SECRET_KEY = 'django-secret-key'
DEBUG = True
ALLOWED_HOSTS = []


# 🔥 INSTALLED APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🔥 APP KAMU
    'main_app',
    'about',
    'contacts',

    # 🔥 USER MANAGEMENT
    'usermanagement_24782050',
    'dashboard_24782050',
]


# 🔥 MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 🔥 ROOT URL
ROOT_URLCONF = 'npm24782050_iet_2026.urls'


# 🔥 TEMPLATE SETTINGS (PENTING BANGET)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 🔥 GLOBAL TEMPLATE (WAJIB ADA FOLDER templates/)
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


# 🔥 WSGI
WSGI_APPLICATION = 'npm24782050_iet_2026.wsgi.application'


# 🔥 DATABASE (POSTGRESQL)
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


# 🔥 CUSTOM USER MODEL
AUTH_USER_MODEL = 'usermanagement_24782050.CustomUser'


# 🔥 AUTH REDIRECT
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# 🔥 STATIC FILES
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# 🔥 DEFAULT AUTO FIELD (BIAR WARNING HILANG)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'