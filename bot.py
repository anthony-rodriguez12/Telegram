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

    #update.message.replay_text(f"Hola! Esto es SkyTravelAPP!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    update.message.reply_text('TOdo bien')

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
    