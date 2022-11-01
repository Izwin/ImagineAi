import base64
import shutil
import urllib
from threading import Timer

import requests

import telebot
from telebot import types
from PIL import Image
from craiyon import Craiyon
from dalle2 import Dalle2

import ChatIds
import Constants
import MarkupsHelper
import OpenArt
import SQLiteService
import UrlExtractor

bot = telebot.TeleBot(Constants.API_KEY)

def premiumFetch(text, message,username):

    dalle = Dalle2(Constants.DALLE_SESS)
    generations = dalle.generate(text)
    urls = UrlExtractor.extractURLS(generations)
    lang = SQLiteService.getUserLanguage(message.chat.id)
    imageListForUser = []
    imageListForAnalytics = []

    for link in urls:
        res = requests.get(link, stream=True)
        if res.status_code == 200:
            with open(f'{hash(link)}.webp', 'wb') as f:
                shutil.copyfileobj(res.raw, f)

                img = open(f"{hash(link)}.webp", "rb")
                imageForList = telebot.types.InputMediaPhoto(img)
                imageListForUser.append(imageForList)
        else:
            print("Dalle загрузка изображений вызвала Exception")
        with urllib.request.urlopen(link) as url:
            img = Image.open(url)
            imageForList = telebot.types.InputMediaPhoto(img)
            imageListForAnalytics.append(imageForList)

    try:
        bot.send_media_group(message.chat.id, imageListForUser)
        bot.send_media_group(ChatIds.analytics, imageListForAnalytics)
    except:
        sendAndDeleteMessage(bot.send_message(message.chat.id,Constants.SAFETY_SYSTEM))
        return

    markup = MarkupsHelper.createMarkupMain(message.message_id,username,message.chat.id)

    bot.edit_message_text(Constants.AFTER_RESULT[lang],message.chat.id,message.message_id,reply_markup=markup)


def openArt(text, message, username):
    lang = SQLiteService.getUserLanguage(message.chat.id)

    urls = UrlExtractor.extractURLS(OpenArt.getOpenArtList(text))

    imageListForUser = []
    imageListForAnalytics = []

    for i in range(0,5):
        res = requests.get(urls[i], stream=True)
        if res.status_code == 200:
            with open(f'{hash(urls[i])}.webp', 'wb') as f:
                shutil.copyfileobj(res.raw, f)

                img = open(f"{hash(urls[i])}.webp", "rb")
                imageForList = telebot.types.InputMediaPhoto(img)
                imageListForUser.append(imageForList)
        else:
            print("OpenArt загрузка изображений вызвала Exception")
        with urllib.request.urlopen(urls[i]) as url:
            img = Image.open(url)
            imageForList = telebot.types.InputMediaPhoto(img)
            imageListForAnalytics.append(imageForList)

    try:
        bot.send_media_group(message.chat.id, imageListForUser)
        bot.send_media_group(ChatIds.analytics, imageListForAnalytics)
    except:
        sendAndDeleteMessage(bot.send_message(message.chat.id, Constants.SAFETY_SYSTEM[lang]))
        return

    markup = MarkupsHelper.createMarkupMain(message.message_id, username, message.chat.id)

    bot.edit_message_text(Constants.AFTER_RESULT[lang], message.chat.id, message.message_id, reply_markup=markup)


def freeFetch(request,message,username):
    generator = Craiyon()
    result = generator.generate(request)
    images = result.images
    imageList = []
    lang = SQLiteService.getUserLanguage(message.chat.id)

    for img in images:
        image = telebot.types.InputMediaPhoto(base64.decodebytes(img.encode("utf-8")))
        imageList.append(image)

    markup = MarkupsHelper.createMarkupMain(message.message_id,username,message.chat.id)
    bot.edit_message_text(Constants.AFTER_RESULT[lang],message.chat.id,message.message_id,reply_markup=markup)

    bot.send_media_group(message.chat.id, imageList)
    bot.send_media_group(ChatIds.analytics, imageList)



def sendAndDeleteMessage(message):
    t = Timer(5, deleteMessage, [message])
    t.start()

def deleteMessage(message):
    bot.delete_message(message.chat.id, message.message_id)
