"""
Basic example for a bot that uses inline keyboards.
"""
from telegram.ext import Updater, CommandHandler
from helper import gsheet_helper

from cfg import TOKEN    
    
    #updater = Updater("1595242339:AAFfNxwj3JB108952Oo1jO6VcKmKpYIDURk")
    #$env:TOKEN="1595242339:AAFfNxwj3JB108952Oo1jO6VcKmKpYIDURk"  <-- copiar

def start(update, context):
    print(update.message)

    update.message.replay_text(f"Holis! Esto es SkyTravelAPP!")

def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Start
    updater.start_polling()
    print("Estoy vivo")

    #Me quedo esperando
    updater.idle()

if __name__=="__main__":
    main()
    