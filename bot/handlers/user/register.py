from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from sqlalchemy import select

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import User, Town
from bot.kb.user import get_towns_list, get_main_user_menu
from bot.states.user import UserRegisterState


@dp.message_handler(commands=["start"], state="*")
@session_decorator(add_param=True)
async def start(current_session, msg: types.Message, state: FSMContext):
    user = await User.get(msg.from_user.id)

    if user:
        await msg.answer("Ласкаво просимо",
                         reply_markup=await get_main_user_menu(user.town_id))
    else:
        await User.create(id=msg.from_user.id,
                          name=msg.from_user.full_name,
                          user_name=msg.from_user.username)
        query = select(Town).order_by(Town.rating.desc(), Town.id)
        towns = (await current_session.execute(query)).scalars().all()

        await UserRegisterState.wait_town.set()
        await msg.answer("Оберіть ваше місце проживання", reply_markup=get_towns_list(towns))


@dp.message_handler(Text(equals="⚙ Змінити місце проживання"))
@session_decorator(add_param=True)
async def change_user_town(current_session, msg: types.Message, state: FSMContext):
    query = select(Town).order_by(Town.rating.desc(), Town.id)
    towns = (await current_session.execute(query)).scalars().all()

    # towns = await Town.get_list()
    await UserRegisterState.wait_town.set()
    await msg.answer("Оберіть ваше місце проживання", reply_markup=get_towns_list(towns))


@dp.message_handler(state=UserRegisterState.wait_town)
@session_decorator(add_param=False)
async def assign_user_to_town(msg: types.Message, state: FSMContext):
    user = await User.get(None, id=msg.from_user.id)
    town = await Town.get(None, name=msg.text)
    if not town:
        return await msg.answer("Нажаль цього міста нема в переліку, спробуйте обрати місто на клавіатурі внизу ще раз")
    await user.update(town_id=town.id)
    await msg.answer(f"Ми запам'ятали, де ви проживаєте", reply_markup=(await get_main_user_menu(town.id)))
    await state.finish()
