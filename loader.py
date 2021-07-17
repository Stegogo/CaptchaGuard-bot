from aiogram import Bot, Dispatcher, types

from data import config

import asyncio
import logging
import gettext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sql import create_pool
import os
import psycopg2

os.environ['DATABASE_URL'] = "postgres://jyufqecsbuaufz:ba2658f4cb8d34361fe71d8d7e4ddea9f711a909abda2f985046d3e1770fd177@ec2-52-19-170-215.eu-west-1.compute.amazonaws.com:5432/dbfno3t6nc4qq6"
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require', port=5432)

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
