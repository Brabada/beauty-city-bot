import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from environs import Env


env = Env()
env.read_env()
TOKEN=os.environ['BOT_TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Visit:
    saloon_id = None
    service_id = None
    day_id = None


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


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('start handler')
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


# @dp.message_handler(state=reg_states.service)
# async def get_service(message: types.Message):
#     schoosed_salon = message.text
#     servises = ['Эпиляция', 'Солярий', 'наращивания ресниц', 'Маникюр'] #TODO тут надо достать все услуги из БД для выбранного салона
#     servises_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     servises_button = [types.KeyboardButton(f'{i}') for i in servises]
#     for _ in servises_button:
#         servises_markup.add(_)
#     await bot.send_message(message.chat.id,
#                            f"В салоне {schoosed_salon} доступны следующие услугу:",
#                            reply_markup=servises_markup)
#     await reg_states.master.set()
#
#
# @dp.message_handler(state=reg_states.master)
# async def get_master(message: types.Message):
#     schoosed_salon = '' #TODO как достать? почитать про FSMContext
#     schoosed_service = message.text
#     masters_button = ['Юлия Лахина', 'Виктория Хегай', 'Елизавета Невзорова'] #TODO тут надо достать всех мастеров салона(schoosed_salon) с соответ. услугой(schoosed_service)
#     masters_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for _ in masters_button:
#         masters_markup.add(_)
#     await bot.send_message(message.chat.id,
#                            f"Выберите мастера:",
#                            reply_markup=masters_markup)
#
#     await reg_states.date.set()
#
#
# @dp.message_handler(state=reg_states.date)
# async def get_date(message: types.Message):
#     schoosed_master = message.text
#     schedule_button = ['16 декабря', '17 декабря', '18 декабря', '19 декабря', '20 декабря'] #TODO достать доступные даты у мастера
#     schedule_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for _ in schedule_button:
#         schedule_markup.add(_)
#     await bot.send_message(message.chat.id,
#                            f"Выберите доступную дату у мастера {schoosed_master}:",
#                            reply_markup=schedule_markup)
#
#     await reg_states.time.set()
#
#
# @dp.message_handler(state=reg_states.time)
# async def get_time(message: types.Message):
#     schoosed_master = '' #TODO как достать? почитать про FSMContext
#     schedule_button = ['8:00-8:40', '8:50-9:30', '9:40-10:20', '10:35-11:15', '11:25-12:05'] #TODO достать доступное время у мастера
#     schedule_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for _ in schedule_button:
#         schedule_markup.add(_)
#     await bot.send_message(message.chat.id,
#                            f"Выберите доступное время у мастера {schoosed_master}:",
#                            reply_markup=schedule_markup)


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