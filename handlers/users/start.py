from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from BL.logic import create_user
from loader import dp
from utils.db_api import database


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    create_user(message.from_user.id)
    await message.answer(f"Привет, {message.from_user.full_name}!")



