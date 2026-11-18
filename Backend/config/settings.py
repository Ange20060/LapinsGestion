"""
Configuration principale de l'application LapinGestion.
Django 5.2 --API REST Framework 3.15 --PostgreSQL 15.3 --Python 3.12.2
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

#Chargement des variables d'environnement depuis le fichier .env
# Implémentation légère évitant une dépendance externe manquante.
def load_env_file(path):
    if not path.exists():
        return

    with path.open('r', encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            if key and key not in os.environ:
                os.environ[key] = value


load_env_file(BASE_DIR / '.env')

#securité
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-key-change-before-production')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'True'

ALLOWED_HOSTS = [
  host.strip() for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if host.strip()
]

#Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',  # Application de gestion des utilisateurs de LapinGestion
    #Application externes
    'rest_framework',  # Django REST Framework pour les API
    'corsheaders',  # Gestion des en-têtes CORS pour les requêtes cross-origin
    'rest_framework.authtoken',  # Gestion des tokens d'authentification pour les API
]
#Utilisateurs personalisés
AUTH_USER_MODEL = 'accounts.User'  # Utilisation du modèle User personnalisé défini dans

#Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Middleware pour gérer les en-têtes CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#URLs
ROOT_URLCONF = 'config.urls'

#Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
  ]
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

#Base de données
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.postgresql').lower()
if DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'LapinGestion_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'CONN_MAX_AGE': 600,  # Durée de vie maximale de la connexion en secondes
            'OPTIONS': {
                'connect_timeout': 10,  # Délai d'attente pour la connexion en secondes
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
      #Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

#Fichiers statiques
STATIC_URL = '/static/'
STATICFILES_ROOT = BASE_DIR / 'staticfiles'

#Fichiers médias
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#API REST
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

#CORS
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',') if origin.strip()
]

#Securité des cookies de session
SESSION_COOKIE_AGE = 1209600  # 2 semaines en secondes
SESSION_COOKIE_HTTPONLY = True  # Empêche l'accès au cookie via JavaScript
CSRF_COOKIE_HTTPONLY = True  # Empêche l'accès au cookie CSRF via JavaScript
SESSION_COOKIE_SECURE = not DEBUG  # Utiliser des cookies sécurisés en production

#Identifiants
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Type de champ par défaut pour les clés primaires
