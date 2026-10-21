import os
from pathlib import Path
BASE_DIR = Path(os.getenv('QIMA_BASE_DIR', Path(__file__).resolve().parent.parent))
DATA_DIR = Path(os.getenv('QIMA_DATA_DIR', BASE_DIR / 'data'))
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'unsafe-dev-key-change-before-deploy')
DEBUG = os.getenv('DJANGO_DEBUG', '0') == '1'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('DJANGO_ALLOWED_HOSTS','localhost,127.0.0.1').split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [x.strip() for x in os.getenv('CSRF_TRUSTED_ORIGINS','').split(',') if x.strip()]
INSTALLED_APPS = [
 'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
 'django.contrib.messages','django.contrib.staticfiles','apps.dashboard','apps.bookings',
]
MIDDLEWARE = [
 'django.middleware.clickjacking.XFrameOptionsMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware',   # ← add this line
 'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'
ASGI_APPLICATION='config.asgi.application'
DB_ENGINE=os.getenv('DB_ENGINE','sqlite3')
if DB_ENGINE == 'postgresql':
 DATABASES={'default':{
  'ENGINE':'django.db.backends.postgresql',
  'NAME':os.getenv('POSTGRES_DB','qima'),
  'USER':os.getenv('POSTGRES_USER','qima'),
  'PASSWORD':os.getenv('POSTGRES_PASSWORD',''),
  'HOST':os.getenv('POSTGRES_HOST','localhost'),
  'PORT':os.getenv('POSTGRES_PORT','5432'),
 }}
else:
 DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':DATA_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'}]
LANGUAGE_CODE='en-us'
TIME_ZONE=os.getenv('TZ','Asia/Phnom_Penh')
USE_I18N=True
USE_TZ=True
STATIC_URL='static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
MEDIA_URL='media/'
MEDIA_ROOT=Path(os.getenv('MEDIA_ROOT', DATA_DIR/'uploads'))
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='login'
LOGIN_REDIRECT_URL='dashboard'
LOGOUT_REDIRECT_URL='login'
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=False
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS='DENY'
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https') if os.getenv('TRUST_PROXY_SSL','0') == '1' else None
