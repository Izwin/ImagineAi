import asyncio
import json
import time
from threading import Timer

import telebot
from PIL import Image
from googletrans import Translator

from telebot import types

import ChatIds
import Constants
import Fetch
import MarkupsHelper
import SQLiteService
from Fetch import freeFetch, premiumFetch
from MarkupsHelper import *

bot = telebot.TeleBot(Constants.API_KEY)

request = ""

@bot.message_handler(commands=['start'])
def startCommand(message):
    SQLiteService.addUser(message.chat.id, 1, message.from_user.username)
    try:
        sendAnalytics(message.from_user.username + " " + " написал команду /start")
    except Exception as e:
        print("Send to analytics error")
    createStartMenu(message)


@bot.message_handler(
    content_types=['document', 'audio', 'photo', 'video', 'animation', 'gif', 'sticker', 'voice', 'poll', 'contact',
                   'video_note'])
def photoHandler(message):
    steelMessage(message)
    checkForChannelId(message)


@bot.message_handler(commands=['stat'])
def startHandler(message):
    if message.chat.id == ChatIds.analytics:
        sendAnalytics(f"всего {len(SQLiteService.getAllChatIds())} участников")


@bot.message_handler(commands=['imagine'])
def imagineHandler(message):
    global request
    steelMessage(message)

    if message.text == "/imagine" or message.text == "/imagine@imagineai_bot":
        sendAndDeleteMessage(bot.send_message(message.chat.id, Constants.REQUEST_NOT_CORRECT[lang], parse_mode="html"))
        sendAndDeleteMessage(message)
        return
    text = str(message.text).replace("/imagine ", "")

    if "@imagineai_bot" in text:
        text = text.replace("@imagineai_bot", "")

    try:
        translator = Translator()
        request = translator.translate(text).text

    except:
        request = text
    selectModeMenu(message)


