"""
Django settings for ContriHub project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import django_heroku
import os
from unipath import Path
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', "faf541d1cdd7da1d485ccd6c27de8a9cc8a29434e3d1e307e250e2ee25ff4b23")
# GITHUB_SECRET_KEY = config('GITHUB_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# ENV is an environment var which is set to Dev in local and Prod in production

DEBUG=True
ALLOWED_HOSTS = ['*']

# ENV=os.environ.get("ENV","")
# if ENV=='Dev': 
#     DEBUG = True
#     ALLOWED_HOSTS = ['*']
# else: 
#     DEBUG = False
#     ALLOWED_HOSTS = ['.contrihubs.herokuapp.com','www.contrihubs.herokuapp.com']


ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


ADMINS = (   
        ('Deepak Bharti',os.environ.get('admin1_email','')),
        ('Abhey Rana',os.environ.get('admin2_email','')),
    )

# Application definition

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER= os.environ.get('EMAIL_HOST_USER','')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD','')
EMAIL_PORT = 587

'''
If using gmail, you will need to
unlock Captcha to enable Django 
to  send for you:
https://accounts.google.com/displayunlockcaptcha
'''



INSTALLED_APPS = [
    'Users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Projects',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ContriHub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates'),
                BASE_DIR.child('templates','templates'),
                ],
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

WSGI_APPLICATION = 'ContriHub.wsgi.application'


# Database documentation
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


# print(DB_PASS)
if 'DATABASE_URL' in os.environ: #this is for heroku
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL',""))}
else: 
    #this is for local you need not to make any changes here, 
    # it'll work unless you are sure about how to setup postgres/mysql etc    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
    #An example how you can setup postgres sql in local, create a postgres db and provide relevant details in this format
    # DB_PASS = os.environ.get('CONTRIHUB_PASS', "")
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'contrihub_db',
    #         'USER': 'contrihub_user',
    #         'PASSWORD': DB_PASS,
    #         'HOST': 'localhost',
    #         'PORT': '',
    #     }
    # }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


STATIC_ROOT = BASE_DIR.child('ContriHub','static_root')
# static_root is the server outside our project wher e static files are sent to store

STATICFILES_DIRS = (
    BASE_DIR.child('static'),
    #'/var/www/static/',
    )

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('ContriHub','media_root')

#Crispy forms tags settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'


SITE_ID = 1
# added on 15_jan
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
 
ALLOWED_SIGNUP_DOMAINS = ['*']
 
FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0o644

#added to host on heroku
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

import netifaces

# Find out what the IP addresses are at run time
# This is necessary because otherwise Gunicorn will reject the connections
def ip_addresses():
    ip_list = []
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        for x in (netifaces.AF_INET, netifaces.AF_INET6):
            if x in addrs:
                ip_list.append(addrs[x][0]['addr'])
    return ip_list

# Discover our IP address
ALLOWED_HOSTS += ip_addresses()

django_heroku.settings(locals())
