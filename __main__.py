import os
import math
import random
import tempfile
import requests
from dotenv import load_dotenv
import telebot
from PIL import Image

TONES = [
    lambda: '█',
    lambda: '▓',
    lambda: '▒',
    lambda: '░',
    lambda: '.'
]
MAX_IMAGE_SIZE = 30

load_dotenv()
bot = telebot.TeleBot(os.environ['BOT_TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Hello I\'m UTPhoto bot! I can turn your photo into an UTF art! " +
        "Just send a photo to me and you will get a result."
    )


@bot.message_handler(func=lambda message: True)
def reply_to_invalid_command(message):
    bot.send_message(
        message.chat.id, 'I don\'t undarstand you! Try typing /help.')


@bot.message_handler(content_types=['photo'])
def send_UTF_art(message):
    file_id = message.photo[0].file_id
    photo_telegram_file = bot.get_file(file_id)
    response = requests.get(
        f'https://api.telegram.org/file/bot{bot.token}/{photo_telegram_file.file_path}'
    )
    image_tempfile = tempfile.TemporaryFile()
    image_tempfile.write(response.content)
    image = Image.open(image_tempfile)
    if image.height > image.width:
        new_height = MAX_IMAGE_SIZE
        new_width = math.ceil(MAX_IMAGE_SIZE * image.width / image.height)
    else:
        new_width = MAX_IMAGE_SIZE
        new_height = math.ceil(MAX_IMAGE_SIZE * image.height / image.width)

    image = image.resize((new_width, new_height))
    result = '```'
    for row in range(image.height):
        for column in range(image.width):
            chanels = image.getpixel((column, row))
            gray = (max(chanels) + min(chanels)) / 2
            level = math.ceil(gray / 255 * len(TONES)) - 1
            result += TONES[level]() * 2

        result += '\n'

    result += '```'
    bot.send_message(message.chat.id, result, parse_mode='MarkdownV2')

bot.infinity_polling()
