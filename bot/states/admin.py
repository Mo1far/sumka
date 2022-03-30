from aiogram.dispatcher.filters.state import StatesGroup, State


class TownsState(StatesGroup):
    create = State()
    edit = State()


class GlobalCategoryState(StatesGroup):
    create_name = State()
    create_desc = State()

    edit_name = State()
    edit_description = State()


class CategoryState(StatesGroup):
    create_name = State()
    create_desc = State()

    edit_name = State()
    edit_description = State()
