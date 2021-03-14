#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import pickle

from typing import Dict

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Nombre','Age', 'Color favorito'],
    ['Number of siblings', 'Something else...'],
    ['Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def cargar_datos():
    try:
        with open("traducciones.dat", "rb") as f:
            return pickle.load(f)
    except (OSError, IOError) as e:
        return dict()


def guardar_datos(dic):
    with open("traducciones.dat", "wb") as f:
        pickle.dump(dic, f)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "!Bienvenido! Esto es SkytravelApp"
        "¿Que puedo hacer por ti?",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Tu {text.lower()}? Sí, me encantaría escuchar eso!.')

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Muy bien, por favor, envíenme primero la categoría,' 'por ejemplo "La habilidad más impresionante"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    dic = cargar_datos()
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    
    logger.info("Esto es User_data adentro de dict: %s", facts_to_str(user_data))
    logger.info("Esto es User_data no se por que no funciona")
    guardar_datos(user_data)
    
    update.message.reply_text(
        "¡Genial! Para que sepas, esto es lo que ya me has dicho:"
        f"{facts_to_str(user_data)} Puedes decirme más, o cambiar tu opinión"
        " Sobre algo.",
        reply_markup=markup,
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"Me he enterado de estos datos sobre ti: {facts_to_str(user_data)} ¡Hasta la próxima vez!"
    )

    user_data.clear()
    return ConversationHandler.END





def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1595242339:AAFfNxwj3JB108952Oo1jO6VcKmKpYIDURk")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Nombre|Age|Color favorito|Number of siblings)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Something else...$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()


    updater.idle()


if __name__ == '__main__':
    main()