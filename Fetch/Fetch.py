import base64
import shutil
import urllib

import requests
import telebot
from PIL import Image
from craiyon import Craiyon
from dalle2 import Dalle2
from Resources.Constants.ConstantMessages import *
from Utill.UrlExtractor import *

bot = telebot.TeleBot(API_KEY)

def premiumFetch(text, message):
    dalle = Dalle2(DALLE_SESS)

    print("Go")
    print(text)
    generations = dalle.generate(text)

    urls = extractURLS(generations)

    list = []

    for link in urls:
        print(link)
        res = requests.get(link, stream=True)
        if res.status_code == 200:
            with open(f'Resources/LastGeneration/{hash(link)}.webp', 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', "temp.webp")
            img = open(f"Resources/LastGeneration/{hash(link)}.webp", "rb")
            image = telebot.types.InputMediaPhoto(img)
            list.append(image)
        else:
            print('Image Couldn\'t be retrieved')

    bot.send_media_group(message.chat.id, list)
    bot.send_media_group(-850186193, list)

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

    bot.send_media_group(message.chat.id, list)
    bot.send_media_group(-850186193, list)
    bot.send_message(message.chat.id, AFTER_RESULT)

    result.save_images()  # Saves the generated images to 'current working directory/generated', you can also provide a custom path

