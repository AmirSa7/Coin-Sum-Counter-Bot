# do this so we acn import modules from parent dir
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.files import file

import cv2
import numpy as np
from io import BytesIO

import recognition.processing.process_image as pi
import client


def count_coins_in_recieved_image(update: Update, context: CallbackContext) -> None:
    """Perform all the proccessing and return a value"""

    # download_recieved_image(update, context)

    img = get_last_recieved_photo_as_ndarray(update)

    # proccessedImg, coinSum = client.send_image_to_flask_server(img)
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
    imgByteStringArray = get_TelegramFile_as_byte_string_array(telegramFile)
    ndarray = cv2.imdecode(imgByteStringArray, -1)
    return ndarray


# def get_TelegramFile_as_ndarray(telegramFile) -> np.ndarray:
#     io_buf = BytesIO()
#     telegramFile.download(out=io_buf)
#     io_buf.seek(0)
#     ndarray = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
#     io_buf.close()
#     return ndarray


def get_TelegramFile_as_byte_string_array(telegramFile):
    io_buf = BytesIO()
    telegramFile.download(out=io_buf)
    io_buf.seek(0)
    imgByteString = io_buf.getbuffer()
    imgByteStringArray = np.frombuffer(imgByteString, np.uint8).copy()
    # io_buf.close() TODO: understand how to close this buffer correctly
    return imgByteStringArray


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