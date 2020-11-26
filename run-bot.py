#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.files import file

import time
import cv2

from Utils import utils

import numpy as np
from io import BytesIO
import json

import recognition.processing.process_image as pi

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Shahar is cute!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot is still under construction.')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    


def count_coins_in_recieved_image(update: Update, context: CallbackContext) -> None:
    """Perform all the proccessing and return a value"""

    # download_recieved_image(update, context)

    img = get_last_recieved_photo_as_ndarray(update)
    proccessedImg, coinSum = pi.process_image(img)
    send_ndarray_image_to_user(update, context, proccessedImg)
    replyString = 'The sum of the coins is: {}'.format(coinSum)
    update.message.reply_text(replyString)

    print(replyString)



def send_ndarray_image_to_user(update: Update, context: CallbackContext, img: np.ndarray):
    chat_id = update.message.chat_id

    is_success, buffer = cv2.imencode(".jpg", img)
    io_buf = BytesIO(buffer)
    io_buf.seek(0)

    context.bot.send_photo(chat_id, photo=io_buf)
    io_buf.close()



def get_TelegramFile_as_ndarray(telegramFile) -> np.ndarray:
    io_buf = BytesIO()
    telegramFile.download(out=io_buf)
    io_buf.seek(0)
    ndarray = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
    io_buf.close()
    return ndarray


def get_last_recieved_photo_as_ndarray(update: Update) -> np.ndarray:
    telegramFile = update.message.photo[-1].get_file()
    ndarray = get_TelegramFile_as_ndarray(telegramFile)
    return ndarray


def download_recieved_image(update: Update, context: CallbackContext) -> None:
    """Download the last image recieved by the user."""
    newFile = update.message.photo[-1].get_file()
    newFileName = produce_img_name(update)
    newFile.download(newFileName)
    print('Image was successfully downloaded and saved.')


def produce_img_name(update: Update) -> str:
    folder = 'Bot-Operation/Recieved-Images/'
    userID =  str(update.message.from_user.id)
    currTime = str(time.time())
    fileExtension = '.jpg'
    delim = '-'
    fixedName = 'last_image'

    imgName = folder + userID + delim + currTime + fileExtension
    return imgName
    

def read_txt_file_to_string(txt_file: str) -> str:
    """Return The text stored inside a txt_file.txt file as string"""
    with open(txt_file, 'r') as file:
        data = file.read().replace('\n', '')
        return data


def get_token_from_txt_file(token_txt_file: str) -> str:
    token_string = read_txt_file_to_string(token_txt_file)
    return token_string



def main():
    """Start the bot."""

    token = get_token_from_txt_file('../CoinSumCounterBotToken.txt')

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo, count_coins_in_recieved_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
