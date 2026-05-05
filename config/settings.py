import os, random, string, boto3, os, json
from pathlib import Path
from dotenv import load_dotenv
from str2bool import str2bool
from django.contrib.messages import constants as messages
from botocore.exceptions import ClientError
from pathlib import Path

load_dotenv()

def get_secret(secret_name):
  region_name = "us-east-1"

  session = boto3.session.Session()
  client = session.client(
    service_name="secretsmanager",
    region_name=region_name,
  )

  try:
    response = client.get_secret_value(SecretId=secret_name)
  except ClientError as e:
    raise RuntimeError(f"Secrets Manager error: {e}")

  secret_string = response.get("SecretString")
  if not secret_string:
    raise RuntimeError("SecretString is empty")

  return json.loads(secret_string)  

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "staging":
    secrets = get_secret("restore/staging/db")
else:
    secrets = {}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.get("SECRET_KEY") or os.environ.get("SECRET_KEY")

if not SECRET_KEY:
  SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))

# Enable/Disable DEBUG Mode
DEBUG = True#str2bool(os.environ.get('DEBUG'))

# Docker HOST
ALLOWED_HOSTS = ['*']

# Add here your deployment HOSTS
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'https://new.restorecalendar.com', 'https://app.restorecalendar.com']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:    
  ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",
  "django_crontab",
  "auditlog",

  # Serve UI pages
  "apps.restore",

  # Tooling API-GEN
  'rest_framework',            # Include DRF           # <-- NEW 
  'rest_framework.authtoken',  # Include DRF Auth      # <-- NEW   
]

AUTH_USER_MODEL = 'restore.User'

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "whitenoise.middleware.WhiteNoiseMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
  "auditlog.middleware.AuditlogMiddleware"
]

AUTHENTICATION_BACKENDS = [
  'apps.restore.backends.EmailBackend',
  'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = "config.urls"

HOME_TEMPLATES = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
  {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [HOME_TEMPLATES],
    "APP_DIRS": True,
    "OPTIONS": {
      "context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
      ],
    },
  },
]

WSGI_APPLICATION = "config.wsgi.application"

# Messages

MESSAGE_TAGS = {
  messages.DEBUG:   'secondary',
  messages.INFO:    'info',
  messages.SUCCESS: 'success',
  messages.WARNING: 'warning',
  messages.ERROR:   'danger',
}

# Database

if ENVIRONMENT == "staging" and secrets:
  DB_ENGINE   = secrets.get("DB_ENGINE")
  DB_USERNAME = secrets.get("DB_USERNAME")
  DB_PASSWORD = secrets.get("DB_PASSWORD")
  DB_HOST     = secrets.get("DB_HOST")
  DB_PORT     = secrets.get("DB_PORT")
  DB_NAME     = secrets.get("DB_NAME")
else:
  DB_ENGINE   = os.getenv('DB_ENGINE'   , 'django.db.backends.postgresql')
  DB_USERNAME = os.getenv('DB_USERNAME' , 'postgres')
  DB_PASSWORD = os.getenv('DB_PASSWORD' ,'amrutha123')
  DB_HOST     = os.getenv('DB_HOST'     , 'localhost')
  DB_PORT     = os.getenv('DB_PORT'     , '5432')
  DB_NAME     = os.getenv('DB_NAME'     , 'djan_db')


if DB_ENGINE and DB_NAME and DB_USERNAME:
  DATABASES = { 
    'default': {
      'ENGINE'  : 'django.db.backends.postgresql', 
      'NAME'    : 'djan_db',
      'USER'    : 'postgres',
      'PASSWORD': 'amrutha123',
      'HOST'    : 'localhost',
      'PORT'    : '5432',
    }, 
  }

# Password validation

AUTH_PASSWORD_VALIDATORS = [
  {
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
  },
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "login"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.TokenAuthentication',
  ],
}

# Cron Jobs

CRONJOBS = [
  # (schedule, task, [args], [kwargs], [suffix (>> /var/log/cron_digest.log 2>&1)])
  ('0 6 * * *', 'apps.restore.cron.send_nudges', ['morning'], {}),
  ('0 12 * * *', 'apps.restore.cron.send_nudges', ['midday'], {}),
  ('0 18 * * *', 'apps.restore.cron.send_nudges', ['evening'], {}),
  ('0 2 * * *', 'apps.restore.cron.assign_suggestions', [], {}),
]