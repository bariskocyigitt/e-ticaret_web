"""
Django settings for minishop project (deploy-ready).
"""

from pathlib import Path
import os  # NEW: üretimde ortam değişkenlerini kullanacağız

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Security / Env ===
# CHANGED: Sabit anahtar yerine ortam değişkeni; prod'da SECRET_KEY'i Render/Railway'da set edeceğiz
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

# CHANGED: DEBUG'i ortam değişkeninden oku (lokalde True, canlıda False yapacağız)
DEBUG = os.getenv("DEBUG", "True") == "True"

# CHANGED: Canlı ortamda Render domainini (veya kendi domainini) ALLOWED_HOSTS'a env ile ver
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # NEW: statikleri prod’da Whitenoise ile servis et
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
        # shop/templates klasörü
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
# Not: Demo/deploy için SQLite bırakıldı. Kalıcı DB istersen Postgres'e geçebiliriz.
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
STATICFILES_DIRS = [BASE_DIR / "static"]            # /static/ için kaynak klasörler
STATIC_ROOT = BASE_DIR / "staticfiles"              # collectstatic hedefi (deploy)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # NEW

# === Security behind proxy (Render gibi) ===
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]  # NEW: canlıda CSRF hatası olmasın
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # NEW: proxy ardında doğru scheme

# (Opsiyonel) Canlıda cookie güvenliğini sıkılaştır
if not DEBUG:  # NEW
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# === Auth redirects ===
LOGIN_URL = "signup"            # CHANGED: girişsiz kullanıcı kayıt sayfasına yönlensin
LOGIN_REDIRECT_URL = "orders"
LOGOUT_REDIRECT_URL = "home"

# === Defaults ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
