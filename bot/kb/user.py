from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlalchemy import or_

from bot.db.decorators import session_decorator
from bot.db.models import Town, Category

main_user_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Змінити місце проживання"))
category_info_callback = CallbackData("category_info", "category_id")


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@session_decorator()
async def get_main_user_menu(town_id):
    main_user_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main_categories = await Category.get_list(or_(Category.town_id == None, Category.town_id == town_id),
                                              parent_category_id=None)
    for category in main_categories:
        main_user_menu.insert(category.name)
    main_user_menu.insert(KeyboardButton("Змінити місце проживання"))
    return main_user_menu


def get_towns_list(towns: List[Town]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for town in towns:
        kb.insert(KeyboardButton(town.name))
    return kb
