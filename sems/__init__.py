import os
from pathlib import Path
from decouple import  config, Csv



BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY=config('SECRET_KEY')
ALGORITHM=config('ALGORITHM')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# DB_URL=config("DB_URL")
DATABASE_URL=config("DB_URL")
DB_NAME= config("DB_NAME")
ENGINE = config("DB_ENGINE")
HOST = config("DB_HOST")
PASSWORD = config("DB_PASSWORD")
