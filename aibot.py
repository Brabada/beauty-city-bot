import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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
    service = State()
    personal_cab = State()
    saloon = State()
    like_dislike = State()
    rand_new_recipe = State()


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
async def booking(message: types.Message):
    global booking_markup
    booking_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    booking_kb = types.KeyboardButton('Запись')
    profile_kb = types.KeyboardButton('Личный кабинет👤')
    booking_markup.add(booking_kb, profile_kb)
    if message.text == 'Запись':
        saloons_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        saloons = ['Vibe', 'Milane', 'Грусть', 'Lokon'] #TODO тут надо достать все салоны
        saloons_button = [types.KeyboardButton(f'{i}') for i in saloons]
        for _ in saloons_button:
            saloons_markup.add(_)
        await bot.send_message(message.chat.id,
                               f"Выберите салон",
                               reply_markup=saloons_markup)
        await reg_states.saloon.set()

        await reg_states.service.set()


@dp.message_handler(state=reg_states.service)
async def service(message: types.Message):
    schoosed_salon = message.text
    servises = ['Эпиляция', 'Солярий', 'наращивания ресниц', 'Маникюр'] #TODO тут надо достать все услуги из БД для выбранного салона
    servises_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    servises_button = [types.KeyboardButton(f'{i}') for i in servises]
    for _ in servises_button:
        servises_markup.add(_)
    await bot.send_message(message.chat.id,
                           f"Выберите услугу",
                           reply_markup=servises_markup)

    await reg_states.service.set()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)