from typing import Tuple, Any
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

import main
from data.config import I18N_DOMAIN, LOCALES_DIR

class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        return await main.get_lang()

def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
