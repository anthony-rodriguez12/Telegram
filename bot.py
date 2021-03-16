"""
Basic example for a bot that uses inline keyboards.
"""
from telegram.ext import Updater, CommandHandler
from helper import gsheet_helper

from cfg import TOKEN    
    
    #$env:TOKEN="1595242339:AAFfNxwj3JB108952Oo1jO6VcKmKpYIDURk"  <-- copiar Token

gsconn = gsheet_helper()

def start(update, context):
   # print(update.message)
    name = update.message.from_user.username
    Saludo = f"""
Hola! {name}!, Esto es SkyTravelAPP!\n¿En que puedo ayudarte?
/Ver_Vuelos - Mostrara los Vuelos.   /Buscar para buscar
    """
    update.message.reply_text(Saludo)
    print("esto es message.text: %s",update.message.text)
    print("esto es from_user: %s",update.message.from_user)
    
def listadoV(update, context):
    vuelos = gsconn.getlistado()
    update.message.reply_text(f"{vuelos}")
    # New_Avi = {
    #     'Id:': 2,
    #    'Avion:':"Fenix",
    #    'IATA:':"GYE",
    #    'Aerop - Origen:':"José Joaquín de Olmedo",
    #    'Aerop - Destino:':"José Delgado",
    #    'Pais-Origen:':"Ecuador",
    #    'Pais-Des:':"Mexico",
    #    'Ciudad-Orig:':"Guayaquil",
    #    'Ciudad-Des:':"Mexico City",
    #    'Asientos-Libre:':300,
    #    'Asient-Ocupa:': 0
    #}
    update.message.reply_text("Ingresa el aeropuerto ")
    New_Avi = update.message.text
    gsconn.store_user(New_Avi)
    
    #update.message.reply_text(f"Listo! Datos añadidos!")
def buscar(update, context):
    update.message.reply_text("Ingresa el aeropuerto ")
    New_Avi = update.message.text
    gsconn.store_user(New_Avi)
    

def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("Ver_Vuelos", listadoV))
    updater.dispatcher.add_handler(CommandHandler("Buscar", buscar))

    # Start
    updater.start_polling()
    print("Estoy vivo")

    #Me quedo esperando
    updater.idle()

if __name__=="__main__":
    main()
    