from aiogram import types

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import Category
from bot.kb.user import category_info_callback


@dp.callback_query_handler(category_info_callback.filter())
@session_decorator(add_param=False)
async def category_info(cq: types.CallbackQuery, callback_data: dict):
    category = await Category.get(int(callback_data["category_id"]))
    await cq.message.answer(category.description)
    await cq.answer()
