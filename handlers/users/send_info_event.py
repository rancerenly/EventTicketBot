from datetime import datetime, timedelta

import aiogram.utils.markdown as fmt
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from data import config

from keyboards.inline.keyboards import get_keyboard_use_event, get_keyboard_set_time

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


@dp.callback_query_handler(Text(startswith="set_notify_"))
async def set_notify_event(call: types.CallbackQuery):
    event_name = call.data.split("_")[2]
    await call.message.answer("Когда Вам напомнить о концерте?",
                              reply_markup=get_keyboard_set_time(event_name))


@dp.callback_query_handler(Text(startswith="name_"))
async def send_info_event(call: types.CallbackQuery):
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
    await call.answer()


