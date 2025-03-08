"""
Django settings for genomic_platform project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env=environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / 'genomic_patform' / '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Utilisez une clé secrète sécurisée en production et ne la partagez jamais.
SECRET_KEY = env('SECRET_KEY', default='fallback_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)  # En production, DEBUG doit toujours être False.

# Liste des hôtes autorisés pour le déploiement en production.
# Ajoutez ici votre domaine réel ou l'adresse IP du serveur.
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

print(SECRET_KEY)
print(DEBUG)
print(type(DEBUG))
print(ALLOWED_HOSTS)


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'genomic_data',  # Assurez-vous que cette application existe dans votre projet.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise pour la gestion des fichiers statiques.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'genomic_platform.urls'  # Fichier de configuration des URLs.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Répertoire des templates.
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

WSGI_APPLICATION = 'genomic_platform.wsgi.application'  # Configuration WSGI.

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Utilisation de SQLite3.
        'NAME': BASE_DIR / 'db.sqlite3',  # Chemin vers la base de données SQLite.
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'fr-fr'  # Langue française.
TIME_ZONE = 'UTC'  # Fuseau horaire UTC.
USE_I18N = True  # Activation de l'internationalisation.
USE_TZ = True  # Utilisation des fuseaux horaires.

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'  # URL de base pour les fichiers statiques.

# Répertoires supplémentaires pour les fichiers statiques.
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Répertoire des fichiers statiques supplémentaires.
]

# Répertoire où les fichiers statiques collectés seront stockés.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuration de WhiteNoise pour la gestion des fichiers statiques en production.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration des médias (fichiers uploadés par les utilisateurs).
MEDIA_URL = '/media/'  # URL de base pour les fichiers média.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Répertoire des fichiers média.

# Redirections pour l'authentification.
LOGIN_URL = 'login'  # URL de connexion.
LOGIN_REDIRECT_URL = 'home'  # Redirection après connexion.
LOGOUT_REDIRECT_URL = 'login'  # Redirection après déconnexion.

# Configuration de l'envoi d'emails.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Serveur SMTP de Gmail.
EMAIL_PORT = 587  # Port SMTP pour TLS.
EMAIL_USE_TLS = True  # Utilisation de TLS pour la sécurité.
EMAIL_HOST_USER = 'alioubakolo224@gmail.com'  # Votre adresse email Gmail.
EMAIL_HOST_PASSWORD = '@lioubakolo224'  # Votre mot de passe Gmail.
DEFAULT_FROM_EMAIL = 'alioubakolo224@gmail.com'  # Adresse email par défaut.

# URL du site (utilisé pour les liens absolus).
SITE_URL = 'http://127.0.0.1:8000'  # À remplacer par votre domaine réel en production.