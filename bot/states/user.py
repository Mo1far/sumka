from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    wait_town = State()


class UserMenuState(StatesGroup):
    main_menu = State()