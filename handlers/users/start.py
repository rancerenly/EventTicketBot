from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api import database


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    database.User.create(id=message.from_user.id,
                         city=1, genre=1)
    await message.answer(f"Привет, {message.from_user.full_name}!")



