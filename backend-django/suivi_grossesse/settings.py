"""
Django settings for suivi_grossesse project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# ============================================================
# SECURITY
# ============================================================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@!v)-c^d#jsb#4ab27lbvyw-giwhwq7gjl15&zi*z2@naxz1vv')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# ============================================================
# INSTALLED APPS - ⚠️ IMPORTANT : drf_spectacular DOIT être présent
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # ⭐ Third-party apps
    'rest_framework',           # Django REST Framework
    'corsheaders',              # CORS
    'drf_spectacular',          # ⭐ SWAGGER UI - OBLIGATOIRE
    
    # ⭐ Custom apps
    'api',
]

# ============================================================
# MIDDLEWARES
# ============================================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'suivi_grossesse.urls'

TEMPLATES = [
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
]

WSGI_APPLICATION = 'suivi_grossesse.wsgi.application'

# ============================================================
# DATABASE - MySQL
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'suivi_grossesse'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}



# ============================================================
#ALLOWED_HOSTS = [
   # "127.0.0.1",
   # "localhost",
    #".ngrok-free.dev",
#]


#CSRF_TRUSTED_ORIGINS = [
    #"https://finished-creature-cardigan.ngrok-free.dev",
#]
# REST FRAMEWORK - ⚠️ IMPORTANT : DEFAULT_SCHEMA_CLASS
# ============================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # ⭐ OBLIGATOIRE pour Swagger
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'UNAUTHENTICATED_USER': None,
}

# ============================================================
# CORS
# ============================================================
CORS_ALLOWED_ORIGINS = [
    os.getenv('CORS_ORIGIN', 'http://localhost:5173'),
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

CORS_ALLOW_CREDENTIALS = True

# ============================================================
# ⭐ SPECTACULAR (SWAGGER) SETTINGS - OBLIGATOIRE
# ============================================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'API SuiviGrossesse',
    'DESCRIPTION': """
## API de suivi médical de grossesse

Cette API permet le suivi médical des grossesses.

###  Authentification
- **JWT (JSON Web Token)** 
- Obtenez un token via `/api/v1/auth/login`
- Utilisez `Authorization: Bearer <token>`

###  Rôles
| Rôle | Description |
|------|-------------|
| **PATIENTE** | Femme enceinte |
| **SOIGNANT** | Sage-femme, gynécologue |
| **ADMIN** | Administrateur |

###  Fonctionnalités
- Patiente : Grossesses, rendez-vous, examens
- Soignant : Consultations, examens, alertes
- Admin : Gestion utilisateurs, supervision
""",
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'TAGS': [
        {'name': 'Authentification', 'description': 'Inscription, connexion, déconnexion'},
        {'name': 'Patiente', 'description': 'Gestion des grossesses, rendez-vous, examens'},
        {'name': 'Soignant', 'description': 'Gestion des patientes, consultations'},
        {'name': 'Administrateur', 'description': 'Supervision et gestion'},
    ],
}

# ============================================================
# JWT SETTINGS
# ============================================================
JWT_SECRET = os.getenv('JWT_SECRET', 'suivi_grossesse_jwt_secret')
JWT_EXPIRES_DAYS = int(os.getenv('JWT_EXPIRES_DAYS', '7'))

# ============================================================
# STATIC FILES
# ============================================================
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

