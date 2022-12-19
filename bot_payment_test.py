import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from environs import Env


env = Env()
env.read_env()

bot_token = env.str('BOT_TOKEN', 'REPLACE_ME')
buy_token = env.str('PAYMENTS_TOKEN', 'REPLACE_ME')


# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# prices
PRICE = types.LabeledPrice(label="Стоимость одной услуги", amount=500*100)  # в копейках (руб)

# buy
@dp.message_handler(commands=['buy'])
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



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)