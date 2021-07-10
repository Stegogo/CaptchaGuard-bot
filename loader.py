from aiogram import Bot, Dispatcher, types

from data import config

import asyncio
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sql import create_pool

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = loop.run_until_complete(create_pool())
