from datetime import datetime, timedelta

import aiogram.utils.markdown as fmt
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

# временная мера, для проверки работоспособности бота
from data import config
from handlers.users.show_all import test_events

from loader import dp, scheduler


def schedule_job(date):
    scheduler.add_job(send_notify_event, "date",
                      run_date=date, args=(dp,))


async def send_notify_event(dp: Dispatcher):
    await dp.bot.send_message(
        config.ADMINS[0], "Сообщение по таймеру"
    )


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
            callback_data=f"time_1_{event}"
        ),
        types.InlineKeyboardButton(
            text="За восемь часов",
            callback_data=f"time_0_8_{event}"
        ),
        types.InlineKeyboardButton(
            text="За два часа",
            callback_data=f"time_0_2_{event}"
        )]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


@dp.callback_query_handler(Text(startswith="set_notify_"))
async def set_notify_event(call: types.CallbackQuery):
    date = ""
    event = call.data.split("_")[2]
    for _ in test_events:
        if _["name"].__eq__(event):
            date = datetime.strptime(_['time'], '%Y-%m-%d %H:%M:%S')
    await call.message.answer("Когда Вам напомнить о концерте?",
                              reply_markup=get_keyboard_set_time(event))


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


