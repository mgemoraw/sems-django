import os
from pathlib import Path
from decouple import  config, Csv
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from urllib.parse import quote_plus




BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


SECRET_KEY=config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

#sqlite database setring
# DB_URL = f"sqlite:///{BASE_DIR}/smees.db"

MailBody = ""

# postgresql database setting
DB_URL=config("DB_URL")
DB_NAME= config("DB_NAME")
DB_ENGINE = config("DB_ENGINE")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_PASSWORD = config("DB_PASSWORD")

class Settings(BaseSettings):
    # app configurations
    APP_NAME: str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG:bool = bool(os.environ.get("DEBUG", False))

    # mail config
    MAIL_HOST:str = config("MAIL_HOST")
    MAIL_USERNAME:str = config("MAIL_USERNAME")
    MAIL_PORT:str = config("MAIL_PORT")
    MAIL_PWD:str = config("MAIL_PASSWORD")


    # mysql database config
    MYSQL_HOST: str = os.environ.get("DB_HOST", "localhost")
    MYSQL_PORT: str = os.environ.get("DB_PORT", "3306")
    MYSQL_DB: str = os.environ.get("DB_NAME", "smees")
    MYSQL_USER: str = os.environ.get("DB_USER", 'root')
    MYSQL_PWD: str = os.environ.get("DB_PASSWORD", 'Mengist#2451')
    DATABASE_URL:str = os.environ.get("DB_URL")
    # DATABASE_URL:str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


    # postgresql datbase configuration
    PG_HOST: str = os.environ.get("PG_HOST", 'localhost')
    PG_PORT: str = os.environ.get("PG_PORT", '5432')
    PG_DB: str = os.environ.get("PG_DB", 'smees')
    PG_USER: str = os.environ.get("DB_USER", 'postgres')
    PG_PWD: str = os.environ.get("DB_PASSWORD", 'root#sgetme')
    PG_URL:str = os.environ.get("PG_URL")





def get_settings() -> Settings:
    return Settings()
