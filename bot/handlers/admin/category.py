from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import or_

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import Town, Category
from bot.enums import CategoryActionEnum
from bot.filters.admin import IsSuperAdmin
from bot.kb.admin import category_callback, get_town_for_categories, get_categories_for_town, get_category_action_kb
from bot.states.admin import CategoryState


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.view_towns.value))
@session_decorator(add_param=False)
async def category_towns_list(cq: types.CallbackQuery) -> None:
    towns = await Town.get_list()
    await cq.message.answer("Список міст для категорій", reply_markup=get_town_for_categories(towns))
    await cq.answer()


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.view_by_town.value))
@session_decorator(add_param=False)
async def category_by_town_list(cq: types.CallbackQuery, callback_data: dict) -> None:
    town_id = int(callback_data["town_id"])
    town = await Town.get(None, id=town_id)
    categories = await Category.get_list(or_(Category.town_id == None, Category.town_id == town_id), parent_category_id=None)
    await cq.message.answer(f"Список категорій для {town.name}",
                            reply_markup=get_categories_for_town(categories, town_id))
    await cq.answer()


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.view_sub_category.value))
@session_decorator(add_param=False)
async def sub_category_by_town_list(cq: types.CallbackQuery, callback_data: dict) -> None:
    town_id = int(callback_data["town_id"])
    parent_category = await Category.get(None, id=int(callback_data["category_id"]))
    town = await Town.get(None, id=town_id)
    categories = await Category.get_list(town_id=town_id, parent_category_id=parent_category.id)
    await cq.message.answer(f"Список підкатегорій для {town.name} {parent_category.name}",
                            reply_markup=get_categories_for_town(categories, town_id))
    await cq.answer()


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.create.value))
@session_decorator(add_param=False)
async def create_category_by_town_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await CategoryState.create_name.set()
    async with state.proxy() as data:
        data["town_id"] = int(callback_data["town_id"])

    await cq.message.answer("Введіть назву категорії \n"
                            "Для скасування - /cancel")
    await cq.answer("Введіть назву категорії")


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.add_sub_category.value))
@session_decorator(add_param=False)
async def create_sub_category_by_town_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await CategoryState.create_name.set()
    async with state.proxy() as data:
        data["town_id"] = int(callback_data["town_id"])
        data["parent_category_id"] = int(callback_data["category_id"])

    await cq.message.answer("Введіть назву категорії \n"
                            "Для скасування - /cancel")
    await cq.answer("Введіть назву категорії")


@dp.message_handler(IsSuperAdmin(), state=CategoryState.create_name)
@session_decorator(add_param=False)
async def create_category_name_by_town(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = msg.text

    await msg.answer("Введіть опис категорії!")
    await CategoryState.create_desc.set()


@dp.message_handler(IsSuperAdmin(), state=CategoryState.create_desc)
@session_decorator(add_param=False)
async def create_category_desc_by_town(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = msg.text

    await Category.create(**data)
    await msg.answer("Створено!")
    await state.finish()


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.detail.value))
@session_decorator(add_param=False)
async def detail_category_by_town_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    category = await Category.get(None, id=int(callback_data["category_id"]))
    town_id = int(callback_data["town_id"])

    await cq.message.answer(f"Назва - {category.name} \n\n"
                            f"Опис - {category.description}", reply_markup=get_category_action_kb(category, town_id=town_id))
    await cq.answer()


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.delete.value))
@session_decorator(add_param=False)
async def category_delete_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    category = await Category.get(None, id=int(callback_data["category_id"]))
    await category.delete()

    await cq.answer("Видалено!")


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.edit_name.value))
async def category_edit_name_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await CategoryState.edit_name.set()

    async with state.proxy() as data:
        data["id"] = int(callback_data["category_id"])

    await cq.message.answer("Введіть нову назву \n"
                            "Для скасування - /cancel")
    await cq.answer("Введіть нову назву")


@dp.message_handler(IsSuperAdmin(), state=CategoryState.edit_name)
@session_decorator(add_param=False)
async def category_edit_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category: Category = await Category.get(None, id=data["id"])
        await category.update(name=msg.text)

    await state.finish()
    await msg.answer("Відредаговано!")


@dp.callback_query_handler(IsSuperAdmin(), category_callback.filter(action=CategoryActionEnum.edit_description.value))
async def category_edit_description_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await CategoryState.edit_description.set()

    async with state.proxy() as data:
        data["id"] = int(callback_data["category_id"])

    await cq.message.answer("Введіть новий опис \n"
                            "Для скасування - /cancel")
    await cq.answer("Введіть новий опис")


@dp.message_handler(IsSuperAdmin(), state=CategoryState.edit_description)
@session_decorator(add_param=False)
async def category_edit_description(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category: Category = await Category.get(None, id=data["id"])
        await category.update(description=msg.text)

    await state.finish()
    await msg.answer("Відредаговано!")
