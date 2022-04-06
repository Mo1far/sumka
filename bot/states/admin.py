from aiogram.dispatcher.filters.state import State, StatesGroup


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


class MailingState(StatesGroup):
    add_text = State()
    add_town = State()
