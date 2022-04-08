from operator import or_

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import select

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import Category, MessageLog, User
from bot.kb.user import get_main_user_menu


def get_category_list_menu(categories):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for category in categories:
        kb.insert(KeyboardButton(category.name))

    kb.add(KeyboardButton("↩ Назад"))
    return kb


@dp.message_handler()
@session_decorator(add_param=True)
async def menu(current_session, msg: types.Message, state: FSMContext):
    user = await User.get(msg.from_user.id)
    await MessageLog.create(text=msg.text, user_id=user.id, user_town_id=user.town_id)

    if msg.text == "↩ Назад":
        data = await state.get_data()
        if previous_category_id := data.get("previous_category_id"):
            category: Category = (
                await Category.get(previous_category_id)
                if previous_category_id
                else None
            )
        else:
            return await msg.answer(
                "🕹Оберіть потрібний розділ",
                reply_markup=await get_main_user_menu(user.town_id),
            )

    else:
        category: Category = await Category.get(
            None,
            or_(Category.town_id == None, Category.town_id == user.town_id),
            name=msg.text,
        )
    if not category:
        return await msg.answer(
            "Не можу вас зрозуміти", reply_markup=await get_main_user_menu(user.town_id)
        )

    query = (
        select(Category)
        .filter_by(parent_category_id=category.id)
        .filter(or_(Category.town_id == None, Category.town_id == user.town_id))
        .order_by(Category.rating.desc(), Category.id)
    )
    sub_categories = (await current_session.execute(query)).scalars().all()

    if not sub_categories:
        if parent_category := await Category.get(None, id=category.parent_category_id):
            await state.set_data(
                {"previous_category_id": parent_category.parent_category_id}
            )
        return await msg.answer(category.description, disable_web_page_preview=True)

    kb = get_category_list_menu(sub_categories)
    await msg.answer("🕹Оберіть потрібний розділ", reply_markup=kb)

    if category.parent_category_id:
        await state.set_data({"previous_category_id": category.parent_category_id})
    else:
        await state.set_data({})
