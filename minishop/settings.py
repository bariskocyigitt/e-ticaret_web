"""
Django settings for minishop project (updated).
"""

from pathlib import Path

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Security ===
SECRET_KEY = "dev-secret-key"  # PROD: ortam değişkeninden ver
DEBUG = True                   # PROD: False yap
ALLOWED_HOSTS: list[str] = []  # Deploy'da alan adını ekle

# === Apps ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "shop",
]

# === Middleware ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "minishop.urls"

# === Templates ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # shop/templates klasörünü kullan
        "DIRS": [BASE_DIR / "shop" / "templates"],
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

WSGI_APPLICATION = "minishop.wsgi.application"

# === Database ===
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# === Password validation ===
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# === i18n / tz ===
LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

# === Static files ===
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]       # /static/ için kaynak klasörler
STATIC_ROOT = BASE_DIR / "staticfiles"         # collectstatic hedefi (deploy)

# === Auth redirects ===
LOGIN_URL = "signup"
LOGIN_REDIRECT_URL = "orders"
LOGOUT_REDIRECT_URL = "home"

# === Defaults ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
