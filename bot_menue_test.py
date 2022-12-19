import logging
from datetime import datetime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from environs import Env
import asyncio


env = Env()
env.read_env()
logging.basicConfig(level=logging.INFO)

bot_token = env.str('BOT_TOKEN', 'REPLACE_ME')
buy_token = env.str('PAYMENTS_TOKEN', 'REPLACE_ME')

bot = Bot(bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

class Visit:
    day = None
    saloon = None
    master = None
    service = None

class RegStates(StatesGroup):
    main_menu = State()
    new_visit = State()

    self_data = State()
    name = State()
    phone = State()

    personal_cab = State()

    like_dislike = State()
    rand_new_recipe = State()


def get_saloons():
    saloons = [{'id': 1, 'name': "Pleasure", 'address': "За углом на лево"},
               {'id': 2, 'name': "Joy", 'address': "За углом на лево"},
               {'id': 3, 'name': "Honey", 'address': "За углом на лево"}]
    return saloons


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sign_for_visit = types.KeyboardButton("Записаться🧾")
    pers_cab_button = types.KeyboardButton("Личный кабинет👤")
    markup.add(sign_for_visit, pers_cab_button)
    await bot.send_message(message.chat.id,
                           f"Хотите стать еще красивее?",
                           reply_markup=markup)
    await RegStates.main_menu.set()


@dp.message_handler(state=RegStates.main_menu)
async def main_menu(message: types.Message, state: FSMContext):
    main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sign_for_visit = types.KeyboardButton("Записаться🧾")
    pers_cab_button = types.KeyboardButton("Личный кабинет👤")
    main_menu_markup.add(sign_for_visit, pers_cab_button)
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Хотите стать еще красивее?",
                               reply_markup=main_menu_markup)
    if message.text == "Записаться🧾":
        new_visit_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


        buttons = [types.KeyboardButton("В салон🏠"),
                   types.KeyboardButton("На дату📅"),
                   types.KeyboardButton("К мастеру🙋")]

        for i in range(500):
            buttons.append(types.KeyboardButton(str(i)))
        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        new_visit_markup.add(*buttons).row(go_to_main_menu)

        await bot.send_message(message.chat.id,
                                 f"Записаться",
                                 reply_markup=new_visit_markup)
        await RegStates.new_visit.set()


        # new_visit_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #
        # saloons = get_saloons()
        # for saloon in saloons:
        #     print(saloon['id'])
        #
        # rand_recipe_button = types.KeyboardButton("Любой🍽")
        # nongluten_recipe_button = types.KeyboardButton("Безглютеновый🍪")
        # vegetarian_recipe_button = types.KeyboardButton("Вегетарианский🥗")
        # nonlactose_recipe_button = types.KeyboardButton("Безлактозный🍰")
        # go_to_main_menu = types.KeyboardButton("Главное меню📚")
        # new_visit_markup.add(vegetarian_recipe_button, nongluten_recipe_button,
        #                       nonlactose_recipe_button).row(rand_recipe_button).row(go_to_main_menu)
        # await bot.send_message(message.chat.id,
        #                        f"Выберете салон",
        #                        reply_markup=new_visit_markup)
        # await RegStates.new_visit.set()


@dp.message_handler(state=RegStates.new_visit)
async def new_visit(message: types.Message):
    main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sign_for_visit = types.KeyboardButton("Записаться🧾")
    pers_cab_button = types.KeyboardButton("Личный кабинет👤")
    main_menu_markup.add(sign_for_visit, pers_cab_button)
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                         f"Хотите стать еще красивее?",
                         reply_markup=main_menu_markup)
        await RegStates.main_menu.set()

    # if message.text == "В салон🏠":



    # "В салон🏠"),
    # types.KeyboardButton("На дату📅"),
    # types.KeyboardButton("К мастеру🙋"


    # global like_dislike_markup
    # like_dislike_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # like_button = types.KeyboardButton("Сохранить❤")
    # dislike_button = types.KeyboardButton("Больше не показывать👎")
    # go_to_main_menu = types.KeyboardButton("Главное меню📚")
    # like_dislike_markup.row(like_button, dislike_button).add(go_to_main_menu)
    # if message.text == "Любой🍽":
    #     global rand_dish
    #     rand_dish = Dish.objects.order_by('?').first()
    #     user_dish = UserDish.objects.filter(dish=rand_dish, user=message.from_user.id, disliked=True).first()
    #     if user_dish is not None:
    #         rand_dish = Dish.objects.order_by('?').first()
    #     dish_ingredients = DishProduct.objects.filter(dish=rand_dish)
    #     dish_steps = DishStep.objects.all().filter(dish=rand_dish)
    #     await bot.send_message(message.chat.id,
    #                            f"Вот ваше блюдо:\n"
    #                            f"{rand_dish.title}\n",
    #                            reply_markup=like_dislike_markup)
    #     with open(pic_download(rand_dish.picture), 'rb') as file:
    #         await bot.send_photo(message.chat.id,
    #                              file)
    #     if rand_dish.description is not None:
    #         await bot.send_message(message.chat.id,
    #                             f"{rand_dish.description}")
    #
    #     await bot.send_message(message.chat.id,
    #                            f"Ингредиенты:")
    #
    #     for dish_ingredient in dish_ingredients:
    #         await bot.send_message(message.chat.id,
    #                                f"{dish_ingredient.product}{dish_ingredient.amount}\n")
    #
    #     await bot.send_message(message.chat.id,
    #                            "Инструкция по приготовлению:")
    #     for dish_step in dish_steps:
    #         if dish_step.picture:
    #             await bot.send_message(message.chat.id,
    #                                    f"{dish_step.order}. {dish_step.description}")
    #             with open(pic_download(dish_step.picture), 'rb') as file:
    #                 await bot.send_photo(message.chat.id,
    #                                      file)
    #         else:
    #             await bot.send_message(message.chat.id,
    #                                    f"{dish_step.order}. {dish_step.description}")
    #     await reg_states.rand_new_recipe.set()
    #
    # if message.text == "Безглютеновый🍪":
    #     tag = 3
    #     await show_recipe(message, tag)
    #
    # if message.text == "Вегетарианский🥗":
    #     tag = 2
    #     await show_recipe(message, tag)
    #
    # if message.text == "Безлактозный🍰":
    #     tag = 1
    #     await show_recipe(message, tag)



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


if __name__ == "__main__":
    main()
