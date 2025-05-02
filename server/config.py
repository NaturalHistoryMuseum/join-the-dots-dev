import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)
    # Force load .env file
    load_dotenv(override=True)

    # Database Configuration

    # FOR LOCAL TESTING
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_NEW_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    # Secondary Database Configuration
    # FOR LOCAL TESTING
    SECONDARY_DB_HOST = os.getenv("SECONDARY_DB_HOST")
    SECONDARY_DB_USER = os.getenv("SECONDARY_DB_USER")
    SECONDARY_DB_PASSWORD = os.getenv("SECONDARY_DB_PASSWORD")
    SECONDARY_DB_NAME = os.getenv("SECONDARY_DB_NAME")

    # FOR K8S
    # MYSQL_HOST = os.environ.get("MYSQL_HOST")
    # MYSQL_USER = os.environ.get("MYSQL_USER")
    # MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    # MYSQL_DB = os.environ.get("MYSQL_DATABASE")
