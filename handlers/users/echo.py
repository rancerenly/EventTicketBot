from aiogram import types
from aiogram.dispatcher import FSMContext
import sqlite3
from loader import dp


# @dp.message_handler(commands="print")
# async def bot_echadso(message: types.Message):
#     conn = sqlite3.connect('D:\\DB\events.db', check_same_thread=False)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM event")
#     data = cursor.fetchall()
#     print(data[0][7])
#     await message.reply_photo(photo=open(data[0][7], 'rb'))



# # Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# @dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state = await state.get_state()
#     await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
#                          f"\nСодержание сообщения:\n"
#                          f"<code>{message}</code>")
#
#

