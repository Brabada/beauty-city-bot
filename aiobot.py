import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.message import ContentType
from environs import Env


env = Env()
env.read_env()
TOKEN=os.environ['BOT_TOKEN']
buy_token = env.str('PAYMENTS_TOKEN', 'REPLACE_ME')

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# prices
PRICE = types.LabeledPrice(label="Стоимость одной услуги", amount=500*100)  # в копейках (руб)


class Visit:
    saloon_id = None
    service_id = None
    day_id = None
    
class User:
    chat_id = None
    phone = None


def get_saloons():
    saloons = [{'id': 1, 'name': 'Vibe', 'address': '12345'},
               {'id': 2, 'name': 'Milane', 'address': '12345'},
               {'id': 3, 'name': 'Грусть', 'address': '12345'}, ]
    return saloons

def get_services():
    services = [
        {'id': 1, 'name': 'Ногти'},
        {'id': 2, 'name': 'Волосы'},
        {'id': 3, 'name': 'Брови'}
    ]
    return services


def get_days():
    days = [
        {'id': 1, 'date': '19.12.2022'},
        {'id': 2, 'date': '20.12.2022'},
        {'id': 3, 'date': '21.12.2022'}
    ]
    return days


def get_masters():

    masters = [
        {'id': 1, 'name': 'Ольга',
         'dates': [
             {'date': '19.12.2022', 'saloon_id': 1, 'times': [
                 {'id': 1, 'time_interval': '10:00-11:00', 'busy': True},
                 {'id': 2, 'time_interval': '11:00-12:00', 'busy': True}]},
             {'date': '20.12.2022', 'saloon_id': 2}],
         'services': [1, 2, 3]},
        {'id': 2, 'name': 'Полина',
         'dates': [
             {'date': '19.12.2022', 'saloon_id': 1, 'times': [
                 {'id':1, 'time_interval': '10:00-11:00', 'busy': False},
                 {'id':2, 'time_interval': '11:00-12:00', 'busy': True}]},
                   {'date': '20.12.2022', 'saloon_id': 2}],
         'services': [1, 2, 3]},
        {'id': 3, 'name': 'Юлия',
         'dates': [{'date': '19.12.2022', 'saloon_id': 1},
                   {'date': '20.12.2022', 'saloon_id': 2}],
         'services': [1, 2, 3]}

    ]

    return masters


def get_user(chat_id):
    # Todo if we know him, continue, else initiate new
    user = User()
    user.visit = Visit()
    return user


class RegStates(StatesGroup):
    main_menu = State()

    saloons = State()
    services = State()
    days = State()
    masters = State()
    times = State()

    schedule = State()
    date = State()
    time = State()
    self_data = State()
    name = State()
    payment = State()
    phone = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('start handler')
    print(message.from_user.id)
    user = get_user(message.from_user.id)
    # user.visit = Visit()
    # user

    global main_menu_markup
    main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    booking_kb = types.KeyboardButton('Записаться🗓')
    profile_kb = types.KeyboardButton('Личный кабинет👤')
    main_menu_markup.add(booking_kb, profile_kb)
    await bot.send_message(message.chat.id,
                           text='Добро пожаловать в BeautyCity, выберите интересующий вас раздел',
                           reply_markup=main_menu_markup)

    await RegStates.main_menu.set()


@dp.message_handler(state=RegStates.main_menu)
async def main_menu(message: types.Message, state: FSMContext):
    print('main menu handler')

    go_to_main_menu = types.KeyboardButton("Главное меню📚")

    if message.text == 'Записаться🗓':
        saloons_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        saloons = get_saloons()

        saloons_buttons = [types.KeyboardButton(i['name']) for i in saloons]

        saloons_markup.add(go_to_main_menu).row(*saloons_buttons)
        await bot.send_message(message.chat.id,
                               f"Выберите салон:",
                               reply_markup=saloons_markup)
        await RegStates.saloons.set()


@dp.message_handler(state=RegStates.saloons)
async def select_salon(message: types.Message):
    print('select salon handler')
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Хотите стать еще красивее?",
                               reply_markup=main_menu_markup)

        await RegStates.main_menu.set()

    saloons = get_saloons()

    for saloon in saloons:
        if message.text == saloon['name']:
            Visit.saloon_id = saloon['id']

    print(Visit.saloon_id)

    if message.text:
        services_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        services = get_services()
        services_button = [types.KeyboardButton(i['name']) for i in services]

        services_markup.add(go_to_main_menu).row(*services_button)

        await bot.send_message(message.chat.id,
                         f"Выберите салон:",
                         reply_markup=services_markup)
        await RegStates.services.set()


@dp.message_handler(state=RegStates.services)
async def select_service(message: types.Message):
    print('select services handler')
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Хотите стать еще красивее?",
                               reply_markup=main_menu_markup)

        await RegStates.main_menu.set()

    services = get_services()

    print(Visit.saloon_id)
    for service in services:
        if message.text == service['name']:
            Visit.service_id = service['id']
    print(Visit.service_id)

    if message.text:
        days_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        days = get_days()
        days_buttons = [types.KeyboardButton(i['date']) for i in days]

        days_markup.add(go_to_main_menu).row(*days_buttons)

        await bot.send_message(message.chat.id,
                         f"Выберите салон:",
                         reply_markup=days_markup)
        await RegStates.days.set()


