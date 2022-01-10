from datetime import datetime, timedelta

import aiogram.utils.markdown as fmt
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from BL.logic import search_event_by_id, notify_day
from data import config

from keyboards.inline.keyboards import get_keyboard_use_event, get_keyboard_set_time

from loader import dp, scheduler
from utils.db_api import database
from utils.misc import logging


def schedule_job(user, event, notify_date):
    database.Notification.create(user=user, event=event, date=notify_date)
    scheduler.add_job(send_notify_event, "date",
                      run_date=notify_date, args=(dp,))


async def send_notify_event(dp: Dispatcher):
    notifications = database.Notification.select(
        database.Notification.user, database.Notification.date,
        database.Notification.event
    ).where(
        database.Notification.date.day == datetime.today().day
    )
    for _ in notifications:
        event = database.Event.get(id=_.event_id)
        try:
            await dp.bot.send_message(
                _.user_id, f"Уведомляю Вас о концерте {event.name}\nДо мероприятия осталось "
                           f"{event.date.day - datetime.now().day} дней."
            )
        except Exception as err:
            pass
    database.Notification.delete().where(
        database.Notification.date.day == datetime.today().day
    ).execute()


@dp.callback_query_handler(Text(startswith="time_"))
async def set_time_to_notify(call: types.CallbackQuery):
    time = call.data.split("_")[1]
    event_id = call.data.split("_")[2]
    event = search_event_by_id(event_id)
    notify_date = notify_day(event.date, time)
    print(timedelta(microseconds=datetime.now().microsecond))
    schedule_job(call.from_user.id, event, notify_date)
    await call.message.answer(f"Уведомлю Вас о мероприятии {event.name} за {time} дней.")
    await call.answer()


@dp.callback_query_handler(Text(startswith="set_notify_"))
async def set_notify_event(call: types.CallbackQuery):
    event_name = call.data.split("_")[2]
    await call.message.answer("Когда Вам напомнить о концерте?",
                              reply_markup=get_keyboard_set_time(event_name))


@dp.callback_query_handler(Text(startswith="name_"))
async def send_info_event(call: types.CallbackQuery):
    event_id = call.data.split("_")[1]
    event = search_event_by_id(event_id)
    await call.message.answer(
        f"""
{fmt.text(fmt.hbold(f"Мероприятие: {event.name}"))} 
{fmt.text(f"{event.place} - {event.date}.")}
{fmt.text(f"Ограничение: {fmt.hbold(event.age)}+")}
{fmt.text(f"Цена: {fmt.hunderline(event.price)} рублей")}
{event.description} {fmt.hide_link(event.photo)} """,
        reply_markup=get_keyboard_use_event(event.id),
        parse_mode="HTML"
    )
    await call.answer()

