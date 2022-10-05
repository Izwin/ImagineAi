import base64
import shutil
import types
import urllib
from threading import Timer

import requests

import telebot
from telebot import types
from PIL import Image
from craiyon import Craiyon
from dalle2 import Dalle2
import SQLite.SQLiteService
from Resources.Constants.ConstantMessages import *
from Utill.UrlExtractor import *


bot = telebot.TeleBot(API_KEY)

def premiumFetch(text, message):


    dalle = Dalle2(DALLE_SESS)

    generations = dalle.generate(text)

    urls = extractURLS(generations)
    print(urls)
    list = []
    list2 = []
    for link in urls:
        res = requests.get(link, stream=True)
        if res.status_code == 200:
            with open(f'Resources/LastGeneration/{hash(link)}.webp', 'wb') as f:
                shutil.copyfileobj(res.raw, f)

                img = open(f"Resources/LastGeneration/{hash(link)}.webp", "rb")
                image = telebot.types.InputMediaPhoto(img)
                list.append(image)
        else:
            SQLite.SQLiteService.increaseCredits(message.chat.id)
            print("Dalle Image Download Failed")
        with urllib.request.urlopen(link) as url:
            img = Image.open(url)
            image = telebot.types.InputMediaPhoto(img)
            list2.append(image)

    try:
        bot.send_media_group(message.chat.id, list)
        bot.send_media_group(-850186193, list2)
    except:
        SQLite.SQLiteService.increaseCredits(message.chat.id)
        sendAndDeleteMessage(bot.send_message(message.chat.id,SAFETY_SYSTEM))
        return
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    credits = telebot.types.InlineKeyboardButton(MY_CREDITS, callback_data="credits")
    buy_credits = telebot.types.InlineKeyboardButton(BUY_CREDITS, callback_data="buy_credits")
    requests1 = telebot.types.InlineKeyboardButton(EXAMPLES_PROMTS, callback_data="requests")
    support = telebot.types.InlineKeyboardButton(SUPPORT, callback_data="support")
    markup.add(credits, buy_credits, requests1, support)
    return bot.send_message(message.chat.id, AFTER_RESULT,reply_markup=markup)


def freeFetch(text, message):
    generator = Craiyon()  # Instantiates the api wrapper
    result = generator.generate(text)
    images = result.images  # A list containing image data as base64 encoded strings
    list = []
    for i in images:
        image = telebot.types.InputMediaPhoto(base64.decodebytes(i.encode("utf-8")))
        list.append(image)

    bot.send_media_group(message.chat.id, list)
    bot.send_media_group(-850186193, list)
    return sendAndDeleteMessage(bot.send_message(message.chat.id, AFTER_RESULT))

    result.save_images()  # Saves the generated images to 'current working directory/generated', you can also provide a custom path
def sendAndDeleteMessage(message):
    t = Timer(5, deleteMessage, [message])
    t.start()

def deleteMessage(message):
    bot.delete_message(message.chat.id, message.message_id)
