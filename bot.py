import logging
import numpy as np
import time
import os
import sys

from helper import gsheet_helper
from cfg import TOKEN,mode    

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


CHOOSING, TYPING_REPLY, TYPING_CHOICE, BUSCAR, VER, RETORNO, BUY_TICKET1, BUYRT_TICKET1, UBICACION, ANSWER, ID, NOMBRE, CEDULA, FECHA, RESERVA, ASIENTOS, LISTASIENTOS, MOSTRAR = range(18)

reply_keyboard = [
    ['Ver Vuelo', 'Buscar','Listado'],
    ['Buy Ticket', 'BuyRT Ticket'],
    ['start','Salir'],
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
    logger.info(f"El usuario {name} inicio el bot")

    update.message.reply_text(
         f"!Bienvenido {name}! Esto es SkytravelApp\nUn Bot para ayudarte a Revisar, Buscar Vuelos y Comprar Boletos para  Avión.\n"
        "¿Qué puedo hacer por ti?, Si deseas ayuda escribe help y te dare más detalles",
        reply_markup=markup    
    )

    return CHOOSING

def help(update: Update, context: CallbackContext) -> int:
    
    name = update.message.from_user.username
    logger.info(f"El usuario {name}pide ayuda")
    update.message.reply_text(
         f"!Bienvenido {name}! Esto es **SkytravelApp**\nUn Bot para ayudarte a Revisar, Buscar Vuelos y Comprar Boletos para  Avión.\n"
        "Pediste ayuda así que te explicaré como funciono,\n"
        "Tengo 7 botones que puedes usar para interactuar conmigo en mis distintas funciones\n"
        "Listado: Mostrará el listado de todos los vuelos que tengo registrados.\n"
        "Buscar: Buscará en la base de datos un vuelo que desees usando distintos parámetros.\n"
        "Ver Vuelo: Mostrará un vuelo de mi base de datos con todos sus detalles.\n"
        "Buy Ticket: Reservará un asiento/s en un vuelo solo de ida que hayas seleccionado.\n"
        "BuyRT Ticket:Reservará un asiento/s en un vuelo de ida y vuelta que hayas seleccionado.\n"
        "start: Empieza de nuevo la conversación después de salir de ella.\n"
        "Salir: Saldrá de cualquier menú en el que estés.",
        reply_markup=markup    
    )
    update.message.reply_text("Prueba Alguno de los comandos")


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
    update.message.reply_text(f'Por favor Escribe "OK" para continuar')
  
    return RETORNO

def Volver_Retorno(update: Update, context: CallbackContext) -> int:
    logger.info("Logramos Ingresamos a Volver_Retorno")
    name = update.message.from_user.username
    update.message.reply_text(f"Listo {name}!,\n¿Qué deseas hacer ahora?",reply_markup=markup,)

    return CHOOSING


def buscar_choice_vuelo(update: Update, context: CallbackContext) -> int:
    logger.info("Logramos Ingresar a buscar choice vuelo")

    text = update.message.text
    context.user_data['choice'] = text
    
    update.message.reply_text(f'Buscaremos el ID: {text.upper()} en los registros de vuelos, Por favor espere.')
    vuelos = gsconn.Ver_Vuelo(text.upper())
    logger.info(f"Se realizo el Buscar({text})")
    update.message.reply_text(f"{vuelos}")
    
    update.message.reply_text(f'Vuelva a iniciar si desea revisar otro vuelo')
    update.message.reply_text(f'Por favor Escribe "OK" para continuar')
    return RETORNO

def custom_choice(update: Update, context: CallbackContext) -> int:
    logger.info("Logramos entrar en cusmtom_choice de Buscar")
    update.message.reply_text(
        '¿Deseas Buscar? No hay problema!'
    )
    update.message.reply_text(
        'Puedes buscar ingresando alguno de los siguientes datos:\n País de Destino/Origen\n Código IATA\n Nombre de Aeropuerto\n Ciudad o País'
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
    update.message.reply_text(f"{vuelos}")
    name = update.message.from_user.username
    update.message.reply_text(f"Listo {name}!,\n¿Qué deseas hacer ahora?",reply_markup=markup)
    
    return CHOOSING

def Buy_Ticket(update: Update, context: CallbackContext) -> int:
    logger.info("Iniciamos el procesos de Reservar un vuelo solo de ida")
    update.message.reply_text("*****RESERVACIÓN SOLO VUELO DE IDA*****")
    update.message.reply_text("Para Reservar un vuelo primero dinos, ¿En que aeropuerto de los de la lista te encuentras?")
    update.message.reply_text("Las Américas\nToronto\nWashington Dulles\nJosé Joaquín de Olmedo\n De la Ciudad de México\n El Dorado\n Ibiza\n La Chinita\n Astor Piazzolla\n Diego Aracena\n Comodoro Arturo Merino Benítez\n José María Córdova\n Sevilla-San Pablo\n Maiquetía Simón Bolívar\n Berlín-Tegel\n Tirana-Madre Teresa\n Adolfo Suárez Madrid-Barajas\n Miconos\n Florencia-Peretola\n Jorge Newbery\n Mariscal Sucre\n São Paulo\n Jorge Chávez\n Ottawa\n Gustavo Rojas Pinilla\n Zaragoza\n Sauce Viejo\n Suárez Madrid-Barajas")

    logger.info("Se mostro el contesto la ubicacion")
    
    return UBICACION

def BuyRT_Ticket(update: Update, context: CallbackContext) -> int:
    logger.info("Iniciamos el procesos de Reservar un vuelo solo de ida")
    update.message.reply_text("****RESERVACIÓN VUELO****\n****DE IDA Y VUELTA****")
    update.message.reply_text("Para Reservar un vuelo primero dinos, ¿En que aeropuerto de los de la lista te encuentras?")
    update.message.reply_text("Las Américas\nToronto\nWashington Dulles\nJosé Joaquín de Olmedo\n De la Ciudad de México\n El Dorado\n Ibiza\n La Chinita\n Astor Piazzolla\n Diego Aracena\n Comodoro Arturo Merino Benítez\n José María Córdova\n Sevilla-San Pablo\n Maiquetía Simón Bolívar\n Berlín-Tegel\n Tirana-Madre Teresa\n Adolfo Suárez Madrid-Barajas\n Miconos\n Florencia-Peretola\n Jorge Newbery\n Mariscal Sucre\n São Paulo\n Jorge Chávez\n Ottawa\n Gustavo Rojas Pinilla\n Zaragoza\n Sauce Viejo\n Suárez Madrid-Barajas")
    logger.info("Se mostro el contesto la ubicacion")
    
    return UBICACION

def ubicacion1(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos Ubicación: {text}")
    lista = gsconn.Buscar(text)
    ubi = gsconn.SaveNube('F1',text)
    logger.info(ubi)
    logger.info("Se realizaron la lista y el save ubicacion")
    update.message.reply_text("Listo Se ha Guardado Satisfactoriamente su respuesta")
    update.message.reply_text(f"Aqui Estan Todos Los Vuelos del Aeropuerto de {text}")
    update.message.reply_text(f"{lista}")
    update.message.reply_text("¿Desea realizar una reservación en alguno de los vuelos mostrados?\nPorfavor Responda un Si o un No")

    return ANSWER


def answerY(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos un: {text} por respuesta")
    update.message.reply_text("Listo, realizaremos tu reservación en uno de los vuelos mostrados anteriormente")
    update.message.reply_text("Por favor ingresa el ID del vuelo que deseas" )

    return ID

def TheId(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos el ID: {text}")
    pas = gsconn.Buscar_ID(text)
    elID = gsconn.SaveNube('B1',text)
    logger.info(f"El Estado del ID:{elID}")
    if pas == 'ok':
        update.message.reply_text("Listo Se ha Guardado Satisfactoriamente su respuesta")
        update.message.reply_text("Porfavor Ingresa tus Datos Reales para crear un comprobante de Registro")
        update.message.reply_text("Como Primer Dato Ingresa tu Nombre Completo\n Ejemplo: Manuel Jose Perez Herrera")
        return NOMBRE

    else:        
        update.message.reply_text("Losiento el ID es Incorrecto Vuelve a Ingresarlo")
        return ID
 

def answerN(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    logger.info(f"Obtubimos un: {text} por respuesta")
    update.message.reply_text(f"Esta bien respondiste {text},¿Qué deseas hacer ahrora?",reply_markup=markup)

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
    Fecha_Actual = gsconn.FechNube('B4')
    logger.info(f"Se Guardo la fecha de su vuelo:{Fecha_Vuelo} y esto se hizo el {Fecha_Actual}")

    update.message.reply_text(f"Listo Se ha Guardado Satisfactoriamente la fecha de su vuelo en:{text}")
    update.message.reply_text('Ahora Porfavor escriba "OK" para seguir ')
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
    try:
        text = int(text)
    except:
        text = text
    if type(text) != str:
        if text > 0:
        
            logger.info(f"Listo reservaremos {text} asientos")
            update.message.reply_text(f"Listo, Reservaremos {text} asientos para usted")
            CAsiento = gsconn.SaveNube('B6',text)
            logger.info(CAsiento)
            logger.info("Se guardo la cantidad de asientos reservados")
            update.message.reply_text(f"Listo, Porfavor Ingrese una lista de los asientos que desea reservar.")
            update.message.reply_text('Le recordamos que los nombres de los asientos son los numeros del 1 al 300\n Para ingresar los nombres separelos por ","\n Ejemplo 11,2,4,5,8')     
        
            return LISTASIENTOS
        else:
            logger.info(f"Las reservación: {text} esta mal ingresada")
            update.message.reply_text(f"Losiento ingreso una respuesta númerica erronea vuelva a intentarlo")
            return ASIENTOS
    else:
            logger.info(f"Las reservación: {text} esta mal ingresada")
            update.message.reply_text(f"Losiento ingreso una respuesta de texto, vuelva a intentarlo")
            return ASIENTOS            

def Lista_Asientos(update: Update, context: CallbackContext) -> int:
    text = update.message.text  
    logger.info(f"Listo reservaremos los asientos: {text}")
    update.message.reply_text(f"Listo, Usted Reservo estos asientos: {text} ")
    TotalAsientos = gsconn.SaveNube('B10',text)
    logger.info(TotalAsientos)
    logger.info("Se guardaron todos los asientos que reservo")
    update.message.reply_text(f"Por Favor Escriba Mostrar para generar su Recibo")

    return MOSTRAR

def Mostrar_Recib(update: Update, context: CallbackContext) -> int:
    logger.info(f"**Listo Generaremos Recibo**")
    Recibo = gsconn.mostrar()
    try:
        Recibo = int(Recibo)
    except:
        Recibo = Recibo
    update.message.reply_text(f"Felicidades Por Completar la compra de volesto/s para su viaje con Éxito")
    if Recibo[2] == 1:
        update.message.reply_text("************* RECIBO DE IDA *************\n"f"{Recibo[0]}" "\nLista de Asientos Reservados:\n" f"{Recibo[1]}" )
    elif Recibo[2] == 1:
        update.message.reply_text("**********RECIBO DE IDA Y VUELTA **********\n"f"{Recibo[0]}" "\nLista de Asientos Reservados:\n" f"{Recibo[1]}" )        
    update.message.reply_text(f"¿En que le puedo ayudar Ahora?",reply_markup=markup)

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    nombre = update.message.from_user.username
    logger.info(f"El usuario {nombre}Ha salido del bot")
    update.message.reply_text(
        f"Muchas Gracias {nombre} vuelva pronto esperamos haberle servido de ayuda \n ¡¡Hasta la próxima vez!!"
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
                MessageHandler(Filters.regex('^help$'), help),
                MessageHandler(Filters.regex('^Help$'), help),
                MessageHandler( 
                    #Filters.text & ~Filters.command, regular_choice
                    Filters.regex('^(Nombre)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Buscar$'), custom_choice),
                MessageHandler(Filters.regex('^Buy Ticket$'), Buy_Ticket),
                MessageHandler(Filters.regex('^BuyRT Ticket$'), BuyRT_Ticket),
                MessageHandler(Filters.regex('^Listado$'), listadoV),
                MessageHandler(Filters.regex('^Ver Vuelo$'), custom_choiceV),
                MessageHandler(Filters.regex('^Salir$'), done )
            ],  
            TYPING_CHOICE: [
                 MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), buscar_choice_vuelo
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            BUSCAR: [
                MessageHandler(
                   Filters.text & ~Filters.command, buscar_choice
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            VER: [
                MessageHandler(
                   Filters.text & ~Filters.command, buscar_choice_vuelo
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            RETORNO: [
                MessageHandler(
                   Filters.text & ~Filters.command, Volver_Retorno
                ),                
            ],
             BUY_TICKET1: [
                MessageHandler(
                    Filters.regex('^Buy Ticket$'), Buy_Ticket
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],  
            BUYRT_TICKET1: [
                MessageHandler(
                    Filters.regex('^BuyRT Ticket$'), BuyRT_Ticket
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],  
            UBICACION: [
                MessageHandler(
                   Filters.text & ~Filters.command, ubicacion1 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ], 
            ANSWER: [
                MessageHandler(
                    Filters.regex('^Si$'), answerY                    
                ),
                MessageHandler(
                    Filters.regex('^si$'), answerY                    
                ),
                MessageHandler(
                    Filters.regex('^No$'), answerN
                ),
                 MessageHandler(
                    Filters.regex('^no$'), answerN
                ),MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            ID: [
                MessageHandler(
                   Filters.text & ~Filters.command, TheId 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            NOMBRE: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Nombre 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            CEDULA: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Cedula 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            FECHA: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Fecha 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            RESERVA: [
                MessageHandler(
                   Filters.text & ~Filters.command, Reservados 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            ASIENTOS: [
                MessageHandler(
                   Filters.text & ~Filters.command, Regis_Asientos 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            LISTASIENTOS: [
                MessageHandler(
                   Filters.text & ~Filters.command, Lista_Asientos 
                ),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
            MOSTRAR: [
                MessageHandler(Filters.regex('^Mostrar$'), Mostrar_Recib),
                MessageHandler(Filters.regex('^mostrar$'), Mostrar_Recib),
                MessageHandler(
                    Filters.regex('^Salir$'), done )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Salir$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    if mode == "dev":
        # Acceso Local (desarrollo)
        # Start the Bot
        updater.start_polling()

        updater.idle()

    elif mode == "prod":
        #Acceso HEROKU (producción)
        def run(updater):
            PORT = int(os.environ.get("PORT","8443"))
            HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
            # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
            updater.start_webhook(Listen="0.0.0.0", port=PORT, url_parth=TOKEN)
            updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
            
    else:
        logger.info("No se especificó el Mode.")
        sys.exit()

    run(updater)

if __name__ == '__main__':
    main()
    


