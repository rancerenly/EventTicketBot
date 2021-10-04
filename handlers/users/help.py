from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp


@dp.message_handler(CommandHelp(), user_id=ADMINS)
async def bot_help_admin(message: types.Message):
    text = ("Список команд админа: ",
            "/admin_command")
    await message.answer("\n".join(text))


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/show_all - Вывести все концерты")
    await message.answer("\n".join(text))


