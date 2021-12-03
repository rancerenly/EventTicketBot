import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher.filters import Text
from peewee import SqliteDatabase

from BL.logic import events_name
from data import config
from utils.db_api import database
from loader import dp


def get_keyboard_events():
    # Генерация клавиатуры
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for event in events_name():
        keyboard.add(
            types.InlineKeyboardButton(
                text=event[1],
                callback_data=f"name_{event[0]}"
            )
        )
    return keyboard


@dp.message_handler(commands="show_all")
async def show_all(message: types.Message):
    await message.answer(
        "Выберите интересующее Вас мероприятие",
        reply_markup=get_keyboard_events())



