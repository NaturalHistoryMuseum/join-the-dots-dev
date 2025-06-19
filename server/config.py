import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Force load .env file
    load_dotenv(override=True)

    # FOR LOCAL TESTING
    SECRET_KEY = os.getenv('SECRET_KEY')

    # FOR K8S
    # SECRET_KEY = os.environ.get("SECRET_KEY")

    # Database Configuration

    # FOR LOCAL TESTING
    MYSQL_HOST = os.getenv('SECONDARY_DB_HOST')
    MYSQL_USER = os.getenv('SECONDARY_DB_USER')
    MYSQL_PASSWORD = os.getenv('SECONDARY_DB_PASSWORD')
    MYSQL_DB = os.getenv('SECONDARY_DB_NAME')

    # FOR K8S
    # MYSQL_HOST = os.environ.get("MYSQL_HOST")
    # MYSQL_USER = os.environ.get("MYSQL_USER")
    # MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    # MYSQL_DB = os.environ.get("MYSQL_DATABASE")