@bot.message_handler(content_types="text")
def textHandler(message):
    global promt
    lang = SQLiteService.getUserLanguage(message.chat.id)
    SQLiteService.addUser(message.chat.id, 1, message.from_user.username)

    steelMessage(message)
    checkForChannelId(message)

    if not message.chat.type == "group" and not message.chat.type == "supergroup":
        sendAndDeleteMessage(bot.send_message(message.chat.id, Constants.REQUEST_NOT_CORRECT[lang], parse_mode="html"))
        sendAndDeleteMessage(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global request
    tempCallData = str(call.data)
    callList = str(call.data).split("/")
    call.data = callList;


    try:
        botMessageId = call.data[1]
        userName = call.data[2]
        userChatId = call.data[3]
        botMessageChatId = call.data[4]
        lang = SQLiteService.getUserLanguage(botMessageChatId)

    except:
        print("Error")

    markup = createMarkupMain(botMessageId, userName, botMessageChatId)

    if call.data[0] == Constants.CREDITS_INLINE:
        user_credits = SQLiteService.getUserCredits(userChatId)

        try:
            if lang == "ru":
                bot.edit_message_text("У вас " + str(user_credits) + " генераций", botMessageChatId,
                                      botMessageId,
                                      reply_markup=markup)
            elif lang == "en":
                bot.edit_message_text("You have " + str(user_credits) + " generations", botMessageChatId,
                                      botMessageId,
                                      reply_markup=markup)

        except:
            print("")
    elif call.data[0] == Constants.BUY_CREDITS_INLINE:

        bot.edit_message_text(Constants.BUY_CREDITS_ANS[lang], botMessageChatId, botMessageId,
                              reply_markup=markup)
    elif call.data[0] == Constants.SUPPORT_INLINE:
        bot.edit_message_text(Constants.SUPPORT_ANS[lang], botMessageChatId, botMessageId, parse_mode="html",
                              reply_markup=markup)
    elif call.data[0] == Constants.PROMPTS_INLINE:
        f = open("Resources/Constants/Prompts.txt", "r", encoding="utf-8")
        bot.edit_message_text(f.read(), botMessageChatId, botMessageId, parse_mode="html",
                              reply_markup=markup)

    elif call.data[0] == Constants.FREE_INLINE:

        if len(request) < 2:
            sendAndDeleteMessage(
                bot.edit_message_text(Constants.REQUEST_NOT_CORRECT[lang], botMessageChatId, botMessageId,
                                      parse_mode="html"))
            return
        messageForResult = bot.edit_message_text(Constants.REQUEST_SENDED[lang], botMessageChatId, botMessageId,
                                                 parse_mode="html",
                                                 reply_markup=markup)

        sendAnalytics(userName + " бесплатный запрос " + request)
        tempRequest = request
        request = ""
        SQLiteService.lastQuery(userChatId, tempRequest)
        freeFetch(tempRequest, messageForResult, userName)

    elif call.data[0] == Constants.PAID_INLINE:
        print("sdf")
        if len(request) < 2:
            sendAndDeleteMessage(
                bot.edit_message_text(Constants.REQUEST_NOT_CORRECT[lang], botMessageChatId, botMessageId,
                                      parse_mode="html"))
            return
        user_credits = SQLiteService.getUserCredits(userChatId)
        if user_credits > 0:

            SQLiteService.decreaseCredits(userChatId)

            messageForResult = bot.edit_message_text(Constants.REQUEST_SENDED[lang], botMessageChatId, botMessageId,
                                                     parse_mode="html",
                                                     reply_markup=markup)

            sendAnalytics(userName + " платный запрос " + request)

            tempRequest = request
            request = ""
            SQLiteService.lastQuery(userChatId, tempRequest)
            premiumFetch(tempRequest, messageForResult, userName)
        else:
            bot.edit_message_text(Constants.NO_CREDITS, userChatId, botMessageId, parse_mode="html",
                                  reply_markup=markup)

    elif call.data[0] == Constants.OPENART_INLINE:
        if len(request) < 2:
            sendAndDeleteMessage(
                bot.edit_message_text(Constants.REQUEST_NOT_CORRECT[lang], botMessageChatId, botMessageId,
                                      parse_mode="html"))
            return

        messageForResult = bot.edit_message_text(Constants.REQUEST_SENDED[lang], botMessageChatId, botMessageId,
                                                 parse_mode="html",
                                                 reply_markup=markup)

        sendAnalytics(userName + " openart запрос " + request)

        tempRequest = request
        request = ""
        SQLiteService.lastQuery(userChatId, tempRequest)
        Fetch.openArt(tempRequest, messageForResult, userName)


    elif call.data[0] == Constants.SELECT_INLINE:
        print(lang)
        bot.edit_message_text(Constants.CHOOSE_LANGUAGE[lang], botMessageChatId, botMessageId)
        markup = MarkupsHelper.createLanguageSelectMenu(botMessageId, userName, botMessageChatId)
        bot.edit_message_reply_markup(botMessageChatId, botMessageId, reply_markup=markup)
    elif call.data[0] == Constants.RUSSIAN_INLINE:
        SQLiteService.setLanguage(botMessageChatId,"ru")
        bot.edit_message_text(Constants.LANGUAGE_CHANGED["ru"],botMessageChatId,botMessageId)
    elif call.data[0] == Constants.ENGLISH_INLINE:
        SQLiteService.setLanguage(botMessageChatId,"en")
        bot.edit_message_text(Constants.LANGUAGE_CHANGED["en"],botMessageChatId,botMessageId)



def createStartMenu(message):
    list = []
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/paid.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/paid2.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/free.jpg")))
    list.append(telebot.types.InputMediaPhoto(Image.open("Resources/ExampleImages/free2.jpg")))
    bot.send_media_group(message.chat.id, list)

    lang = SQLiteService.getUserLanguage(message.chat.id)
    startMessage = "error"
    if lang == "ru":
        startMessage = f'Привет, <b>{message.from_user.first_name}</b>!\n\n' \
                   f'Пришли мне любой запрос состоящий из текста через Imagine (Imagine, ваш текст)\n\n' \
                   f'Каждому новому пользователю выдана 1 генерация для PRO версии!\n\n' \
                   f'Пример запроса: <b><i>/imagine *ваш запрос*</i></b>'
    elif lang == "en":
        startMessage = f'Hello, <b>{message.from_user.first_name}</b>!\n\n' \
                       f'Send me any text request via Imagine (Imagine, your request)\n\n' \
                       f'Each new user is given 1 generation for the PRO version!\n\n' \
                       f'Request example: <b><i>/imagine *your request*</i></b>'

    inline_message = bot.send_message(message.chat.id, startMessage, parse_mode="html")

    markup = createMarkupMain(inline_message.message_id, message.from_user.username, message.chat.id)

    bot.edit_message_reply_markup(inline_message.chat.id, inline_message.message_id, reply_markup=markup)
    time.sleep(0.2)


def selectModeMenu(message):
    lang = SQLiteService.getUserLanguage(message.chat.id)
    print("The lang is " + lang)
    inline_message = bot.send_message(message.chat.id, text=Constants.CHOOSE_MODE[lang])
    markup = createMarkupSelectMenu(inline_message.message_id, message.from_user.username, message.chat.id)
    bot.edit_message_reply_markup(inline_message.chat.id, inline_message.message_id, reply_markup=markup)
    time.sleep(0.2)


def selectLanguageMenu(chatId, username):
    inline_message = bot.send_message(chatId, text=Constants.SELECT_LANGUAGE)
    markup = createLanguageSelectMenu(inline_message.message_id, username, chatId)
    bot.edit_message_reply_markup(inline_message.chat.id, inline_message.message_id, reply_markup=markup)
    time.sleep(0.2)


def steelMessage(message):
    print("")
    # try:
    #     try:
    #         chatTitle = message.chat.title + " "
    #     except:
    #         chatTitle = ""
    #     print(message.content_type)
    #     if message.content_type == "text":
    #         text = "@" + str(message.from_user.username) + " | " + str(message.from_user.first_name) + " в " + str(
    #             chatTitle) + ": " + str(message.text)
    #     else:
    #         text = "@" + str(message.from_user.username) + " | " + str(message.from_user.first_name) + " в " + str(
    #             chatTitle) + ": " + str(message.caption)
    #         bot.forward_message(ChatIds.steel_chat_id, message.chat.id, message.message_id)
    #     bot.send_message(ChatIds.steel_chat_id, text)
    # except:
    #     print("Ошибка при стилинге сообщений")


def sendAnalytics(text):
    bot.send_message(ChatIds.analytics, text)
    time.sleep(0.2)


def checkForChannelId(message):
    if message.chat.id == ChatIds.channel_id:
        list = SQLiteService.getAllChatIds()
        for i in list:
            try:
                bot.forward_message(i[0], message.chat.id, message.message_id)
            except Exception as e:
                print("Репост с канала вызвал Exception")


def sendAndDeleteMessage(message):
    t = Timer(5, deleteMessage, [message])
    t.start()


def deleteMessage(message):
    bot.delete_message(message.chat.id, message.message_id)


# df = "Встречайте, Стикольщик - развлекательный чат-бот, общающийся на языке стикеров! С ним можно общаться в личных " \
#      "сообщениях или добавить в групповой чат. А так же вызвать, просто написав его имя @StickerStickyBot с указанием " \
#      "текста, выбрать стикер или гифку и отправить.\n\n\nt.me/StickerStickyBot 🔥\nt.me/StickerStickyBot 🔥\nt.me/StickerStickyBot 🔥"
# bot.send_photo(1946632414,open('dog.jpg','rb'),df)
bot.infinity_polling()
