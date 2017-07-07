#coding=UTF-8
"""
Django settings for QinggangManageSys project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os
from . import choose_settings
from .import views


ROW_NUM=10000
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = choose_settings.DEBUG

TEMPLATE_DEBUG = DEBUG

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR,'data_import/static')

# # upload folder
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR,'data_import/media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@o$#tz@^1q8-(nk*8d(-r-pqdbci@*x2(hemnwnvp1&kw$@ggp'

TEMPLATE_DIRS = choose_settings.TEMPLATE_DIRS

# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = choose_settings.ALLOWED_HOSTS

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('maksim', 'ccxysfh1993@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = choose_settings.DATABASES


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',#the core of the authentication framework
    'django.contrib.contenttypes',#allows permissions to be associated with models you create.
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'data_import',
    'django_crontab',
]



MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',#manages sessions across requests.
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',# associates users with requests using sessions.
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',#logs users out of their other sessions after a password change.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'QinggangManageSys.middleware.ProcessExceptionMiddleware'
]

ROOT_URLCONF = 'QinggangManageSys.urls'

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

WSGI_APPLICATION = 'QinggangManageSys.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_CN'

#LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = choose_settings.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = choose_settings.MEDIA_URL

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = choose_settings.STATIC_ROOT
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = choose_settings.STATIC_URL
# '''
# 配置logging模块
# '''
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard':{
#             'format':'%(asctime)s[(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:(funcName)s]-%(message)s'
#             },
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         # 'file': {
#         #     'level': 'DEBUG',
#         #     'class': 'logging.FileHandler',
#         #     'filename': MEDIA_ROOT + '/logs/debug.log',
#         # },
#         # 'mail_admins': {
#         #     'level': 'ERROR',
#         #     'class': 'django.utils.log.AdminEmailHandler',
#         #     'include_html': True,
#         # },
#         # 'default': {
#         #     'level':'INFO',
#         #     'class':'logging.handlers.RotatingFileHandler',
#         #     'filename': MEDIA_ROOT + '/logs/all.log',                #日志输出文件
#         #     'maxBytes': 1024*1024*5,                  #文件大小
#         #     'backupCount': 5,                         #备份份数
#         #     'formatter':'simple',                   #使用哪种formatters日志格式
#         # },
#         # 'error': {
#         #     'level':'ERROR',
#         #     'class':'logging.handlers.RotatingFileHandler',
#         #     'filename': MEDIA_ROOT + '/logs/error.log',
#         #     'maxBytes':1024*1024*5,
#         #     'backupCount': 5,
#         #     'formatter':'standard',
#         # },
#         'console':{
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#         # 'request_handler': {
#         #     'level':'DEBUG',
#         #     'class':'logging.handlers.RotatingFileHandler',
#         #     'filename': MEDIA_ROOT + '/logs/script.log',
#         #     'maxBytes': 1024*1024*5,
#         #     'backupCount': 5,
#         #     'formatter':'standard',
#         # },
#         # 'scprits_handler': {
#         #     'level':'DEBUG',
#         #     'class':'logging.handlers.RotatingFileHandler',
#         #     'filename':MEDIA_ROOT + '/logs/script.log',
#         #     'maxBytes': 1024*1024*5,
#         #     'backupCount': 5,
#         #     'formatter':'standard',
#         # }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#         # 'django.request': {
#         #     'handlers': ['request_handler'],
#         #     'level': 'DEBUG',
#         #     'propagate': False,
#         #     },
#         # 'scripts': {
#         #     'handlers': ['scprits_handler'],
#         #     'level': 'INFO',
#         #     'propagate': False
#         # },
#         # 'blog.views': {
#         #     'handlers': ['default', 'error'],
#         #     'level': 'DEBUG',
#         #     'propagate': True
#         # },
#     },
# }
'''
custom settings
'''
# 系统基本界面主目录
MAIN_OUTFIT_BASE = 'data_import/main/'
#
# CRONJOBS = [
#     ('47 11 * * *', 'django.core.management.call_command', ['aizhan_5domain_visits']),
# ]
CRONJOBS = [
    # 
    ('*/1 * * * *', 'QinggangManageSys.views.paralle_test1'),

]
