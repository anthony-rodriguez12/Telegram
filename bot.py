from telegram.ext import Updater, CommandHandler


def start(update, context):

    update.message.reply_text('Hola, Humano!')

if __name__== '__main__':

    updater = Updater(token='1595242339:AAFfNxwj3JB108952Oo1jO6VcKmKpYIDURk',use_context=True)

    dp = updater.dispatcher 

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()