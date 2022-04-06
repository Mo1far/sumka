from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegisterState(StatesGroup):
    wait_town = State()


class UserMenuState(StatesGroup):
    main_menu = State()
