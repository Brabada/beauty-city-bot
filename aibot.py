import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from environs import Env
from telegram import KeyboardButton

env = Env()
env.read_env()
TOKEN=os.environ["TG_TOKEN"]

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class reg_states(StatesGroup):
    self_data = State()
    name = State()
    booking = State()
    saloon = State()
    service = State()
    master = State()
    schedule = State()
    date = State()
    time = State()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    booking_kb = types.KeyboardButton('Запись')
    profile_kb = types.KeyboardButton('Личный кабинет👤')
    keyboard.add(booking_kb, profile_kb)
    await bot.send_message(message.chat.id,
                           text='Добро пожаловать в BeautyCity, выберите интересующий вас раздел',
                           reply_markup=keyboard)

    await reg_states.booking.set()


@dp.message_handler(state=reg_states.booking)
async def reservation(message: types.Message):
    global booking_markup
    booking_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    booking_kb = types.KeyboardButton('Запись')
    profile_kb = types.KeyboardButton('Личный кабинет👤')
    booking_markup.add(booking_kb, profile_kb)
    if message.text == 'Запись':
        saloons_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        saloons = ['Vibe', 'Milane', 'Грусть', 'Lokon', 'Vibeu'] #TODO тут надо достать все салоны
        saloons_button = [types.KeyboardButton(f'{i}') for i in saloons]
        for _ in saloons_button:
            saloons_markup.add(_)
        await bot.send_message(message.chat.id,
                               f"Выберите салон:",
                               reply_markup=saloons_markup)
        await reg_states.saloon.set()

        await reg_states.service.set()

    if message.text == 'Личный кабинет👤':
        # TODO
        pass



@dp.message_handler(state=reg_states.service)
async def get_service(message: types.Message):
    schoosed_salon = message.text
    servises = ['Эпиляция', 'Солярий', 'наращивания ресниц', 'Маникюр'] #TODO тут надо достать все услуги из БД для выбранного салона
    servises_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    servises_button = [types.KeyboardButton(f'{i}') for i in servises]
    for _ in servises_button:
        servises_markup.add(_)
    await bot.send_message(message.chat.id,
                           f"В салоне {schoosed_salon} доступны следующие услугу:",
                           reply_markup=servises_markup)

    await reg_states.master.set()


@dp.message_handler(state=reg_states.master)
async def get_master(message: types.Message):
    schoosed_salon = '' #TODO как достать? почитать про FSMContext
    schoosed_service = message.text
    masters_button = ['Юлия Лахина', 'Виктория Хегай', 'Елизавета Невзорова'] #TODO тут надо достать всех мастеров салона(schoosed_salon) с соответ. услугой(schoosed_service)
    masters_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for _ in masters_button:
        masters_markup.add(_)
    await bot.send_message(message.chat.id,
                           f"Выберите мастера:",
                           reply_markup=masters_markup)

    await reg_states.date.set()


@dp.message_handler(state=reg_states.date)
async def get_date(message: types.Message):
    schoosed_master = message.text
    schedule_button = ['16 декабря', '17 декабря', '18 декабря', '19 декабря', '20 декабря'] #TODO достать доступные даты у мастера
    schedule_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for _ in schedule_button:
        schedule_markup.add(_)
    await bot.send_message(message.chat.id,
                           f"Выберите доступную дату у мастера {schoosed_master}:",
                           reply_markup=schedule_markup)

    await reg_states.time.set()


@dp.message_handler(state=reg_states.time)
async def get_time(message: types.Message):
    schoosed_master = '' #TODO как достать? почитать про FSMContext
    schedule_button = ['8:00-8:40', '8:50-9:30', '9:40-10:20', '10:35-11:15', '11:25-12:05'] #TODO достать доступное время у мастера
    schedule_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for _ in schedule_button:
        schedule_markup.add(_)
    await bot.send_message(message.chat.id,
                           f"Выберите доступное время у мастера {schoosed_master}:",
                           reply_markup=schedule_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)