"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from .mconfig import config
import time


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']
# SECRET_KEY = '{{secret_key}}'  # при использовании проекта как шаблона

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # D1.3 add flatpages
    'django.contrib.sites',
    'django.contrib.flatpages',

    # D1.4 add flatpages
    'fpages',

    # D2.4
    'simpleapp',
    'accounts',
    'django_filters',

    # D5
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',

    # D6.5. Выполнение задач по расписанию
    'django_apscheduler',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # D1.3 add flatpages
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # D8.3 кэширование сайта целиком
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # D1.3 add flatpages
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # D6.3 # `allauth` обязательно нужен этот процессор
                'django.template.context_processors.request',
            ],
        },
    },
]

# D5
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend', ]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # D12
    'my_local': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': config['DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'UTC'  # UTC+8 - Hongkong

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# LOGIN_URL = ''  # страница входа
LOGIN_REDIRECT_URL = "/portal"  # LOGOUT_REDIRECT_URL = "/accounts/login"
# LOGOUT_REDIRECT_URL = '/accounts/login'
LOGOUT_REDIRECT_URL = "/portal"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# D1.5 bootstrap
STATICFILES_DIRS = [BASE_DIR / "static"]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = config['ACCOUNT_EMAIL_VERIFICATION']  # проверяет наличие реальных почтовых ящиков!
# print('ACCOUNT_EMAIL_VERIFICATION = ', ACCOUNT_EMAIL_VERIFICATION)  # (пароль для сайта любой!)
# ACCOUNT_EMAIL_VERIFICATION = 'none'  # не проверяет наличие реальных почтовых ящиков
# Кроме этого значения, переменная может принимать и два других:
# mandatory — не пускать пользователя на сайт до момента подтверждения почты;
# optional — сообщение о подтверждении будет отправлено, но пользователь может залогиниться без подтверждения почты.
ACCOUNT_CONFIRM_EMAIL_ON_GET = True     # позволит избежать дополнительного входа и активирует аккаунт сразу,
#                                       # как только мы перейдём по ссылке.
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3  # Количество неудачных попыток входа в систему. 'None' - отключить ограничение.
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400  # секунд запрета на вход посте N неудачных попыток.
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS хранит количество дней, когда доступна ссылка на подтверждение регистрации.
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

# D6.2
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # значение по умолчанию (реальная отправка писем)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # вывод отправляемого в консоль (Terminal
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = config['EMAIL_USE_TLS']
EMAIL_USE_SSL = config['EMAIL_USE_SSL']
EMAIL_SUBJECT_PREFIX = 'News portal: '  # EMAIL_SUBJECT_PREFIX = '[Django]'  # Префикс темы письма (managers & admins).
DEFAULT_FROM_EMAIL = config['DEFAULT_FROM_EMAIL']  # Будет отображаться в поле «отправитель» у получателя письма.
SERVER_EMAIL = config['SERVER_EMAIL']
MANAGERS = (config['MANAGERS'],)  # Не те менеджеры, что созданы под Админкой.
ADMINS = (config['ADMINS'],)

# D7.3
CELERY_BROKER_URL = config['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = CELERY_BROKER_URL  # ???
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# D8.3 кэширование
CACHES = {
    'default': {
        'TIMEOUT': 0,  # время кэширования, с. Стандартное время - 5 минут (300 секунд).
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

# D13.4 Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'format_1': {'format': '      con_g> {asctime}  {levelname}\t \t "...{message}..."', 'style': '{'},
        'format_2': {'format': 'con_g, mail> {asctime}  {levelname}\t \t />{pathname} "...{message}..."', 'style': '{'},
        'format_3': {'format': 'g_log,s_log> {asctime}  {levelname}\t \t module={module}.py  "...{message}..."', 'style': '{'},
        'format_4': {'format': 'con_w,e_log> {asctime}  {levelname}\t \t />{pathname}  "...{message}..."  stack=({exc_info})', 'style': '{'},
        # 'full_frm': {'format': 'Test>> {asctime}  {levelname}\t \t  module={module}.py  process={process:d} thread={thread:d}  />{pathname}  "...{message}..."  stack=({exc_info})', 'style': '{'},
        # 'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s', 'datetime': '%Y.%m.%d %H:%M:%S'
    },
    'filters': {
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue', },
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse', },
    },
    'handlers': {
        # будет дублировать сообщения WARNING и ERROR? И уровень DEBUG при выводе в консоль явно "излишен", но, пункт 1:
        # "...В консоль должны выводиться все сообщения уровня DEBUG..."
        'con_gen': {'level': 'INFO', 'filters': ['require_debug_true'], 'class': 'logging.StreamHandler', 'formatter': 'format_1'},
        'con_g_f': {'level': 'INFO', 'filters': [], 'class': 'logging.FileHandler', 'filename': 'logs/general.log', 'formatter': 'format_3'},
        'con_wrn': {'level': 'WARNING', 'filters': ['require_debug_true'], 'class': 'logging.StreamHandler', 'formatter': 'format_2'},
        'con_err': {'level': 'ERROR', 'filters': ['require_debug_true'], 'class': 'logging.StreamHandler', 'formatter': 'format_4'},
        'gen_log': {'level': 'INFO', 'filters': ['require_debug_true'], 'class': 'logging.FileHandler', 'filename': 'logs/general.log', 'formatter': 'format_3'},
        'err_log': {'level': 'ERROR', 'filters': [], 'class': 'logging.FileHandler', 'filename': 'logs/error.log', 'formatter': 'format_4'},
        'sec_log': {'level': 'INFO', 'filters': [], 'class': 'logging.FileHandler', 'filename': 'logs/security.log', 'formatter': 'format_3'},
        'mailing': {'level': 'ERROR', 'filters': ['require_debug_false'], 'class': 'django.utils.log.AdminEmailHandler', 'formatter': 'format_2', 'include_html': True},
        # 'test': {'level': 'INFO', 'class': 'logging.FileHandler', 'filename': 'logs/full.log', 'formatter': 'full_frm'},
    },
    'loggers': {  # propagate = True - сообщение будет передаваться другим логгерам, иначе нет
        'django': {'handlers': ['con_gen', 'con_g_f', 'con_wrn', 'con_err'], 'level': 'DEBUG', 'propagate': True, },
        # ??? Задание (пункт 1): ... Сюда должны попадать все сообщения с основного логгера django.
        # ??? Текст модуля: django: Логгер верхнего уровня, который принимает все сообщения, но непосредственно в него
        # ничего не записывается. Все сообщения, поступающие в него распределяются по дочерним логгерам.
        # ??? парадокс?
        'django.request': {'handlers': ['err_log', 'mailing'], 'level': 'ERROR', 'propagate': False},
        # ошибки обработки запроса
        'django.server': {'handlers': ['err_log', 'mailing'], 'level': 'INFO', 'propagate': False},
        # сообщения, возникающие на этапе вызова команды runserver
        'django.template': {'handlers': ['err_log'], 'level': 'INFO', 'propagate': False},
        # взаимодействие с системой шаблонов Django
        'django.db.backends': {'handlers': ['err_log'], 'level': 'INFO', 'propagate': False},
        # Сообщения, относящиеся к взаимодействию приложения с базой данных (? только ошибки?)
        'django.security': {'handlers': ['sec_log'], 'level': 'WARNING', 'propagate': False},
        # регистрирует события !нарушения! безопасности
    },
}
