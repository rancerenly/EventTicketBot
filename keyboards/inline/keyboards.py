from aiogram import types

from utils.db_api import database


def get_keyboard_use_event(event_name):
    event = database.Event.get(database.Event.name == event_name)
    buttons = [types.InlineKeyboardButton(
        text=f"Купить билет на группу {event.name}",
        url=event.link), types.InlineKeyboardButton(
        text="Поставить уведомления",
        callback_data=f"set_notify_{event.name}"
    )]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


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
            callback_data=f"time_1_{event}")]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard