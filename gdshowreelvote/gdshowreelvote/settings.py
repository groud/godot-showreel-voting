"""
Django settings for gdshowreelvote project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from get_docker_secret import get_docker_secret

def as_yes_no(s : str):
    s = s.lower()
    if s in ['true', 't', 'y', 'yes']:
        return True
    if s in ['false', 'f', 'n', 'no']:
        return False
    return None

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('GDSHOWREEL_DJANGO_SECRET_KEY', get_docker_secret('gdshowreel_django_secret', default=None))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = as_yes_no(os.environ.get('GDSHOWREEL_DJANGO_DEBUG', 'false'))

# Domain name
ALLOWED_HOSTS = os.environ.get('GDSHOWREEL_DJANGO_ALLOWED_HOSTS','').split(',')

# Application definition

INSTALLED_APPS = [
    'vote.apps.VoteConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mozilla_django_oidc',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'mozilla_django_oidc.middleware.SessionRefresh',
]

ROOT_URLCONF = 'gdshowreelvote.urls'

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

                'vote.context_processors.common',
            ],
        },
    },
]

WSGI_APPLICATION = 'gdshowreelvote.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('GDSHOWREEL_DATABASE_NAME', 'gdshowreel'),
        'USER': os.environ.get('GDSHOWREEL_DATABASE_USER', 'mysql'),
        'PASSWORD': os.environ.get('GDSHOWREEL_DATABASE_PASSWORD', get_docker_secret('gdshowreel_django_db_password')),
        'HOST': os.environ.get('GDSHOWREEL_DATABASE_HOST', 'database'),
        'PORT': os.environ.get('GDSHOWREEL_DATABASE_PORT', ''),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

SERVE_STATICS = as_yes_no(os.environ.get('GDSHOWREEL_SERVE_STATICS', "yes"))
STATIC_ROOT = os.environ.get('GDSHOWREEL_STATIC_ROOT', "/var/www/showreel.godotengine.org/static/")
STATIC_URL = '/static/'

### Authentication ###
AUTHENTICATION_BACKENDS = [
    'vote.auth.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'vote.User'

# OICD client connection
OIDC_RP_CLIENT_ID = os.environ.get('GDSHOWREEL_OIDC_RP_CLIENT_ID', get_docker_secret('gdshowreel_oidc_rp_client_id'))
OIDC_RP_CLIENT_SECRET = os.environ.get('GDSHOWREEL_OIDC_RP_CLIENT_SECRET', get_docker_secret('gdshowreel_oidc_rp_client_secret'))

# Signing algorihtm
OIDC_RP_SIGN_ALGO = 'RS256'

# Keycloak configuration
KEYCLOAK_REALM = os.environ.get('GDSHOWREEL_KEYCLOAK_REALM', "master")
KEYCLOAK_HOSTNAME = os.environ.get('GDSHOWREEL_KEYCLOAK_HOSTNAME', "keycloak:8080")

# Keycloak roles in authentication claims
KEYCLOAK_ROLES_PATH_IN_CLAIMS = os.environ.get('GDSHOWREEL_KEYCLOAK_ROLES_PATH_IN_CLAIMS', "realm_access,roles").split(',')
KEYCLOAK_STAFF_ROLE = os.environ.get('GDSHOWREEL_KEYCLOAK_STAFF_ROLE', "staff")
KEYCLOAK_SUPERUSER_ROLE = os.environ.get('GDSHOWREEL_KEYCLOAK_SUPERUSER_ROLE', "admin")

# Keycloak OICD endpoints. You can get those at this endpoint http://{keycloakhost}:{port}/auth/realms/{realm}/.well-known/openid-configuration
OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ.get('GDSHOWREEL_OIDC_OP_AUTHORIZATION_ENDPOINT', f"http://{KEYCLOAK_HOSTNAME}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth") # URL of the OIDC OP authorization endpoint
OIDC_OP_TOKEN_ENDPOINT = os.environ.get('GDSHOWREEL_OIDC_OP_TOKEN_ENDPOINT', f"http://{KEYCLOAK_HOSTNAME}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token") # URL of the OIDC OP token endpoint
OIDC_OP_USER_ENDPOINT = os.environ.get('GDSHOWREEL_OIDC_OP_USER_ENDPOINT', f"http://{KEYCLOAK_HOSTNAME}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo") # URL of the OIDC OP userinfo endpoint
OIDC_OP_JWKS_ENDPOINT = os.environ.get('GDSHOWREEL_OIDC_OP_JWKS_ENDPOINT', f"http://{KEYCLOAK_HOSTNAME}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs")
OIDC_OP_LOGOUT_ENDPOINT = os.environ.get('GDSHOWREEL_OIDC_OP_LOGOUT_ENDPOINT', f"http://{KEYCLOAK_HOSTNAME}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout")

# URLS
LOGIN_REDIRECT_URL = '/submissions'
LOGOUT_REDIRECT_URL = '/login'

LOGIN_URL = 'login'

# Automatic Keycloak logout
OIDC_OP_LOGOUT_URL_METHOD = "vote.auth.logout"

### Security ###
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

### Custom settings ###
VOTE_MAX_SUBMISSIONS_PER_SHOWREEL = os.environ.get('GDSHOWREEL_VOTE_MAX_SUBMISSIONS_PER_SHOWREEL', 3)
VOTE_ONLY_STAFF_CAN_VOTE = as_yes_no(os.environ.get('GDSHOWREEL_VOTE_ONLY_STAFF_CAN_VOTE', "yes"))