import os
import urllib
import numpy
from dotenv import load_dotenv
import telebot
import cv2

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
    request = urllib.request.urlopen(
        f'https://api.telegram.org/file/bot{bot.token}/{photo_telegram_file.file_path}'
    )
    array = numpy.asarray(bytearray(request.read()), dtype=numpy.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_GRAYSCALE)
    print(type(image))
    print(image.shape)

bot.infinity_polling()
