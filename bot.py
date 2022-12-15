import telegram
import os
import logging
from environs import Env
from telegram import Update, ForceReply, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


env = Env()
env.read_env()
TOKEN=os.environ["TG_TOKEN"]
bot = telegram.Bot(token=TOKEN)


def start(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [['Запись', 'Личный кабинет👤']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Добро пожаловать в BeautyCity, выберите интересующий вас раздел",
                     reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def booking(update: Update, context: CallbackContext) -> None:
    if 'Запись' in update.message.text:
        saloons = ['Vibe', 'Milane', 'Грусть', 'Lokon'] #TODO тут необходимо из БД достать все салоны
        button = [[KeyboardButton(f'{i}')] for i in saloons]
        reply_markup = telegram.ReplyKeyboardMarkup(button)
        bot.send_message(chat_id=update.message.chat_id,
                     text="Выберите салон:",
                     reply_markup=reply_markup)

    if 'Личный кабинет' in update.message.text:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Тут будет данные из личного кабинета",
                         )


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text,  booking))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
