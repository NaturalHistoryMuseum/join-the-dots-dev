import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    # Force load .env file in this directory
    env_path = Path(__file__).resolve().parent / '.env'
    load_dotenv(dotenv_path=env_path, override=True)

    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DATABASE')
