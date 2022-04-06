from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.core import bot, dp
from bot.db.decorators import session_decorator
from bot.db.models import Town, User
from bot.filters.admin import IsSuperAdmin
from bot.kb.admin import get_towns_for_mailing, mailing_callback
from bot.states.admin import MailingState


@dp.callback_query_handler(
    IsSuperAdmin(), mailing_callback.filter(action="start"), state="*"
)
async def mailing_start(cq: types.CallbackQuery):
    await MailingState.add_text.set()
    await cq.answer()
    await cq.message.answer("Введіть текст")


@dp.message_handler(IsSuperAdmin(), state=MailingState.add_text)
@session_decorator()
async def mailing_add_town(msg: types.Message, state: FSMContext):
    await state.set_data({"text": msg.text})

    towns = await Town.get_list()
    kb = get_towns_for_mailing(towns)
    await MailingState.add_town.set()

    await msg.answer("Оберіть місто", reply_markup=kb)


@dp.callback_query_handler(
    IsSuperAdmin(),
    mailing_callback.filter(action="assing_town"),
    state=MailingState.add_town,
)
@session_decorator()
async def mailing_start(
    cq: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    town_id = int(callback_data.get("town_id"))
    if town_id:
        users = await User.get_list(town_id=town_id)
    else:
        users = await User.get_list()

    await cq.answer(f"Почали розсилку на {len(users)} юзера")
    text = (await state.get_data())["text"]
    count = 0
    await state.finish()
    for user in users:
        try:
            await bot.send_message(user.id, text)
            count += 1
        except Exception as e:
            pass

    await cq.message.answer(f"Надіслано {count} повідомлень")
