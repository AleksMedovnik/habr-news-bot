# pip install requests beautifulsoup4 pytelegrambotapi

import requests, telebot
from telebot import types
from bs4 import BeautifulSoup as bs


bot = telebot.TeleBot('5332131635:AAEv9FtOmTZY8TiZmLJ2xqa3MsEdZwz94AA')
URL = 'https://habr.com/ru/news/'


def build_menu(buttons, n_cols):
	return [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

def parser_data(url):
	req = bs(requests.get(url).text, 'html.parser')
	list_data = []
	for link in req.find_all('a', class_='tm-article-snippet__title-link'):
		list_data.append(
			types.InlineKeyboardButton(text=link.text, url=f"https://habr.com{link.get('href')}")
		)
	return list_data


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')


@bot.message_handler(content_types=["text"])
def show_data(message):
	markup = types.InlineKeyboardMarkup(build_menu(parser_data(URL), n_cols=1))
	bot.send_message(
		chat_id=message.chat.id,
		text='News from Habr',
		reply_markup=markup)


bot.polling(none_stop=True)