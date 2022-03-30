from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import User, Town
from bot.kb.user import main_user_menu, get_towns_list




@dp.message_handler(commands=["cancel"], state="*")
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("Скасовано")
