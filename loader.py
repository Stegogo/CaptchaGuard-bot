from aiogram import Bot, Dispatcher, types

from data import config

import asyncio
import logging
import gettext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sql import create_pool
import os
import psycopg2

os.environ['DATABASE_URL'] = "postgres://mgfxmdcettahps:cd1a197a7e128b11e3f86e6aa0de5a87ae45494fca839837cbedd9bbb1385c9a@ec2-54-220-195-236.eu-west-1.compute.amazonaws.com:5432/darcoeb8hro3p1"
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require', port=(process.env.PORT or 8080))

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
from middlewares.language_middlware import setup_middleware
i18n = setup_middleware(dp)
_ = i18n.gettext
db = conn
