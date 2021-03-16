
import logging
import numpy as np

from helper import gsheet_helper
from cfg import TOKEN    

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

gsconn = gsheet_helper()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Nombre','Age', 'Color favorito','Listado'],
    ['Number of siblings', 'Buscar'],
    ['start','Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)




def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    name = update.message.from_user.username
    update.message.reply_text(
        f"!Bienvenido {name}! Esto es SkytravelApp\n"
        "¿Que puedo hacer por ti?",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Buscaremos coincidencias con {text.lower()} en los campos mencionados anteriormente.')

    return TYPING_REPLY

def buscar_choice(update: Update, context: CallbackContext) -> int:
    logger.info("Ingresamos a buscar choice")
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Buscaremos coincidencias con {text.lower()} en los campos mencionados anteriormente.')

    vuelos = gsconn.Buscar(text)
    logger.info("Se realizo el Buscar(text)")
    df = vuelos[0]
    x = vuelos[1]
    update.message.reply_text(f"{df}",reply_markup=markup)
    #df,x
    logger.info(f"comprobando df:{df}")
    logger.info(f"comprobando x:{x}")
    return TYPING_REPLY



def custom_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        '¿Deseas Buscar? No hay problema!, ' 'Puedes buscar ingresando alguno de los siguientes datos:\nPais de Destino/Origen, código IATA, Nombre de Aeropuerto y Ciudad o País \nRecuerda solo ingresar uno de estos datos por búsqueda.'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    logger.info("Esto es User_data adentro de dict: %s", facts_to_str(user_data))
    
    update.message.reply_text(
        "¡Genial! Para que sepas, esto es lo que ya me has dicho:"
        f"{facts_to_str(user_data)} Puedes decirme más, o cambiar tu opinión"
        " Sobre algo.",
        reply_markup=markup,
    )

    return CHOOSING


def listadoV(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Este es el Listado Actualizado de los vuelos:")
    logger.info("Logramos entrar en ListadoV")
    vuelos = gsconn.getlistado()
    logger.info("Se realizo el Vuelos")
    update.message.reply_text(f"{vuelos}",reply_markup=markup)
    
    return CHOOSING



def done(update: Update, context: CallbackContext) -> int:

    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']
    update.message.reply_text(
        f"Me he enterado de estos datos sobre ti: {facts_to_str(user_data)} ¡Hasta la próxima vez!"
    )

    return ConversationHandler.END


def main() -> None:
    
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.regex('^start$'), start),
                MessageHandler(
                    Filters.regex('^(Nombre|Age|Color favorito|Number of siblings)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Buscar$'), custom_choice),
                MessageHandler(Filters.regex('^Listado$'), listadoV),

            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
                ),
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), buscar_choice
                ),
                
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