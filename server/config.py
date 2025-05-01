import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)
    # Force load .env file
    load_dotenv(override=True)

    # Database Configuration

    # FOR LOCAL DEVELOPMENT ONLY
    # MYSQL_HOST = os.getenv("MYSQL_HOST")
    # MYSQL_USER = os.getenv("MYSQL_USER")
    # MYSQL_NEW_PASSWORD = os.getenv("MYSQL_NEW_PASSWORD")
    # MYSQL_DB = os.getenv("MYSQL_DB")

    # FOR PRODUCTION
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_NEW_PASSWORD = os.environ.get("MYSQL_NEW_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")

    print("MYSQL_HOST:", MYSQL_HOST)
    print("MYSQL_USER:", MYSQL_USER)
    print("MYSQL_NEW_PASSWORD:", MYSQL_NEW_PASSWORD)
    print("MYSQL_DB:", MYSQL_DB)

    # Secondary Database Configuration
    # FOR LOCAL TESTGING
    # SECONDARY_DB_HOST = os.getenv("SECONDARY_DB_HOST")
    # SECONDARY_DB_USER = os.getenv("SECONDARY_DB_USER")
    # SECONDARY_DB_PASSWORD = os.getenv("SECONDARY_DB_PASSWORD")
    # SECONDARY_DB_NAME = os.getenv("SECONDARY_DB_NAME")

    # Azure OAuth Configuration
    # FOR LOCAL TESTGING
    # AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    # AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    # AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    # AZURE_REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI")

    # FOR K8S
    AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
    AZURE_REDIRECT_URI = os.environ.get("AZURE_REDIRECT_URI")
