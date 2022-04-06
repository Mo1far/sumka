from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from sqlalchemy import select

from bot.core import dp
from bot.db.decorators import session_decorator
from bot.db.models import Town, User
from bot.kb.user import get_main_user_menu, get_towns_list
from bot.states.user import UserRegisterState

success_msg = """
🏫 Що працює в місті?
Тут інформація про те, де купити продукти, ліки, їжу для вашого котика, де заправити машину, зняти кошти та про інші відкриті заклади у вашому місті.
Якщо ви бажаєте додати інформацію, пишіть нам: @sumka_feedback_bot

🆘 Екстрена ситуація
Треба подзвонити в екстрені служби або знайти бот, куди скинути інформацію про пересування ворожої техніки? Цей розділ вам допоможе, він на варті вашої безпеки.

💟 Психологічна допомога
Почуття тривоги, невизначеності, страху у вас або у ваших близьких? Ми зробили добірку корисних ресурсів, які допоможуть як дорослим так і діткам. Турбуйтесь про себе, бо ви цього варті!

✅Офіційна інформація
Надто багато каналів в телеграмі і хтозна, де пишуть правду і кому вірити? Ця добірка містить лише офіційні перевірені джерела інформації, які захистять вас від дезінформації, фейків та пропаганди. Читайте лише перевірене.

🚙 Евакуація
Плануєте виїхати з міста або України? Шукаєте інформацію про безпечні маршрути та корисну інформацію про евакуацію? Сміливо користуйтесь цими посиланнями, які допоможуть вам спланувати безпечну евакуацію.

💙💛 Допомога
Хочете допомогти військовим? Здати кров? Шукаєте реквізити надійних організацій, щоб перерахувати кошти? Або ж вам потрібна гуманітарна допомога? Цей розділ буде корисним і тим, хто хоче допомогти і тим, хто потребує допомоги. Радимо «прогулятися» цим розділом, щоб краще познайомитися з ним.

📢 Тривога
Де той додаток, що сповіщає про сирену? Де безпечно ховатися під час тривоги? Що має бути у тривожній валізці? Цей розділ вміщує корисні поради: дій у разі хімічної атаки, втрати зв’язку та не тільки. Уся інформація зібрана спеціально для вас в цьому розділі.

💌 Зворотній зв’язок
Сподіваємося, що наш бот став для вас корисним помічником. Якщо у вас є пропозиції, що додати, змінити або ж поділитися враженнями від користування, то пишіть нам
"""


@dp.message_handler(commands=["start"], state="*")
@session_decorator(add_param=True)
async def start(current_session, msg: types.Message, state: FSMContext):
    user = await User.get(msg.from_user.id)

    if user:
        await msg.answer(
            "Ласкаво просимо", reply_markup=await get_main_user_menu(user.town_id)
        )
    else:
        await User.create(
            id=msg.from_user.id,
            name=msg.from_user.full_name,
            user_name=msg.from_user.username,
        )
        query = select(Town).order_by(Town.rating.desc(), Town.id)
        towns = (await current_session.execute(query)).scalars().all()

        await UserRegisterState.wait_town.set()
        await msg.answer(
            "Оберіть ваше місце проживання", reply_markup=get_towns_list(towns)
        )


@dp.message_handler(Text(equals="⚙ Змінити місце проживання"))
@session_decorator(add_param=True)
async def change_user_town(current_session, msg: types.Message, state: FSMContext):
    query = select(Town).order_by(Town.rating.desc(), Town.id)
    towns = (await current_session.execute(query)).scalars().all()

    # towns = await Town.get_list()
    await UserRegisterState.wait_town.set()
    await msg.answer(
        "Оберіть ваше місце проживання", reply_markup=get_towns_list(towns)
    )


@dp.message_handler(state=UserRegisterState.wait_town)
@session_decorator(add_param=False)
async def assign_user_to_town(msg: types.Message, state: FSMContext):
    user = await User.get(None, id=msg.from_user.id)
    town = await Town.get(None, name=msg.text)
    if not town:
        return await msg.answer(
            "Нажаль цього міста нема в переліку, спробуйте обрати місто на клавіатурі внизу ще раз"
        )
    await user.update(town_id=town.id)
    await msg.answer(success_msg, reply_markup=(await get_main_user_menu(town.id)))
    await state.finish()
