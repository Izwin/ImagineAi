import asyncio
import shutil
import urllib

import requests
from threading import Timer

from googletrans import Translator
import telebot
from telebot.async_telebot import AsyncTeleBot
import telebot.asyncio_filters
from telebot import types
from PIL import Image
import logging

from Fetch.Fetch import freeFetch, premiumFetch
from Resources.Constants import Ranks
from Resources.Constants.ConstantMessages import *
import SQLite.SQLiteService

bot = telebot.TeleBot(API_KEY)

isPiar = False

chat_id = -1288868326
analytics = -850186193
kerim_chat_id = 392831022
steel_chat_id = -708812702
channel_id = -1001700593611

temp_message = telebot.types.Message(1,None,None,None,None,"",None)
bot_message= 0
prompt = ""


# link1 = "https://openailabsprodscus.blob.core.windows.net/private/user-nbNYezsfYe3edbZMyrqUfVEZ/generations/generation-c5ePFkJKiQ8m6ICNHlWCJoC9/image.webp?st=2022-10-03T14%3A17%3A04Z&se=2022-10-03T16%3A15%3A04Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/webp&skoid=15f0b47b-a152-4599-9e98-9cb4a58269f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-10-03T14%3A40%3A27Z&ske=2022-10-10T14%3A40%3A27Z&sks=b&skv=2021-08-06&sig=zbxB8fKtgbhY5Rm3iBQn4ocTJTp3OhiITQsRPxK0hqI%3D"
#
# list = []
# list1 = []
#
# list1.append(link1)
# list1.append(link1)
#
# # res = requests.get(link, stream = True)
# # if res.status_code == 200:
# #     with open("temp.webp",'wb') as f:
# #         shutil.copyfileobj(res.raw, f)
# #     print('Image sucessfully Downloaded: ',"temp.webp")
# # else:
# #     print('Image Couldn\'t be retrieved')
#
# #SQLite.SQLiteService.increaseCredits(741168747)
#
# for link in list1:
#     print(link)
#     res = requests.get(link, stream=True)
#     if res.status_code == 200:
#         with open("temp.webp", 'wb') as f:
#             shutil.copyfileobj(res.raw, f)
#         print('Image sucessfully Downloaded: ', "temp.webp")
#         img = open("temp.webp", "rb")
#         image = telebot.types.InputMediaPhoto(img)
#         list.append(image)
#     else:
#         print('Image Couldn\'t be retrieved')
#
#
# bot.send_media_group(741168747, list)
# bot.send_message(741168747, AFTER_RESULT)
#
#
#
# # bot.send_photo(741168747, open('C:\\Users\\zaman\\Desktop\\image1.webp', 'rb'))
#
# # bot.send_photo(741168747, open('temp.webp', 'rb'))
#
# SQLite.SQLiteService.increaseCredits(-1694667913)
#


@bot.message_handler(commands=['start'])
def startHandler(message):
    global temp_message
    temp_message = message
    SQLite.SQLiteService.AddUser(message.chat.id, 1, message.from_user.username)
    try:
        sendAnalytics(message, message.from_user.username + " " + " написал команду /start")
    except Exception as e:
        print("Send to analytics error")
    createStartMenu(message)



@bot.message_handler(commands=['stat'])
def startHandler(message):
    global temp_message
    temp_message = message
    if message.chat.id == analytics:
        sendAnalytics(message, f"всего {len(SQLite.SQLiteService.getAllChatIds())} участников")


@bot.message_handler(commands=['imagine'])
def imagineHandler(message):
    global prompt, temp_message
    temp_message = message
    steelMessage(message)
    # bot.forward_message(steel_chat_id, message.chat.id, message.message_id)

    if message.text == "/imagine" or message.text == "/imagine@imagineai_bot":

        sendAndDeleteMessage(bot.send_message(message.chat.id, REQUEST_NOT_CORRECT, parse_mode="html"))
        sendAndDeleteMessage(message)
        return
    text = str(message.text).replace("/imagine ", "")

    if "@imagineai_bot" in text:
        text = text.replace("@imagineai_bot", "")

    try:
        translator = Translator()
        prompt = translator.translate(text).text

    except:
        prompt = text
    selectModeMenu(message)


@bot.message_handler(commands=['piar'])
def imagineHandler(message):
    global promt, isPiar, temp_message
    temp_message = message
    if message.chat.id == kerim_chat_id:
        isPiar = True


