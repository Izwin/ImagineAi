import base64
from dalle2 import Dalle2
import telebot
from telebot import types
from urlextract import URLExtract
from PIL import Image
import urllib.request
from craiyon import Craiyon

API_KEY = "5497414946:AAFByjMLiHy9xnKtzFv9I2CftSqglQT7gtY"
bot = telebot.TeleBot(API_KEY)
promt = ""



def premiumFetch(text,message):
    dalle = Dalle2("sess-4zmYspys77WdJzzNDHUpkge1dzzNgvcnmFGLg3tJ")
    # generations = "[{'id': 'generation-dzhcmR2LalasPDo7CgZj1hMo', 'object': 'generation', 'created': 1664663337, 'generation_type': 'ImageGeneration', 'generation': {'image_path': 'https://openailabsprodscus.blob.core.windows.net/private/user-nbNYezsfYe3edbZMyrqUfVEZ/generations/generation-dzhcmR2LalasPDo7CgZj1hMo/image.webp?st=2022-10-01T21%3A29%3A59Z&se=2022-10-01T23%3A27%3A59Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/webp&skoid=15f0b47b-a152-4599-9e98-9cb4a58269f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-10-01T21%3A44%3A09Z&ske=2022-10-08T21%3A44%3A09Z&sks=b&skv=2021-08-06&sig=KG8zUiWF0jqyy2tLNnbljwA8TZaWo1zORtFgS36O2Gk%3D'}, 'task_id': 'task-cCwKFnNliqIcjjrWABIh0izU', 'prompt_id': 'prompt-YyjnI8xWWtMphrvTu40dDo7V', 'is_public': False}, {'id': 'generation-u3ZvTHb2cRQUd3rkEH1zpR2L', 'object': 'generation', 'created': 1664663337, 'generation_type': 'ImageGeneration', 'generation': {'image_path': 'https://openailabsprodscus.blob.core.windows.net/private/user-nbNYezsfYe3edbZMyrqUfVEZ/generations/generation-u3ZvTHb2cRQUd3rkEH1zpR2L/image.webp?st=2022-10-01T21%3A29%3A59Z&se=2022-10-01T23%3A27%3A59Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/webp&skoid=15f0b47b-a152-4599-9e98-9cb4a58269f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-10-01T21%3A44%3A09Z&ske=2022-10-08T21%3A44%3A09Z&sks=b&skv=2021-08-06&sig=meJovjdQ9or3977aUGwviNkULEFYj6ARWPxT3cHDVXw%3D'}, 'task_id': 'task-cCwKFnNliqIcjjrWABIh0izU', 'prompt_id': 'prompt-YyjnI8xWWtMphrvTu40dDo7V', 'is_public': False}, {'id': 'generation-kUR1lWQdZVvBAduAjC3TjfGH', 'object': 'generation', 'created': 1664663337, 'generation_type': 'ImageGeneration', 'generation': {'image_path': 'https://openailabsprodscus.blob.core.windows.net/private/user-nbNYezsfYe3edbZMyrqUfVEZ/generations/generation-kUR1lWQdZVvBAduAjC3TjfGH/image.webp?st=2022-10-01T21%3A29%3A59Z&se=2022-10-01T23%3A27%3A59Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/webp&skoid=15f0b47b-a152-4599-9e98-9cb4a58269f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-10-01T21%3A44%3A09Z&ske=2022-10-08T21%3A44%3A09Z&sks=b&skv=2021-08-06&sig=58UjTlByd1n8jJ1SGn9eP9%2BtZnqVsdUoXbPEDRR/2ME%3D'}, 'task_id': 'task-cCwKFnNliqIcjjrWABIh0izU', 'prompt_id': 'prompt-YyjnI8xWWtMphrvTu40dDo7V', 'is_public': False}, {'id': 'generation-hPFKM8pSr7J0XkEi5WYNbgrv', 'object': 'generation', 'created': 1664663337, 'generation_type': 'ImageGeneration', 'generation': {'image_path': 'https://openailabsprodscus.blob.core.windows.net/private/user-nbNYezsfYe3edbZMyrqUfVEZ/generations/generation-hPFKM8pSr7J0XkEi5WYNbgrv/image.webp?st=2022-10-01T21%3A29%3A59Z&se=2022-10-01T23%3A27%3A59Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/webp&skoid=15f0b47b-a152-4599-9e98-9cb4a58269f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-10-01T21%3A44%3A09Z&ske=2022-10-08T21%3A44%3A09Z&sks=b&skv=2021-08-06&sig=QzH3rxZzsXTMcC3m5cmk01J8n6kulyjflwXoIqRm3wA%3D'}, 'task_id': 'task-cCwKFnNliqIcjjrWABIh0izU', 'prompt_id': 'prompt-YyjnI8xWWtMphrvTu40dDo7V', 'is_public': False}]"
    generations = dalle.generate(text)


    extractor = URLExtract()
    urls = extractor.find_urls(str(generations))

    list = []
    for i in urls:
        with urllib.request.urlopen(i) as url:
            img = Image.open(url)
            image = telebot.types.InputMediaPhoto(img)
            list.append(image)

    bot.send_media_group(message.chat.id, list)

def isPromt(text):
    if "Imagine," in text:
        return True
    return False

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
    result.save_images()  # Saves the generated images to 'current working directory/generated', you can also provide a custom path


@bot.message_handler(commands=['start'])
def greet(message):
    mes = f'Привет, <b>{message.from_user.first_name}</b>! Пришли мне любой текст в формате: Imagine, ..., и я переведу его в картинку! Создатели: @raufkhalilov @sheluvsshmmookyyy'
    bot.send_message(message.chat.id, mes, parse_mode="html")



@bot.message_handler(content_types="text")
def handleText(message):
    global promt

    if message.text == "Бесплатно":
        bot.send_message(message.chat.id, "Ваш запрос отправлен!")
        print(promt)
        freeFetch(promt, message)

    elif message.text == "Платно":
        bot.send_message(message.chat.id, "Ваш запрос отправлен!")
        premiumFetch(promt, message)
    if (isPromt(message.text)):

        text = str(message.text).replace("Imagine, ","")
        promt = text


        createMenu(message)


def createMenu(message):
    print("createMenu")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    free = types.KeyboardButton("Бесплатно")
    paid = types.KeyboardButton("Платно")
    markup.add(free)
    markup.add(paid)
    bot.send_message(message.chat.id, text="Выберите способ", reply_markup=markup)


print("HELLO WORLD!!!))))))))))))))))))))")
bot.infinity_polling()
