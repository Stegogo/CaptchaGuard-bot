import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMINS = os.getenv("ADMIN_ID")
host = os.getenv("PGHOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")

I18N_DOMAIN = 'base'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = './locale'
LANGUAGES = ['en', 'ru', 'ua']
