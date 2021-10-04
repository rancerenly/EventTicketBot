import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp

shit_event = {
    'id': 1,
    'name': 'ssshhhiiittt',
    'place': 'The Mods Bar',
    'time': '28 ноября, воскресенье, 20:00',
    'price': 900.0,
    'linkToPay': 'https://afisha.yandex.ru/krasnoyarsk/concert/ssshhhiiittt-2021-11-28',
    'age': 16,
    'photo': 'https://sun9-81.userapi.com/impg/hyE5GXpEE9sNCOVA6uno4qltTUMm1I3kQUPLGA/5VDhx1ZqG6k.jpg?size=604x604&quality=96&sign=f75973e769db46cb85b43a162a54020b&type=album',
    'description':
        """ssshhhiiittt! — это музыка внутренних терзаний и разочарований в самом себе.
Благодаря цепким мелодиям и понятным каждому текстам, группа моментально стала одним из главных
явлений на отечественной сцене, расширяя с каждым днем географию своих слушателей.
Группа сыграет специальный сет, исполнит новый альбом и все самые важные песни."""}
LSP_event = {
    'id': 2,
    'name': 'ЛСП',
    'place': 'Circus Concert Hall',
    'time': '28 ноября, воскресенье, 20:00',
    'price': 1100.0,
    'linkToPay': 'https://afisha.yandex.ru/krasnoyarsk/concert/lsp-2021-11-22?source=event',
    'age': 16,
    'photo': 'https://a2.fm/system/event/poster_image/134/5.jpg',
    'description': 'Madstream Booking представляет: каравелла любви снова бороздит необъятные просторы России!'
}

test_events = [shit_event, LSP_event]


def get_keyboard_events():
    # Генерация клавиатуры
    buttons = []
    for event in test_events:
        buttons.append(types.InlineKeyboardButton(
            text=f"{event['name']}",
            callback_data=f"event_{event['name']}"
        ))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands="show_all")
async def show_all(message: types.Message):
    await message.answer(
        "Выберите интересующий Вас концерт",
        reply_markup=get_keyboard_events())


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
{_['description']}{fmt.hide_link(_['photo'])}
{fmt.hlink("Купить билет прямо сейчас", _['linkToPay'])}""",
                parse_mode="HTML", disable_web_page_preview=False
            )
            break
    await call.answer()
