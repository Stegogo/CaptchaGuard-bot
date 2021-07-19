from aiogram import Bot, Dispatcher, types

from data import config

import asyncio
import logging
import gettext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import psycopg2

import urllib.parse as urlparse
import os

url1 = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname1 = url1.path[1:]
user1 = url1.username
password1 = url1.password
host1 = url1.hostname
port1 = url1.port

con = psycopg2.connect(
            dbname=dbname1,
            user=user1,
            password=password1,
            host=host1,
            port=port1
            )
con.autocommit = True

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
from middlewares.language_middlware import setup_middleware
i18n = setup_middleware(dp)
_ = i18n.gettext
db = con
