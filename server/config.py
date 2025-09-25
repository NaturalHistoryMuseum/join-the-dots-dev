import os
from datetime import timedelta

from dotenv import load_dotenv


class Config:
    # Force load .env file
    load_dotenv(override=True)

    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DATABASE')

    # Azure Configuration
    CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    TENANT_ID = os.environ.get('AZURE_TENANT_ID')
    REDIRECT_URI = os.environ.get('AZURE_REDIRECT_URI')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'None'
    JWT_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Power BI Configuration
    AUDIENCE = f'api://{CLIENT_ID}'
    ISSUER = f'https://login.microsoftonline.com/{TENANT_ID}/v2.0'
    VALID_ISSUERS = [
        f'https://login.microsoftonline.com/{TENANT_ID}/v2.0',
        f'https://login.microsoftonline.com/{TENANT_ID}/',
        f'https://sts.windows.net/{TENANT_ID}/',
    ]
    JWKS_URL = f'https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys'
