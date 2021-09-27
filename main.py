import telebot
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime

bot = telebot.TeleBot('А вот я прям и выложил его токен', parse_mode=None)

@bot.message_handler(commands=['start'])
def intro(message):
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}."
                                      " Для того, чтобы узнать погоду на сегодня, выбери город".format(message.from_user, bot.get_me()))

@bot.message_handler(commands=['info'])
def narw(message):
    a = requests.get('https://sinoptik.ua/погода-москва')
    html1 = BS(a.content, 'html.parser')
    for el in html1.select('#content'):
        date = el.select('.day-link')[0].text
        trash = el.select('.oDescription .description')[0].text
        current_date = str(datetime.now().date())
        bot.send_message(message.chat.id, "Сегодня" + '\n' + current_date + '\n' + date + '\n' + trash)

@bot.message_handler(content_types=['text'])
def definition(message):
    url='https://sinoptik.ua/погода-{}'.format(str.lower(message.text))
    print(url)
    r = requests.get(url)
    html = BS(r.content, 'html.parser')
    for el in html.select('#content'):
        date = el.select('.day-link')[0].text
        t_min = el.select('.temperature .min')[0].text
        t_max = el.select('.temperature .max')[0].text
        description = el.select('.wDescription .description')[0].text
        current_date = str(datetime.now().date())
        bot.send_message(message.chat.id,
                     "\nПрогноз погоды на :\n" + date + '\n' + current_date
                     + '\n' + t_min + ', ' + t_max + '\n' + '\n' + description + '\n')


bot.polling(none_stop=True)
