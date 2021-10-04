from aiogram import types

from loader import dp
from data.config import ADMINS


@dp.message_handler(user_id=ADMINS, commands="admin_command")
async def admin_cmd_hi(message: types.Message):
    await message.reply(f"Привет Админ, {message.from_user.full_name}!")