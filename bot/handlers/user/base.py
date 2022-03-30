from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import or_

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import User, Category
from bot.kb.user import get_categories_info, category_info_callback


@dp.message_handler(text=["Отримати допомогу"])
@session_decorator(add_param=False)
async def start(msg: types.Message, state: FSMContext):
    user = await User.get(msg.from_user.id)
    categories = await Category.get_list(or_(Category.parent_category_id == None, Category.town_id == user.town_id))
    await msg.answer("Оберіть категорії яка вас цікавить", reply_markup=get_categories_info(categories))


@dp.callback_query_handler(category_info_callback.filter())
@session_decorator(add_param=False)
async def category_info(cq: types.CallbackQuery, callback_data: dict):
    category = await Category.get(int(callback_data["category_id"]))
    await cq.message.answer(category.description)
    await cq.answer()
