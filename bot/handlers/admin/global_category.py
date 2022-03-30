# from aiogram import types
# from aiogram.dispatcher import FSMContext
#
# from bot.core import dp
# from bot.db.decorators import session_decorator
# from bot.db.models import Category
# from bot.enums import GlobalCategoryActionEnum
# from bot.filters.admin import IsSuperAdmin
# from bot.kb.admin import get_global_category_admin_kb, global_category_callback, get_global_category_action_kb
# from bot.states.admin import TownsState, GlobalCategoryState
#
#
# @dp.callback_query_handler(IsSuperAdmin(), global_category_callback.filter(action=GlobalCategoryActionEnum.view.value))
# @session_decorator(add_param=False)
# async def global_category_list(cq: types.CallbackQuery) -> None:
#     categories_list = await Category.get_list()
#     await cq.message.answer("Список глобальних категорій", reply_markup=get_global_category_admin_kb(categories_list))
#     await cq.answer()
#
#
# @dp.callback_query_handler(IsSuperAdmin(), global_category_callback.filter(action=GlobalCategoryActionEnum.detail.value))
# @session_decorator(add_param=False)
# async def global_category_detail(cq: types.CallbackQuery, callback_data: dict) -> None:
#     category = await Category.get(int(callback_data["category_id"]))
#     await cq.message.answer(f"Назва - {category.name} \n\n"
#                             f"Опис - {category.description}", reply_markup=get_global_category_action_kb(category))
#
#
# @dp.callback_query_handler(IsSuperAdmin(), global_category_callback.filter(action=GlobalCategoryActionEnum.create.value))
# async def global_category_create_btn(cq: types.CallbackQuery) -> None:
#     await GlobalCategoryState.create_name.set()
#
#     await cq.message.answer("Введіть назву глобальної категорії \n"
#                             "Для скасування - /cancel")
#     await cq.answer("Введіть назву глобальної категорії")
#
#
# @dp.message_handler(IsSuperAdmin(), state=GlobalCategoryState.create_name)
# @session_decorator(add_param=False)
# async def global_category_create_name(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["name"] = msg.text
#
#     await msg.answer("Введіть опис категорії!")
#     await GlobalCategoryState.create_desc.set()
#
#
# @dp.message_handler(IsSuperAdmin(), state=GlobalCategoryState.create_desc)
# @session_decorator(add_param=False)
# async def global_category_create_desc(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["description"] = msg.text
#
#     await Category.create(**data, is_global=True)
#
#     await msg.answer("Створено!")
#     await state.finish()
#
#
# @dp.callback_query_handler(IsSuperAdmin(), global_category_callback.filter(action=GlobalCategoryActionEnum.edit_name.value))
# async def global_category_edit_name_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
#     await GlobalCategoryState.edit_name.set()
#
#     async with state.proxy() as data:
#         data["id"] = int(callback_data["category_id"])
#
#     await cq.message.answer("Введіть нову назву \n"
#                             "Для скасування - /cancel")
#     await cq.answer("Введіть нову назву")
#
#
# @dp.message_handler(IsSuperAdmin(), state=GlobalCategoryState.edit_name)
# @session_decorator(add_param=False)
# async def global_category_edit_name(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         category: Category = await Category.get(id=data["id"])
#         await category.update(name=msg.text)
#
#     await state.finish()
#     await msg.answer("Відредаговано!")
#
#
# @dp.callback_query_handler(IsSuperAdmin(),
#                            global_category_callback.filter(action=GlobalCategoryActionEnum.edit_description.value))
# async def global_category_edit_description_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
#     await GlobalCategoryState.edit_description.set()
#
#     async with state.proxy() as data:
#         data["id"] = int(callback_data["category_id"])
#
#     await cq.message.answer("Введіть новий опис \n"
#                             "Для скасування - /cancel")
#     await cq.answer("Введіть новий опис")
#
#
# @dp.message_handler(IsSuperAdmin(), state=GlobalCategoryState.edit_description)
# @session_decorator(add_param=False)
# async def global_category_edit_description(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         category: Category = await Category.get(id=data["id"])
#         await category.update(description=msg.text)
#
#     await state.finish()
#     await msg.answer("Відредаговано!")
#
#
# @dp.callback_query_handler(IsSuperAdmin(), global_category_callback.filter(action=GlobalCategoryActionEnum.delete.value))
# @session_decorator(add_param=False)
# async def global_category_delete_btn(cq: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
#     category = await Category.get(id=int(callback_data["category_id"]))
#     await category.delete()
#
#     await cq.answer("Видалено!")
