from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import Town
from bot.enums import TownActionEnum
from bot.filters.admin import IsSuperAdmin
from bot.kb.admin import admin_kb, towns_callback, get_towns_admin_kb
from bot.states.admin import TownsState


@dp.callback_query_handler(IsSuperAdmin(), towns_callback.filter(action=TownActionEnum.view.value))
@session_decorator(add_param=False)
async def town_list(cq: types.CallbackQuery) -> None:
    towns_list = await Town.get_list()
    await cq.message.answer("Список міст", reply_markup=get_towns_admin_kb(towns_list))
    await cq.answer()


@dp.callback_query_handler(IsSuperAdmin(), towns_callback.filter(action=TownActionEnum.create.value))
async def town_create_start(cq: types.CallbackQuery) -> None:
    await TownsState.create.set()

    await cq.message.answer("Введіть назву міста \n"
                            "Для скасування - /cancel")
    await cq.answer("Введіть назву міста")


@dp.message_handler(IsSuperAdmin(), state=TownsState.create)
@session_decorator(add_param=False)
async def town_create(msg: types.Message, state: FSMContext):
    await Town.create(name=msg.text)
    await state.finish()
    await msg.answer("Створено!")


@dp.callback_query_handler(IsSuperAdmin(), towns_callback.filter(action=TownActionEnum.edit.value))
async def town_edit_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await TownsState.edit.set()

    town_id = callback_data.get("town_id")
    async with state.proxy() as data:
        data["town_id"] = town_id

    await cq.message.answer("Введіть нову назву \n"
                            "Для скасування - /cancel")
    await cq.answer("Введіть нову назву")


@dp.message_handler(IsSuperAdmin(), state=TownsState.edit)
@session_decorator(add_param=False)
async def town_edit(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        town_id = int(data["town_id"])
    town = await Town.get(id=town_id)

    await town.update(name=msg.text)
    await state.finish()
    await msg.answer("Відредаговано!")


@dp.callback_query_handler(IsSuperAdmin(), towns_callback.filter(action=TownActionEnum.delete.value))
@session_decorator(add_param=False)
async def town_delete_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    town_id = int(callback_data["town_id"])
    town = await Town.get(None, id=town_id)
    await town.delete()

    await cq.answer("Видалено!")
