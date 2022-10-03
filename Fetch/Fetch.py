import base64
import urllib

import telebot
from PIL import Image
from craiyon import Craiyon
from dalle2 import Dalle2
from telebot import types
from Constants.constansts import *
from Utill.UrlExtractor import *

bot = telebot.TeleBot(API_KEY)

def premiumFetch(text, message):
    dalle = Dalle2(DALLE_SESS)

    print("Go")
    print(text)
    generations = dalle.generate(text)

    urls = extractURLS(generations)

    list = []
    for i in urls:
        with urllib.request.urlopen(i) as url:
            img = Image.open(url)
            image = telebot.types.InputMediaPhoto(img)
            list.append(image)



    bot.send_media_group(message.chat.id, list)

    bot.send_message(message.chat.id, AFTER_RESULT)



def freeFetch(text, message):
    print("freeFetch")
    print(text)
    generator = Craiyon()  # Instantiates the api wrapper
    result = generator.generate(text)
    images = result.images  # A list containing image data as base64 encoded strings
    list = []
    for i in images:
        image = telebot.types.InputMediaPhoto(base64.decodebytes(i.encode("utf-8")))
        list.append(image)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    credits = types.KeyboardButton(MY_CREDITS)
    buy_credits = types.KeyboardButton(BUY_CREDITS)
    requests = types.KeyboardButton(EXAMPLES_PROMTS)
    support = types.KeyboardButton(SUPPORT)
    markup.add(credits, buy_credits, requests, support)

    bot.send_media_group(message.chat.id, list)
    bot.send_message(message.chat.id, AFTER_RESULT, reply_markup=markup)

    result.save_images()  # Saves the generated images to 'current working directory/generated', you can also provide a custom path

