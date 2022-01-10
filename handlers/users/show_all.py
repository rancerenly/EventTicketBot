import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher.filters import Text
from peewee import SqliteDatabase

from BL.logic import events_name, get_genres, search_events_by_genre, genre_name
from data import config
from utils.db_api import database
from loader import dp


def get_keyboard_events():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for event in events_name():
        keyboard.add(
            types.InlineKeyboardButton(
                text=event[1],
                callback_data=f"name_{event[0]}"
            )
        )
    return keyboard


def get_keyboard_genres():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for genre in get_genres():
        keyboard.add(types.InlineKeyboardButton(
            text=genre[1],
            callback_data=f"genre_{genre[0]}"
            )
        )
    return keyboard


def get_keyboard_events_by_genre(genre_id):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    events = search_events_by_genre(genre_id)
    if not events.__eq__([]):
        for event in events:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=event[1],
                    callback_data=f"name_{event[0]}"
                )
            )
        return keyboard
    else:
        return None


@dp.message_handler(commands="show_all")
async def show_all(message: types.Message):
    await message.answer(
        "Выберите интересующее Вас мероприятие",
        reply_markup=get_keyboard_events())


@dp.callback_query_handler(Text(startswith='genre_'))
async def send_events_by_genre(call: types.CallbackQuery):
    genre_id = call.data.split("_")[1]
    keyboard = get_keyboard_events_by_genre(genre_id)
    if keyboard is None:
        await call.message.answer(f"Мероприятий по выбранному жанру не нашлось. Посмотрите другие жанры",
                                  reply_markup=get_keyboard_genres())
    else:
        await call.message.answer(f'Меропрития по жанру: {genre_name(genre_id)}',
                                  reply_markup=keyboard)
    await call.answer()


@dp.message_handler(commands="show_by_genre")
async def show_by_genre(message: types.Message):
    await message.answer("Выберите интересующий Вас жанр",
                         reply_markup=get_keyboard_genres())




