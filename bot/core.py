from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode

dp: Dispatcher
bot: Bot


def create_dp(config: dict):
    global dp, bot
    bot = Bot(config["bot_token"], parse_mode=ParseMode.HTML, validate_token=True)
    storage = RedisStorage2(host=config["redis_host"],
                            port=config["redis_port"],
                            db=config["redis_db"],
                            password=config["redis_password"],
                            prefix=config["redis_prefix"]
                            )

    dp = Dispatcher(bot, storage=storage)

    return dp
