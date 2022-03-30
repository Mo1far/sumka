from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

dp: Dispatcher
bot: Bot


def create_dp(config: dict):
    global dp, bot
    bot = Bot(config["bot_token"], parse_mode=ParseMode.HTML, validate_token=True)
    # storage = RedisStorage2(**config.redis)
    storage = MemoryStorage()

    dp = Dispatcher(bot, storage=storage)

    return dp
