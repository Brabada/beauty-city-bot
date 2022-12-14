import telegram
import os
import logging
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


load_dotenv()
TOKEN=os.environ["TG_TOKEN"]
bot = telegram.Bot(token=TOKEN)


def start(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [['Запись', 'Личный кабинет👤']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Custom Keyboard Test",
                     reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()