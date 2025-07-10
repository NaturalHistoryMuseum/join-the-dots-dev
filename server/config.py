import os

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
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_COOKIE_CSRF_PROTECT = True
