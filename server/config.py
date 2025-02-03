import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)

    # Database Configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

    # Secondary Database Configuration
    SECONDARY_DB_HOST = os.getenv("SECONDARY_DB_HOST")
    SECONDARY_DB_USER = os.getenv("SECONDARY_DB_USER")
    SECONDARY_DB_PASSWORD = os.getenv("SECONDARY_DB_PASSWORD")
    SECONDARY_DB_NAME = os.getenv("SECONDARY_DB_NAME")

    # Azure OAuth Configuration
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    AZURE_REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI")