@dp.message_handler(state=RegStates.days)
async def select_day(message: types.Message):
    print('select days handler')
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Хотите стать еще красивее?",
                               reply_markup=main_menu_markup)

        await RegStates.main_menu.set()

    days = get_days()
    for day in days:
        if message.text == day['date']:
            Visit.day_date = day['date']

    print(Visit.saloon_id)
    print(Visit.service_id)
    print(Visit.day_date)

    if message.text:
        masters_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        masters = get_masters()
        masters_buttons = [types.KeyboardButton(i['name']) for i in masters]

        masters_markup.add(go_to_main_menu).row(*masters_buttons)

        await bot.send_message(message.chat.id,
                         f"Выберите салон:",
                         reply_markup=masters_markup)
        await RegStates.masters.set()


@dp.message_handler(state=RegStates.masters)
async def select_master(message: types.Message):
    print('select masters handler')
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Хотите стать еще красивее?",
                               reply_markup=main_menu_markup)

        await RegStates.main_menu.set()

    masters = get_masters()
    for master in masters:
        if message.text == master['name']:
            Visit.master_id = master['id']

    print(Visit.saloon_id)
    print(Visit.service_id)
    print(Visit.day_date)
    print(Visit.master_id)

    if message.text:
        times_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        masters = get_masters()
        times = []
        for master in masters:
            if master['id'] == Visit.master_id:
                for date in master['dates']:
                    print(date['date'])
                    print(Visit.day_date)
                    if date['date'] == Visit.day_date:
                        times = date['times']


        times_buttons = [types.KeyboardButton(i['time_interval']) for i in times]

        times_markup.add(go_to_main_menu).row(*times_buttons)

        await bot.send_message(message.chat.id,
                         f"Выберите салон:",
                         reply_markup=times_markup)
        await RegStates.times.set()


@dp.message_handler(state=RegStates.times)
async def register_user(message: types.Message):
    print('select times handler')
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Хотите стать еще красивее?",
                               reply_markup=main_menu_markup)

        await RegStates.main_menu.set()

    # Todo new user register
    if True:
        global self_data_markup
        self_data_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes_button = types.KeyboardButton("Соглашаюсь")
        no_button = types.KeyboardButton("Не соглашаюсь")
        self_data_markup.add(yes_button, no_button)
        await bot.send_message(message.chat.id,
                                f"Здравствуйте, вы даёте соглашение на обработку персональных данных?",
                               reply_markup=self_data_markup)
        await RegStates.self_data.set()
    # Todo old user process to pay
    else:
        pass

@dp.message_handler(state=RegStates.self_data)
async def get_permission(message: types.Message):
    if message.text == "Соглашаюсь":
        name_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        use_tg_first_name = types.KeyboardButton("Имя из телеграма")
        name_markup.add(use_tg_first_name)
        await bot.send_message(message.chat.id,
                           "Как вы хотите чтобы к вам обращались? Нажмите на кнопку или введите ваше имя.",
                           reply_markup=name_markup)
        await RegStates.name.set()
    if message.text == "Не соглашаюсь":
        await bot.send_message(message.chat.id,
                               "Для продолжения вы должны дать согласие.",
                               reply_markup=self_data_markup)


@dp.message_handler(state=RegStates.name)
async def get_name(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    use_tg_phone = types.KeyboardButton("Номер из телеграма", request_contact=True)
    markup.add(use_tg_phone)
    if message.chat.type == 'private':
        if message.text == "Имя из телеграма":
            user_name = message.from_user.first_name
        else:
            user_name = message.text
        await state.update_data(name=user_name)
        await bot.send_message(message.chat.id,
                               f"Хорошо, {user_name}, теперь нажмите на кнопку, или введите свой телефон.",
                               reply_markup=markup)
        await RegStates.phone.set()


@dp.message_handler(state=RegStates.phone, content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as user:
        if message.chat.type == 'private':
            if message.contact is not None:
                user['phone'] = message.contact.phone_number
            else:
                user['phone'] = message.text

        payment_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        pay_button = types.KeyboardButton("Оплатить")

        payment_markup.add(go_to_main_menu).row(pay_button)

        await bot.send_message(message.chat.id,
                         f"Выберите салон:",
                         reply_markup=payment_markup)
        await RegStates.payment.set()


@dp.message_handler(state=RegStates.payment)
async def buy(message: types.Message):
    if buy_token.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Оплата услуги",
                           description="Услуга: Наращивание ресниц \ Салон: Восхищение, Тверская-ямская 15 \ Мастер: Мастер Шифу \ Время: 20 декабря 2022 18:30",
                           provider_token=buy_token,
                           currency="rub",
                           photo_url="https://i.ytimg.com/vi/aSPYIVN075M/maxresdefault.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")



def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def main():
    print("Бот Запущен")
    loop = get_or_create_eventloop()
    executor.start_polling(dp, loop=loop)


if __name__ == '__main__':
    main()