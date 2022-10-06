from telebot import types

import Constants


def createMarkupMain(inlineMessageId, username, chatId):
    markup = types.InlineKeyboardMarkup(row_width=2)
    callback_data = "/" + str(inlineMessageId) + "/" + str(username) + "/" + str(chatId) + "/" + str(chatId)
    credits = types.InlineKeyboardButton(Constants.MY_CREDITS,
                                         callback_data=Constants.CREDITS_INLINE + callback_data)
    buy_credits = types.InlineKeyboardButton(Constants.BUY_CREDITS,
                                             callback_data=Constants.BUY_CREDITS_INLINE + callback_data)
    promts = types.InlineKeyboardButton(Constants.EXAMPLES_PROMTS,
                                        callback_data=Constants.PROMPTS_INLINE + callback_data)
    support = types.InlineKeyboardButton(Constants.SUPPORT,
                                         callback_data=Constants.SUPPORT_INLINE + callback_data)

    markup.add(credits, buy_credits, promts, support)
    return markup


def createMarkupSelectMenu(inlineMessageId, username, chatId):
    callback_data = "/" + str(inlineMessageId) + "/" + str(username) + "/" + str(chatId) + "/" + str(chatId)

    markup = types.InlineKeyboardMarkup(row_width=2)

    free = types.InlineKeyboardButton(Constants.FREE, callback_data=Constants.FREE_INLINE + callback_data)
    paid = types.InlineKeyboardButton(Constants.PAID, callback_data=Constants.PAID_INLINE + callback_data)

    markup.add(free, paid)

    return markup
