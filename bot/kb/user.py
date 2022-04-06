from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from sqlalchemy import or_, select

from bot.db.decorators import session_decorator
from bot.db.models import Category, Town

category_info_callback = CallbackData("category_info", "category_id")


@session_decorator(add_param=True)
async def get_main_user_menu(current_session, town_id):
    main_user_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = (
        select(Category)
        .filter_by(parent_category_id=None)
        .filter(or_(Category.town_id == None, Category.town_id == town_id))
        .order_by(Category.rating.desc(), Category.id)
    )
    main_categories = (await current_session.execute(query)).scalars().all()

    # main_categories = await Category.get_list(or_(Category.town_id == None, Category.town_id == town_id),
    #                                           parent_category_id=None)
    for category in main_categories:
        main_user_menu.insert(category.name)
    main_user_menu.insert(KeyboardButton("⚙ Змінити місце проживання"))
    return main_user_menu


def get_towns_list(towns: List[Town]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for town in towns:
        kb.insert(KeyboardButton(town.name))
    return kb
