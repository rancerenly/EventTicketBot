from datetime import datetime, timedelta

import aiogram.utils.markdown as fmt
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from data import config
<<<<<<< Updated upstream
from handlers.users.show_all import test_events
=======
from keyboards.inline.keyboards import get_keyboard_use_event, get_keyboard_set_time
>>>>>>> Stashed changes

from loader import dp, scheduler
from utils.db_api import database


def schedule_job(user, event, notify_date):
    database.Notification.create(user=user, event=event, date=notify_date)
    scheduler.add_job(send_notify_event, "date",
                      run_date=notify_date, args=(dp,))



async def send_notify_event(dp: Dispatcher):
    await dp.bot.send_message(
        database.User.select(database.User.id == database.Notification.user),
        f"Уведомляю Вас о концерте {database.Notification.event}"
    )


<<<<<<< Updated upstream
def get_keyboard_use_event(event):
    # формирование кнопки покупки
    buttons = []
    for _ in test_events:
        if _["name"].__eq__(event):
            buttons = [types.InlineKeyboardButton(
                text=f"Купить билет на группу {_['name']}",
                url=_['linkToPay']),
                types.InlineKeyboardButton(
                    text="Поставить уведомления",
                    callback_data=f"set_notify_{_['name']}"
                )]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
    # окончание формирования кнопки покупки


def get_keyboard_set_time(event):

    buttons = [
        types.InlineKeyboardButton(
            text="За месяц",
            callback_data=f"time_30_{event}"),
        types.InlineKeyboardButton(
            text="За две недели",
            callback_data=f"time_14_{event}"),
        types.InlineKeyboardButton(
            text="За сутки",
            callback_data=f"time_1_{event}"
        ),
        types.InlineKeyboardButton(
            text="За восемь часов",
            callback_data=f"time_0_8_{event}"
        ),
        types.InlineKeyboardButton(
            text="За два часа",
            callback_data=f"time_0_2_{event}"
        )]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
=======
@dp.callback_query_handler(Text(startswith="time_"))
async def set_time_to_notify(call: types.CallbackQuery):
    time = call.data.split("_")[1]
    event_name = call.data.split("_")[2]
    event = database.Event.get(database.Event.name == event_name)
    notify_date = datetime.now() + timedelta(seconds=10)
    # notify_date = event.date - timedelta(int(time))
    schedule_job(call.from_user.id, event, notify_date)
    await call.message.answer(f"Уведомлю Вас о концерте {event.name} за {time} дней.")
    await call.answer()
>>>>>>> Stashed changes


@dp.callback_query_handler(Text(startswith="set_notify_"))
async def set_notify_event(call: types.CallbackQuery):
    event_name = call.data.split("_")[2]
    await call.message.answer("Когда Вам напомнить о концерте?",
                              reply_markup=get_keyboard_set_time(event_name))


@dp.callback_query_handler(Text(startswith="name_"))
async def send_info_event(call: types.CallbackQuery):
<<<<<<< Updated upstream
    event = call.data.split("_")[1]

    for _ in test_events:
        if _["name"].__eq__(event):
            await call.message.answer(
                f"""
{fmt.text(fmt.hbold(f"Концерт группы: #{_['name']}"))} 
{fmt.text(f"{_['place']} - {_['time']}.")}
{fmt.text(f"Ограничение: {fmt.hbold(_['age'])}+")}
{fmt.text(f"Цена: {fmt.hunderline(_['price'])} рублей")}
{_['description']}{fmt.hide_link(_['photo'])} """,
                parse_mode="HTML", disable_web_page_preview=False,
                reply_markup=get_keyboard_use_event(event)
            )
            break
=======
    event_name = call.data.split("_")[1]
    event = database.Event.get(database.Event.name == event_name)
    await call.message.answer(
        f"""
{fmt.text(fmt.hbold(f"Концерт группы: #{event.name}"))} 
{fmt.text(f"{event.place} - {event.date}.")}
{fmt.text(f"Ограничение: {fmt.hbold(event.age)}+")}
{fmt.text(f"Цена: {fmt.hunderline(event.price)} рублей")}
{event.description}
        {fmt.hide_link(event.photo)}""",
        parse_mode="HTML",
        reply_markup=get_keyboard_use_event(event_name),
    )
>>>>>>> Stashed changes
    await call.answer()


