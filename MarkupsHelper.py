from telebot import types

import Constants
import SQLiteService


def createMarkupMain(inlineMessageId, username, chatId):
    markup = types.InlineKeyboardMarkup(row_width=2)
    lang = SQLiteService.getUserLanguage(chatId)
    callback_data = "/" + str(inlineMessageId) + "/" + str(username) + "/" + str(chatId) + "/" + str(chatId)
    credits = types.InlineKeyboardButton(Constants.MY_CREDITS[lang],
                                         callback_data=Constants.CREDITS_INLINE + callback_data)
    buy_credits = types.InlineKeyboardButton(Constants.BUY_CREDITS[lang],
                                             callback_data=Constants.BUY_CREDITS_INLINE + callback_data)
    promts = types.InlineKeyboardButton(Constants.EXAMPLES_PROMTS[lang],
                                        callback_data=Constants.PROMPTS_INLINE + callback_data)
    support = types.InlineKeyboardButton(Constants.SUPPORT[lang],
                                         callback_data=Constants.SUPPORT_INLINE + callback_data)

    selectLanguage = types.InlineKeyboardButton(Constants.SELECT_LANGUAGE[lang],
                                         callback_data=Constants.SELECT_INLINE + callback_data)

    ad = types.InlineKeyboardButton("Анонимный чат",
                                         "https://t.me/Anononimuschat_bot")

    markup.add(credits, buy_credits, promts, support,selectLanguage,ad)
    return markup


def createMarkupSelectMenu(inlineMessageId, username, chatId):
    callback_data = "/" + str(inlineMessageId) + "/" + str(username) + "/" + str(chatId) + "/" + str(chatId)

    lang = SQLiteService.getUserLanguage(chatId)

    markup = types.InlineKeyboardMarkup(row_width=1)

    free = types.InlineKeyboardButton(Constants.FREE[lang], callback_data=Constants.FREE_INLINE + callback_data)
    paid = types.InlineKeyboardButton(Constants.PAID[lang], callback_data=Constants.PAID_INLINE + callback_data)
    openArt = types.InlineKeyboardButton(Constants.OPENART[lang], callback_data=Constants.OPENART_INLINE + callback_data)

    markup.add(free, openArt, paid)

    return markup

def createLanguageSelectMenu(inlineMessageId, username, chatId):
    callback_data = "/" + str(inlineMessageId) + "/" + str(username) + "/" + str(chatId) + "/" + str(chatId)

    markup = types.InlineKeyboardMarkup(row_width=1)

    russian= types.InlineKeyboardButton(Constants.RUSSIAN, callback_data=Constants.RUSSIAN_INLINE + callback_data)
    english = types.InlineKeyboardButton(Constants.ENGLISH, callback_data=Constants.ENGLISH_INLINE + callback_data)

    markup.add(russian, english)

    return markup
