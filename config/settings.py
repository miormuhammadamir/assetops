import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY','development-only-unsafe-key')
DEBUG=os.environ.get('DJANGO_DEBUG','0')=='1'
if not DEBUG and SECRET_KEY=='development-only-unsafe-key':
    raise ImproperlyConfigured('Set DJANGO_SECRET_KEY when DEBUG=0')
ALLOWED_HOSTS=[h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS','127.0.0.1,localhost').split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS=[h.strip() for h in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS','').split(',') if h.strip()]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','operations']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
if os.environ.get('POSTGRES_DB'):
    DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.environ['POSTGRES_DB'],'USER':os.environ.get('POSTGRES_USER',''),'PASSWORD':os.environ.get('POSTGRES_PASSWORD',''),'HOST':os.environ.get('POSTGRES_HOST','127.0.0.1'),'PORT':os.environ.get('POSTGRES_PORT','5432')}}
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='en-us'; TIME_ZONE=os.environ.get('DJANGO_TIME_ZONE','Asia/Kuala_Lumpur'); USE_I18N=True; USE_TZ=True
STATIC_URL='static/';STATICFILES_DIRS=[BASE_DIR/'static'];STATIC_ROOT=BASE_DIR/'staticfiles'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='login';LOGIN_REDIRECT_URL='dashboard';LOGOUT_REDIRECT_URL='login'
SESSION_COOKIE_HTTPONLY=True;CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SECURE=not DEBUG;CSRF_COOKIE_SECURE=not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF=True;SECURE_REFERRER_POLICY='same-origin';X_FRAME_OPTIONS='DENY'
SECURE_SSL_REDIRECT=os.environ.get('DJANGO_SECURE_SSL_REDIRECT','0')=='1'
SECURE_HSTS_SECONDS=int(os.environ.get('DJANGO_HSTS_SECONDS','0'))
