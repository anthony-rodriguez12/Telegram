
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

CHOOSING, TYPING_REPLY, TYPING_CHOICE, BUSCAR, VER, RETORNO, UBICACION, ANSWER, ID, NOMBRE, CEDULA, FECHA, RESERVA, ASIENTOS = range(14)

reply_keyboard = [
    ['Ver Vuelo', 'Buscar','Listado'],
    ['Buy Ticket', 'BuyRT Ticket'],
    ['start','Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)




def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    logger.info("Ingresamos a start")
    name = update.message.from_user.username
    
    update.message.reply_text(
         f"!Bienvenido {name}! Esto es SkytravelApp\nUn Bot para ayudarte a Revisar, Buscar Vuelos y Comprar Voletos para  Avión\n"
        "¿Que puedo hacer por ti?",
        reply_markup=markup
    
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Buscaremos coincidencias con {text.lower()} en los campos mencionados anteriormente.')

    return TYPING_REPLY

def buscar_choice(update: Update, context: CallbackContext) -> int:
    logger.info("Logramos Ingresamos a buscar choice")

    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Buscaremos coincidencias con {text} en los campos mencionados anteriormente.')

    vuelos = gsconn.Buscar(text)
    logger.info("Se realizo el Buscar(text)")
    update.message.reply_text(f"Estos son los Resultados de buscar {text}:")
    update.message.reply_text(f"{vuelos}")
    update.message.reply_text(f'Escriba "OK" para continuar')
  
    return RETORNO

def Volver_Retorno(update: Update, context: CallbackContext) -> int:
    logger.info("Logramos Ingresamos a Volver_Retorno")
    name = update.message.from_user.username
    update.message.reply_text(f"Listo {name}!,\n¿Que deseas hacer ahora?",reply_markup=markup,)

    return CHOOSING


def buscar_choice_vuelo(update: Update, context: CallbackContext) -> int:
    logger.info("Logramos Ingresar a buscar choice vuelo")

    text = update.message.text
    context.user_data['choice'] = text
    
    update.message.reply_text(f'Buscaremos el ID: {text.upper()} en los registros de vuelos, Porfavor espere.')
    vuelos = gsconn.Ver_Vuelo(text.upper())
    logger.info(f"Se realizo el Buscar({text})")
    update.message.reply_text(f"{vuelos}")
    
    update.message.reply_text(f'Porfavor vuelva a iniciar si desea revisar otro vuelo')
    update.message.reply_text(f'Escriba Ok para continuar')
    return RETORNO

def custom_choice(update: Update, context: CallbackContext) -> int:
    logger.info("Logramos entrar en cusmtom_choice de Buscar")
    update.message.reply_text(
        '¿Deseas Buscar? No hay problema!'
    )
    update.message.reply_text(
        'Puedes buscar ingresando alguno de los siguientes datos:\n Pais de Destino/Origen\n Código IATA\n Nombre de Aeropuerto\n Ciudad o País'
    )
    update.message.reply_text(
        'Recuerda solo ingresar uno de estos datos por búsqueda.'
    )

    return BUSCAR

def custom_choiceV(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Para revisar los detalles de un vuelo,' ' por favor ingresar el "ID" del vuelo que deseas revisar'
    )

    return VER


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
    logger.info("Se mostro el listado de vuelos")
    update.message.reply_text(f"{vuelos}",reply_markup=markup)
    
    return CHOOSING

def Buy_Ticket(update: Update, context: CallbackContext) -> int:
    logger.info("Iniciamos el procesos de Reservar un vuelo solo de ida")
    update.message.reply_text("*****RESERVACIÓN SOLO VUELO DE IDA*****")
    update.message.reply_text("Para Reservar un vuelo primero dinos, ¿En que aeropuerto de los de la lista te encuentras?")
    update.message.reply_text("José Joaquín de Olm.\nLas Américas\nToronto\nWashington Dulles\nJosé Joaquín de Olm.")
    logger.info("Se mostro el contesto la ubicacion")
    
    return UBICACION

def ubicacion1(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos Ubicación: {text}")
    lista = gsconn.Buscar(text)
    ubi = gsconn.SaveNube('F1',text)
    logger.info(ubi)
    logger.info("Se realizaron la lista y el save ubicacion")
    update.message.reply_text("Listo Se ha Guardado Satisfactoriamente tu respuesta")
    update.message.reply_text(f"Aqui Estan Todos Los Vuelos del Aeropuerto {text}")
    update.message.reply_text(f"{lista}")
    update.message.reply_text("¿Desea realizar una reservación en alguno de los vuelos mostrados?\nPorfavor Responda un Si o un No")

    return ANSWER


def answerY(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos un: {text} por respuesta")
    update.message.reply_text("Listo reservaremos un asiento de los vuelos mostrados para ti")
    update.message.reply_text("Por favor ingresa el ID del vuelo que deseas" )

    return ID

def TheId(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos el ID: {text}")
    pas = gsconn.Buscar_ID(text)
    elID = gsconn.SaveNube('B1',text)
    logger.info(f"El Estado del ID:{elID}")
    if pas == 'ok':
        update.message.reply_text("Listo Se ha Guardado Satisfactoriamente el ID de tu respuesta")
        update.message.reply_text("Ahora Porfavor Ingresa tus Datos Reales para crear un comprobante de Registro")
        update.message.reply_text("Como Primer Dato Ingresa tu Nombre Completo\n Ejemplo: Manuel Jose Perez Herrera")
        return NOMBRE

    else:        
        update.message.reply_text("Losiento el ID es Incorrecto Vuelve a Ingresarlo")
        return ID
 

def answerN(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos un: {text} por respuesta")
    update.message.reply_text(f"Respondiste {text}, asi que escoje ¿Que deseas hacer ahrora?",reply_markup=markup)

    return CHOOSING


def Regis_Nombre(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos el Nombre: {text}")
    Nom = gsconn.SaveNube('B2',text)
    logger.info(Nom)
    logger.info("Se Guardo el Nombre")

    update.message.reply_text(f"Listo Se ha Guardado Satisfactoriamente tu Nombre como:{text}")
    update.message.reply_text("Ahora Porfavor Ingresa tu Cédula de Identidad\n Ejemplo: 0987654321")
    return CEDULA 

def Regis_Cedula(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos su número de Cedula: {text}")
    Ced = gsconn.SaveNube('B3',text)
    logger.info(Ced)
    logger.info("Se Guardo el número de Cedula")
    update.message.reply_text(f"Listo Se ha Guardado Satisfactoriamente tu número de Cedula:{text}")
    update.message.reply_text('Ahora Porfavor Ingresa la Fecha para tu vuelo\n Ejemplo: "10/4/2021"')
    return FECHA 

def Regis_Fecha(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos la fecha de su vuelo: {text}")
    Fecha_Vuelo = gsconn.SaveNube('B5',text)
    logger.info(Fecha_Vuelo)
    logger.info("Se Guardo la fecha de su vuelo")

    update.message.reply_text(f"Listo Se ha Guardado Satisfactoriamente la fecha de su vuelo en:{text}")
    update.message.reply_text('Ahora Porfavor escriba "ok" para seguir ')
    return  RESERVA

def Reservados(update: Update, context: CallbackContext) -> int:
    logger.info("Listo empezaremos el proceso de reservación")
    elID = gsconn.Retornar_ID()
    elasiento = gsconn.Buscar_Asientos(elID)
    logger.info("Se Completo el retorno del ID")
    update.message.reply_text(f"Listo, tenemos: {elasiento} asientos disponibles, cuantos desea reservar?")
    return  ASIENTOS

def Regis_Asientos(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Listo reservaremos {text} asientos")
    update.message.reply_text(f"Listo, Reservaremos {text} asientos para usted")
    CAsiento = gsconn.SaveNube('B6',text)
    logger.info(CAsiento)
    logger.info("Se guardo la cantidad de asientos reservados")
    update.message.reply_text(f"Listo, Porfavor Ingrese una lista de los asientos que desea reservar.")
    update.message.reply_text('Le recordamos que los nombres de los asientos son los numeros del 1 al 300\n Para ingresar los nombres separelos por ","\n Ejemplo 11,2,4,5,8')

    return  ASIENTOS


def done(update: Update, context: CallbackContext) -> int:
    nombre = update.message.from_user.username

    update.message.reply_text(
        f"Muchas Gracias {nombre} vuelva pronto esperamos haverle servido de ayuda \n ¡¡Hasta la próxima vez!!"
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
                    #Filters.text & ~Filters.command, regular_choice
                    Filters.regex('^(Nombre)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Buscar$'), custom_choice),
                MessageHandler(Filters.regex('^Listado$'), listadoV),
                MessageHandler(Filters.regex('^Ver Vuelo$'), custom_choiceV),
            ],  
            TYPING_CHOICE: [
                 MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), buscar_choice_vuelo
                ),
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
            BUSCAR: [
                MessageHandler(
                   Filters.text & ~Filters.command, buscar_choice
                )
            ],
            VER: [
                MessageHandler(
                   Filters.text & ~Filters.command, buscar_choice_vuelo
                )
            ],
            RETORNO: [
                MessageHandler(
                   Filters.text & ~Filters.command, Volver_Retorno
                )
            ],
            UBICACION: [
                MessageHandler(
                   Filters.text & ~Filters.command, ubicacion1 
                )
            ], 
            ANSWER: [
                MessageHandler(
                    Filters.regex('^(Si)$'), answerY,
                    Filters.regex('^(No)$'), answerN
                ),
            ],
            ID: [
                MessageHandler(
                   Filters.text & ~Filters.command, TheId 
                )
            ],
            NOMBRE: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Nombre 
                )
            ],
            CEDULA: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Cedula 
                )
            ],
            FECHA: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Fecha 
                )
            ],
            RESERVA: [
                MessageHandler(
                   Filters.text & ~Filters.command, Reservados 
                )
            ],
            ASIENTOS: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Asientos 
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