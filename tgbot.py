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

GETMSG, GETNUM = range(2)


def start(bot, update):
    """
    Show welcome message
    """
    update.message.reply_text(
        'Hello {}!'.format(update.message.from_user.first_name)+'\n'
        'My name is T-Gmail Scholar Alert Bot. Hope I can help you! ',
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

def get(bot, update, args):
    """
    Get all the emails' literatures.
    It's A Disastah!! if you have too many unreaded Google Scholar Alert emails.
    Yeah, like a $6Million's EchoSlam right on your head.
    """
    try:
        msg_no = int(args[0])
        if msg_no < 2 or msg_no > 5:
            update.message.reply_text(
                    'Invalid given number: {}'.format(args[0])+'\n'
                    'Usage: /get <number>\n'
                    '<number> should be in 2~5.'

                    )
            return
    
        tgMsg = []
        tgMsg = gmail.getGmailMsg(msg_no)
        
        for message in tgMsg[0:n]:
            for info in message.msg:
                update.message.reply_text(
                        text = info, 
                        parse_mode=tg.ParseMode.MARKDOWN
                        )   
        return ConversationHandler.END

    except(IndexError, ValueError):
        update.message.reply_text(
                'Usage: /get <number>\n'
                '<number> should be in 2~5.'
                )

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    
    config = configparser.ConfigParser()
    config.read('config.ini')

    Token = config['token_info']['token']
    proxy = config['proxy_info']['proxy']
    REQUEST_KWARGS = {'proxy_url': proxy}

    updater = Updater(token = Token,  request_kwargs = REQUEST_KWARGS )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("latest", latest))
    dp.add_handler(CommandHandler("all", all))
    dp.add_handler(CommandHandler("get", get, pass_args=True))


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