@bot.callback_query_handler(func=lambda call: call.data in ['credits', 'free_method','paid_method','buy_credits','support','requests'])
def callback_query(call):
    global prompt
    print(prompt)
    markup = types.InlineKeyboardMarkup()
    credits = types.InlineKeyboardButton(MY_CREDITS, callback_data="credits")
    buy_credits = types.InlineKeyboardButton(BUY_CREDITS, callback_data="buy_credits")
    requests = types.InlineKeyboardButton(EXAMPLES_PROMTS, callback_data="requests")
    support = types.InlineKeyboardButton(SUPPORT, callback_data="support")
    markup.add(credits, buy_credits, requests, support)
    if call.data == "credits":
        user_credits = SQLite.SQLiteService.GetUserCredits(temp_message.chat.id)


        bot.edit_message_text("У вас " + str(user_credits) + " кредитов",temp_message.chat.id,bot_message,reply_markup=markup)
    elif call.data == "buy_credits":
        bot.edit_message_text(BUY_CREDITS_ANS, temp_message.chat.id,bot_message,reply_markup=markup)
    elif call.data == "support":
        bot.edit_message_text(SUPPORT_ANS, temp_message.chat.id,bot_message,parse_mode="html",reply_markup=markup)
    elif call.data == "requests":
        f = open("Resources/Constants/Prompts.txt", "r", encoding="utf-8")
        bot.edit_message_text(f.read(), temp_message.chat.id,bot_message,parse_mode="html",reply_markup=markup)
    elif call.data == "free_method":
        print(prompt)

        if len(prompt) < 2:
            bot.edit_message_text(REQUEST_NOT_CORRECT, temp_message.chat.id, bot_message, parse_mode="html", reply_markup=markup)
            return
        # try:
        #     print(bot.get_chat_member("@domlorda", message.from_user.id).status)
        #     if bot.get_chat_member("@domlorda", message.from_user.id).status not in Ranks.Roles:
        #         raise Exception
        #
        # except Exception as e:
        #     print(e)
        #     bot.send_message(message.chat.id, "Вы не подписаны")
        #     return
        deleteMessage(bot.edit_message_text(REQUEST_SENDED, temp_message.chat.id, bot_message, parse_mode="html", reply_markup=markup))

        sendAnalytics(temp_message, temp_message.from_user.username + " бесплатный запрос " + prompt)
        temp = prompt
        promt = ""
        freeFetch(temp, temp_message)
    elif call.data == "paid_method":
        if len(prompt) < 2:
            bot.edit_message_text(REQUEST_NOT_CORRECT, temp_message.chat.id, bot_message, parse_mode="html", reply_markup=markup)
            return
        user_credits = SQLite.SQLiteService.GetUserCredits(temp_message.chat.id)
        print(user_credits)
        if user_credits > 0:
            SQLite.SQLiteService.decreaseCredits(temp_message.chat.id)
            sendAndDeleteMessage(bot.edit_message_text(REQUEST_SENDED, temp_message.chat.id, bot_message, parse_mode="html", reply_markup=markup))
            sendAnalytics(temp_message, temp_message.from_user.username + " платный запрос " + prompt)

            temp = prompt
            promt = ""
            premiumFetch(temp, temp_message)
        else:
            bot.edit_message_text(NO_CREDITS, temp_message.chat.id, bot_message, parse_mode="html", reply_markup=markup)


