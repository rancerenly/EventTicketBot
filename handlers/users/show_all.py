import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher.filters import Text
from peewee import SqliteDatabase

from data import config
from utils.db_api import database
from loader import dp


def get_keyboard_events():
    # Генерация клавиатуры
    buttons = []
    for event in database.Event.select():
        buttons.append(types.InlineKeyboardButton(
            text=event.name,
            callback_data=f"name_{event.name}"
        ))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands="show_all")
async def show_all(message: types.Message):
    await message.answer(
        "Выберите интересующий Вас концерт",
        reply_markup=get_keyboard_events())



