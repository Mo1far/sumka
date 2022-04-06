from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bot.db.models import Category, Town
from bot.enums import CategoryActionEnum, GlobalCategoryActionEnum, TownActionEnum

towns_callback = CallbackData("towns", "action", "town_id")
category_callback = CallbackData("category", "action", "category_id", "town_id")
mailing_callback = CallbackData("mailing", "action", "town_id")

admin_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        "Міста",
        callback_data=towns_callback.new(action=TownActionEnum.view.value, town_id=0),
    ),
    InlineKeyboardButton(
        "Категорії",
        callback_data=category_callback.new(
            action=CategoryActionEnum.view_towns.value, category_id=0, town_id=0
        ),
    ),
    InlineKeyboardButton(
        "Розсилка", callback_data=mailing_callback.new(action="start", town_id=0)
    ),
)


def get_towns_admin_kb(towns_list: List[Town]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for town in towns_list:
        kb.row(
            InlineKeyboardButton(
                f"{town.name} ✏️",
                callback_data=towns_callback.new(
                    action=TownActionEnum.edit.value, town_id=town.id
                ),
            ),
            InlineKeyboardButton(
                "Видалити ❌",
                callback_data=towns_callback.new(
                    action=TownActionEnum.delete.value, town_id=town.id
                ),
            ),
        )
    kb.add(
        InlineKeyboardButton(
            "Додати місто",
            callback_data=towns_callback.new(
                action=TownActionEnum.create.value, town_id=0
            ),
        )
    )
    return kb


def get_town_for_categories(towns: List[Town]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for town in towns:
        kb.add(
            InlineKeyboardButton(
                town.name,
                callback_data=category_callback.new(
                    action=CategoryActionEnum.view_by_town.value,
                    category_id=0,
                    town_id=town.id,
                ),
            )
        )

    return kb


def get_categories_for_town(
    categories: List[Category], town_id: int, parent_category_id: int = 0
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for category in categories:
        kb.row(
            InlineKeyboardButton(
                f"{category.name} Огляд",
                callback_data=category_callback.new(
                    action=GlobalCategoryActionEnum.detail.value,
                    category_id=category.id,
                    town_id=town_id,
                ),
            ),
            InlineKeyboardButton(
                "Видалити ❌",
                callback_data=category_callback.new(
                    action=GlobalCategoryActionEnum.delete.value,
                    category_id=category.id,
                    town_id=town_id,
                ),
            ),
        )
    if parent_category_id:
        kb.add(
            InlineKeyboardButton(
                "Додати під категорію",
                callback_data=category_callback.new(
                    action=CategoryActionEnum.add_sub_category.value,
                    category_id=parent_category_id,
                    town_id=town_id,
                ),
            )
        )
    else:
        kb.add(
            InlineKeyboardButton(
                "Додати категорію",
                callback_data=category_callback.new(
                    action=CategoryActionEnum.create.value,
                    category_id=0,
                    town_id=town_id,
                ),
            )
        )
    return kb


def get_category_action_kb(category, town_id):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(
            f"Редагувати назву ✏️",
            callback_data=category_callback.new(
                action=CategoryActionEnum.edit_name.value,
                category_id=category.id,
                town_id=0,
            ),
        ),
        InlineKeyboardButton(
            f"Редагувати опис ✏️",
            callback_data=category_callback.new(
                action=CategoryActionEnum.edit_description.value,
                category_id=category.id,
                town_id=0,
            ),
        ),
        InlineKeyboardButton(
            f"Додати підкатегорію ✏️",
            callback_data=category_callback.new(
                action=CategoryActionEnum.add_sub_category.value,
                category_id=category.id,
                town_id=category.town_id or town_id,
            ),
        ),
        InlineKeyboardButton(
            f"Дивитися підкатегорії ✏️",
            callback_data=category_callback.new(
                action=CategoryActionEnum.view_sub_category.value,
                category_id=category.id,
                town_id=category.town_id or town_id,
            ),
        ),
        InlineKeyboardButton(
            "Зробити глобальною",
            callback_data=category_callback.new(
                action=CategoryActionEnum.make_global.value,
                category_id=category.id,
                town_id=category.town_id or 0,
            ),
        ),
        InlineKeyboardButton(
            "Видалити ❌",
            callback_data=category_callback.new(
                action=CategoryActionEnum.delete.value,
                category_id=category.id,
                town_id=0,
            ),
        ),
    )

    return kb


def get_towns_for_mailing(towns: List[Town]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "Глобально",
            callback_data=mailing_callback.new(town_id=0, action="assing_town"),
        )
    )

    for town in towns:
        kb.add(
            InlineKeyboardButton(
                town.name,
                callback_data=mailing_callback.new(
                    town_id=town.id, action="assing_town"
                ),
            )
        )

    return kb
