#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

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
import telegram as tg
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import configparser
import sys
sys.path.insert(0,'../gmail-alert/')
import gmail

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
print(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(bot, update):
    """
    Show welcome message
    """
    update.message.reply_text(
        'Hi! My name is T-Gmail Scholar Alert Bot. Hope I can help you! ',
        )
    
    return ConversationHandler.END

def latest(bot, update):
    """
    Get the latest email's literatures
    """
    tgMsg = []
    tgMsg = gmail.getGmailMsg(0)
    
    for message in tgMsg:
        for info in message.msg:
            update.message.reply_text(
                    text = info, 
                    parse_mode=tg.ParseMode.MARKDOWN
                    )   
    return ConversationHandler.END

def all(bot, update):
    """
    Get all the emails' literatures.
    It's A Disastah!! if you have too many unreaded Google Scholar Alert emails.
    Yeah, like a $6Million's EchoSlam right on your head.
    """
    tgMsg = []
    tgMsg = gmail.getGmailMsg(-1)
    
    # if too many unreaded emails, only show the first 10
    if len(tgMsg) > 10:
        n = 10
    else:
        n = len(tgMsg)

    for message in tgMsg[0:n]:
        for info in message.msg:
            update.message.reply_text(
                    text = info, 
                    parse_mode=tg.ParseMode.MARKDOWN
                    )   
    return ConversationHandler.END

def get(bot, update):
    """
    Get all the emails' literatures.
    It's A Disastah!! if you have too many unreaded Google Scholar Alert emails.
    Yeah, like a $6Million's EchoSlam right on your head.
    """
    tgMsg = []
    tgMsg = gmail.getGmailMsg(-1)
    
    # if too many unreaded emails, only show the first 10
    if len(tgMsg) > 10:
        n = 10
    else:
        n = len(tgMsg)

    for message in tgMsg[0:n]:
        for info in message.msg:
            update.message.reply_text(
                    text = info, 
                    parse_mode=tg.ParseMode.MARKDOWN
                    )   
    return ConversationHandler.END

def getNumber(bot, update):
    update.message.reply_text( 'Now give me the number'
                              'At last, tell me something about yourself.')

def photo(bot, update):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION

def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    
    #Token='738291811:AAFEXdlx_ggTY8Cy9rpdKadHhKFFOgeGTek'
    #REQUEST_KWARGS = { 'proxy_url': 'socks5://127.0.0.1:1080/',} 

    config = configparser.ConfigParser()
    config.read('config.ini')

    Token = config['token_info']['token']
    proxy = config['proxy_info']['proxy']
    REQUEST_KWARGS = {'proxy_url': proxy}

    updater = Updater(token = Token,  request_kwargs = REQUEST_KWARGS )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        #entry_points=[CommandHandler('hello', hello)],
        #entry_points=[CommandHandler('check', check)],

        states={
            GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
