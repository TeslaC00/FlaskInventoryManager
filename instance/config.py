import os
from datetime import timedelta


class APIConfig:
    API_TITLE = "FlaskInventoryManager"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.0"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"


class Config(APIConfig):
    SECRET_KEY = "2e95ecc7acac7ebd88d45c6ae64e3dcea45e625de589e504" # change for PROD
    SECURITY_PASSWORD_SALT = "109801664110750927464141306118929706514" # change for PROD
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USERNAME_REQUIRED = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True
    }  # recommended by flask security too
    JWT_SECRET_KEY = "70fde58923028a892a7978e9e900cf07abfc82a37830b7b5" # change for PROD
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=15
    )  # Access tokens expire after 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)  # Refresh tokens expire after 30 days
    SECURITY_LOGIN_URL = "/login"
    SECURITY_TRACKABLE = True
    SECURITY_LOGIN_USER_TEMPLATE = "security/login_user.html"

    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_CSRF_PROTECT = True
    # JWT_ACCESS_COOKIE_PATH = '/'  # Path where the access token cookie is valid
    # JWT_REFRESH_COOKIE_PATH = '/token/refresh'  # Path where the refresh token cookie is valid
    # JWT_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
    JWT_COOKIE_SAMESITE = "Strict"  # Controls the samesite attribute for cookies
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie" # change for PROD
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie" # change for PROD

    # SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    # SECURITY_TOKEN_AUTHENTICATION_METHODS = ['Bearer']


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False  # don't know if it works
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql://USERNAME:PASSWORD@localhost:3306/DB_NAME"
