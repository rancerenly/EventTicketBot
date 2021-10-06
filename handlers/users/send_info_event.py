import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher.filters import Text

# временная мера, для проверки работоспособности бота
from handlers.users.show_all import test_events
from loader import dp


def get_keyboard_use_event(event):
    # формирование кнопки покупки
    buttons = []
    for _ in test_events:
        if _["name"].__eq__(event):
            buttons = [types.InlineKeyboardButton(
                text=f"Купить билет на группу {_['name']}",
                url=_['linkToPay']),
                types.InlineKeyboardButton(
                    text="Поставить уведомления",
                    callback_data=f"set_notify_{_['name']}"
                )]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
    # окончание формирования кнопки покупки


@dp.callback_query_handler(Text(startswith="set_notify_"))
async def set_notify_event(call: types.CallbackQuery):
    event = call.data.split("_")[2]
    await call.message.answer(event)


@dp.callback_query_handler(Text(startswith="event_"))
async def send_info_event(call: types.CallbackQuery):
    event = call.data.split("_")[1]

    for _ in test_events:
        if _["name"].__eq__(event):
            await call.message.answer(
                f"""
{fmt.text(fmt.hbold(f"Концерт группы: #{_['name']}"))} 
{fmt.text(f"{_['place']} - {_['time']}.")}
{fmt.text(f"Ограничение: {fmt.hbold(_['age'])}+")}
{fmt.text(f"Цена: {fmt.hunderline(_['price'])} рублей")}
{_['description']}{fmt.hide_link(_['photo'])} """,
                parse_mode="HTML", disable_web_page_preview=False,
                reply_markup=get_keyboard_use_event(event)
            )
            break
    await call.answer()
