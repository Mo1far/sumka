from operator import or_

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.core import dp, bot
from bot.db.decorators import session_decorator
from bot.db.models import Category, User
from bot.kb.user import get_main_user_menu


def get_category_list_menu(categories):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        kb.add(KeyboardButton(category.name))

    kb.add(KeyboardButton("Назад"))
    return kb


@dp.message_handler()
@session_decorator()
async def menu(msg: types.Message, state: FSMContext):
    user = await User.get(msg.from_user.id)
    if msg.text == "Назад":
        data = await state.get_data()
        previous_category_id = data.get("previous_category_id")
        category: Category = await Category.get(previous_category_id) if previous_category_id else None
    else:
        category: Category = await Category.get(None, or_(Category.town_id == None, Category.town_id == user.town_id),
                                                name=msg.text)
    if not category:
        return await msg.answer("Не можу вас зрозуміти", reply_markup=await get_main_user_menu(user.town_id))

    sub_categories = await Category.get_list(or_(Category.town_id == None, Category.town_id == user.town_id),
                                             parent_category_id=category.id)
    if not sub_categories:
        await state.set_data({"previous_category_id": category.parent_category_id})
        return await msg.answer(category.description)

    kb = get_category_list_menu(sub_categories)
    await msg.answer("🕹Оберіть потрібний розділ", reply_markup=kb)

    await state.set_data({"previous_category_id": category.parent_category_id})