@bot.message_handler(content_types="text")
def textHandler(message):
    global temp_message

    SQLite.SQLiteService.AddUser(message.chat.id, 1, message.from_user.username)
    try:
        steelMessage(message)
    except Exception as e:
        print(e)
        print("Forward Error")

    global promt, isPiar, chat_id
    if message.chat.id == channel_id:
        list = SQLite.SQLiteService.getAllChatIds()
        for i in list:
            try:
                bot.forward_message(i[0], message.chat.id, message.message_id)
            except:
                SQLite.SQLiteService.removeByChatId(message.chat.id)
                print("Forward Message Error")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    credits = types.KeyboardButton(MY_CREDITS)
    buy_credits = types.KeyboardButton(BUY_CREDITS)
    requests = types.KeyboardButton(EXAMPLES_PROMTS)
    support = types.KeyboardButton(SUPPORT)
    markup.add(credits, buy_credits, requests, support)
    if message.text == FREE:
        if len(promt) < 2:
            bot.send_message(message.chat.id, REQUEST_NOT_CORRECT, parse_mode="html")
            return
        # try:
        #     print(bot.get_chat_member("@domlorda", message.from_user.id).status)
        #     if bot.get_chat_member("@domlorda", message.from_user.id).status not in Ranks.Roles:
        #         raise Exception
        #
        # except Exception as e:
        #     print(e)
        #     bot.send_message(message.chat.id, "Вы не подписаны")
        #     return
        bot.send_message(message.chat.id, REQUEST_SENDED, reply_markup=markup)
        print("Promt")
        sendAnalytics(message, message.from_user.username + " бесплатный запрос " + promt)
        temp = promt
        promt = ""
        freeFetch(temp, message)
    elif message.text == PAID:
        if len(promt) < 2:
            bot.send_message(message.chat.id, REQUEST_NOT_CORRECT, parse_mode="html")
            return
        user_credits = SQLite.SQLiteService.GetUserCredits(message.chat.id)
        print(user_credits)
        if user_credits > 0:
            SQLite.SQLiteService.decreaseCredits(message.chat.id)
            bot.send_message(message.chat.id, REQUEST_SENDED, reply_markup=markup)
            sendAnalytics(message, message.from_user.username + " платный запрос " + promt)

            temp = promt
            promt = ""
            premiumFetch(temp, message)
        else:
            bot.send_message(message.chat.id, NO_CREDITS, reply_markup=markup)


    elif message.text == EXAMPLES_PROMTS:
        f = open("Resources/Constants/Prompts.txt", "r", encoding="utf-8")
        bot.send_message(message.chat.id, f.read(), parse_mode="html")

    elif message.text == MY_CREDITS:
        user_credits = SQLite.SQLiteService.GetUserCredits(message.chat.id)
        bot.send_message(message.chat.id, "У вас " + str(user_credits) + " кредитов")

    elif message.text == BUY_CREDITS:
        bot.send_message(message.chat.id, BUY_CREDITS_ANS)

    elif message.text == SUPPORT:
        bot.send_message(message.chat.id, SUPPORT_ANS)

    else:
        if not channel_id == message.chat.id:
            if not message.chat.type == "group" and not message.chat.type == "supergroup":
                sendAndDeleteMessage(bot.send_message(message.chat.id, REQUEST_NOT_CORRECT, parse_mode="html"))
                sendAndDeleteMessage(message)


@bot.message_handler(
    content_types=['document', 'audio', 'photo', 'video', 'animation', 'gif', 'sticker', 'voice', 'poll', 'contact',
                   'video_note'])
def photoHandler(message):
    global temp_message
    temp_message = message
    steelMessage(message)
    if message.chat.id == channel_id:
        list = SQLite.SQLiteService.getAllChatIds()
        for i in list:
            try:
                bot.forward_message(i[0], message.chat.id, message.message_id)
            except Exception as e:
                SQLite.SQLiteService.removeByChatId(message.chat.id)


def selectModeMenu(message):
    global bot_message
    markup = types.InlineKeyboardMarkup()
    free = types.InlineKeyboardButton(FREE,callback_data = "free_method")
    paid = types.InlineKeyboardButton(PAID,callback_data = "paid_method")
    markup.add(free)
    markup.add(paid)
    bot_message = bot.send_message(message.chat.id, text="Выберите способ", reply_markup=markup).message_id


def createStartMenu(message):
    global bot_message

    list = []
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/paid.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/paid2.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/free.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/free2.jpg")))
    bot.send_media_group(message.chat.id, list)

    startMessage = f'Привет, <b>{message.from_user.first_name}</b>!\n\n' \
                   f'Пришли мне любой запрос состоящий из текста через Imagine (Imagine, ваш текст)\n\n' \
                   f'Запросы желательно !\n\n' \
                   f'Пример запроса: <b><i>/imagine *ваш запрос*</i></b>'

    markup = types.InlineKeyboardMarkup()
    credits = types.InlineKeyboardButton(MY_CREDITS, callback_data="credits")
    buy_credits = types.InlineKeyboardButton(BUY_CREDITS, callback_data="buy_credits")
    requests = types.InlineKeyboardButton(EXAMPLES_PROMTS, callback_data="requests")
    support = types.InlineKeyboardButton(SUPPORT, callback_data="support")
    markup.add(credits, buy_credits, requests, support)
    bot_message = bot.send_message(message.chat.id, startMessage, reply_markup=markup, parse_mode="html").message_id


def steelMessage(message):
    # if message.from_user.username in ADMINS:
    #     return
    try:
        print(message)
        chat = message.chat.title + " "
    except:
        chat = ""
    # stroka = "@" + message.from_user.username + " | " + message.from_user.first_name + " в " + chat + ": " + message.text
    bot.forward_message(steel_chat_id, message.chat.id, message.message_id)


def sendAnalytics(message, text):
    bot.send_message(analytics, text)

def sendAndDeleteMessage(message):
    t = Timer(5,deleteMessage,[message])
    t.start()


def deleteMessage(message):
    bot.delete_message(message.chat.id, message.message_id)
bot.infinity_polling()
