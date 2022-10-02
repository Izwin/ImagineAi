import base64
from googletrans import Translator
from dalle2 import Dalle2
import telebot
from telebot import types
from urlextract import URLExtract
from PIL import Image
import urllib.request

from Fetch.Fetch import freeFetch, premiumFetch
from Utill.UrlExtractor import *
from Constants.constansts import *
from craiyon import Craiyon

bot = telebot.TeleBot(API_KEY)

promt = ""


@bot.message_handler(commands=['start'])
def startHandler(message):
    createStartMenu(message)
    list = []
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/paid.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/paid2.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/free.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/free2.jpg")))
    bot.send_media_group(message.chat.id, list)


@bot.message_handler(commands=['imagine'])
def imagineHandler(message):
    global promt

    if message.text == "/imagine" or message.text == "/imagine@imagineai_bot":
        bot.send_message(message.chat.id, REQUEST_NOT_CORRECT, parse_mode="html")
        return
    text = str(message.text).replace("/imagine ", "")

    if "@imagineai_bot" in text:
        text = text.replace("@imagineai_bot", "")

    translator = Translator()
    promt = translator.translate(text).text

    selectModeMenu(message)


@bot.message_handler(content_types="text")
def textHandler(message):
    global promt
    if message.text == FREE:
        bot.send_message(message.chat.id, REQUEST_SENDED)
        print(promt)
        freeFetch(promt, message)

    elif message.text == PAID:
        bot.send_message(message.chat.id, REQUEST_SENDED)
        print(promt)
        print(message)
        premiumFetch(promt, message)

    elif message.text == EXAMPLES_PROMTS:
        f = open("Constants/requirements.txt", "r", encoding="utf-8")
        bot.send_message(message.chat.id, f.read(), parse_mode="html")

    elif message.text == MY_CREDITS:
        bot.send_message(message.chat.id, "У вас 0 кредитов")

    elif message.text == BUY_CREDITS:
        bot.send_message(message.chat.id, BUY_CREDITS_ANS)

    elif message.text == SUPPORT:
        bot.send_message(message.chat.id, SUPPORT_ANS)



@bot.message_handler(content_types="photo")
def photoHandler(message):
    bot.forward_message(-812810983, message.chat.id, message.message_id)


def selectModeMenu(message):
    print("createMenu")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    free = types.KeyboardButton(FREE)
    paid = types.KeyboardButton(PAID)
    markup.add(free)
    markup.add(paid)
    bot.send_message(message.chat.id, text="Выберите способ", reply_markup=markup)


def createStartMenu(message):
    startMessage = f'Привет, <b>{message.from_user.first_name}</b>!\n\n' \
                   f'Пришли мне любой запрос состоящий из текста через Imagine (Imagine, ваш текст)\n\n' \
                   f'Пример запроса:  "Imagine, сюрреалистическая сказочная картина маслом Сальвадора Дали, изображающая кошку, играющую в шашки». (Платная/Бесплатная)'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    credits = types.KeyboardButton(MY_CREDITS)
    buy_credits = types.KeyboardButton(BUY_CREDITS)
    requests = types.KeyboardButton(EXAMPLES_PROMTS)
    support = types.KeyboardButton(SUPPORT)
    markup.add(credits, buy_credits, requests, support)
    bot.send_message(message.chat.id, startMessage, reply_markup=markup, parse_mode="html")


print("st0art")
bot.infinity_polling()
