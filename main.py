# pip install requests beautifulsoup4 pytelegrambotapi

import requests, telebot
from telebot import types
from bs4 import BeautifulSoup as bs


bot = telebot.TeleBot('...')
URL = 'https://habr.com/ru/news/'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/showNews'))
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}!',
        reply_markup=markup
    )


@bot.message_handler(commands=['showNews'])
def show_data(message):
    req = bs(requests.get(URL).text, 'html.parser')
    text = ''
    for link in req.find_all('a', class_='tm-article-snippet__title-link'):
        text += f'{link.text} https://habr.com{link.get("href")}\n'
    bot.send_message(
        chat_id=message.chat.id,
        text=text
    )


bot.polling(none_stop=True)
