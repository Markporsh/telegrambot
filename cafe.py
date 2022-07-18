from encodings import utf_8
import telebot
import pyowm
import json
from telebot import types
from pyowm import OWM

owm = OWM('56636358a54b58b766012abca0f38b8e')
bot = telebot.TeleBot('5343791026:AAEDBN6xfncSe3pEp5e6WdqZbLr6Oa9vlM8')

cities = {
    'Пермь': 'Perm,Ru',
    'Москва': 'Moscow,Ru',
    'Екатеринбург': 'Ekaterenburg,Ru',
    'Казань': 'Kazan,RU',
    'Омск': 'Omsk,Ru',
    'Санкт-Питербург': 'Petersburg,Ru',
    'Уфа': 'Ufa,Ru'
}


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Доброго времени суток, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['weather'])
def weatherrr(message):
    question = 'В каком городе вы хотите узнать погоду?'
    bot.send_message(message.chat.id, question)
    bot.register_next_step_handler(message, place)
    # mess = f'Погода в городе{city}, составляет {temp}</b>'
    # bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    weatherr = types.KeyboardButton('/weather')
    citys = types.KeyboardButton('/play')
    markup.add(weatherr, citys)
    choice = 'Что будем делать? Выбор за тобой'
    bot.send_message(message.chat.id, choice, reply_markup=markup)


@bot.message_handler(commands=['play'])
def play(message):
    marksup = types.InlineKeyboardMarkup()
    eng = types.InlineKeyboardButton('eng', callback_data='eng')
    rus = types.InlineKeyboardButton('rus', callback_data='rus')
    marksup.add(eng, rus)
    play_answer = 'Круто, обожаю играть в города! На каком языке?'


def place(message):
    city = message.text
    if city in cities:
        location = cities[city]
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        weather = observation.weather
        temp = weather.temperature('celsius')
        # place = cities('city')
        replace = f'Погода в городе {city} {round(temp["temp"])} градусов'
        bot.send_message(message.chat.id, replace)
        return location, city
    else:
        bot.send_message(message.chat.id, "Я еще не знаю такого города")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'eng':
        marks_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        first = types.KeyboardButton('I start first')
        second = types.KeyboardButton('You first')
        marks_reply.add(first, second)
        bot.send_message(call.message.chat.id,
                         'Who is going first?', reply_markup=marks_reply)
    elif call.data == 'rus':
        marks_reply_rus = types.ReplyKeyboardMarkup(resize_keyboard=True)
        first_rus = types.KeyboardButton('Я начну!')
        second_rus = types.KeyboardButton('Начинай ты!')
        marks_reply_rus.add(first_rus, second_rus)
        bot.send_message(call.message.chat.id, 'Кто первый?',
                         reply_markup=marks_reply_rus)


@bot.message_handler(content_types=['text'])
def game_rus(message):
    if message.text == 'Я начну!':
        if_bot_wait_answer = bot.send_message(
            message.chat.id, 'А ты неплох, поехали! Пиши название города!')
        bot.register_next_step_handler(if_bot_wait_answer, city_game)
    elif message.text == 'Начинай ты!':
        bot.send_message(
            message.chat.id, 'К сожалению в данный момент мы не доделали дальнейшие действия бота :(')
    elif message.text == 'I start first':
        bot.send_message(
            message.chat.id, 'Wow what are boss. But new functions is not working right now. We are sorry :(')
    elif message.text == 'You first':
        bot.send_message(
            message.chat.id, 'New functions is not working right now. We are sorry :(')


def city_game(message):
    cityes_old = []
    bad_symbols = {'ъ', 'ь' "ц" "й" "ы"}
    text1 = open('города.txt', encoding='utf_8')
    cityes = []
    step = 'AI'
    for i in text1:
        cityes.append(i)
    for i in range(len(cityes)):
        if cityes[i][-1] == '/n':
            cityes = cityes[i][:-1]
    cityes_all = cityes.copy()
    game_over = False
    city = message.text
    if city in set(cityes_all):
        pass
    else:
        no_city()
    s_end = list(city)
    while not game_over:
        if step == 'AI':
            city = ''
            for city_next in cityes:
                if city_next[0].lower() == s_end[-1]:
                    city = city_next
            if city == '':
                bot.send_message(
                    message.chat.id, f'Не могу найти город на букву {s_end[-1]}. Вы победили')
                game_over = True
            else:
                bot.send_message(message.chat.id,
                                 city)
                step = 'humun'
        else:
            correct = False
            while not correct:
                if city == '/stop':
                    game_over = True
                    correct = True
                else:
                    if city[0].lower() != s_end[-1]:
                        correct = False
                        bot.send_message(
                            message.chat.id, f'Не верный город,назоваите город на букву {s_end[-1]}')
                    if city in set(cityes_all):
                        pass
                    else:
                        correct = False
                        bot.send_message(message.chat.id,
                                         'Такого города не существует')
                    if city in set(cityes_old):
                        correct = False
                        bot.send_message(
                            message.chat.id, 'Не верно. Такой город уже называли')
                step = 'AI'


def no_city(message):
    bot.send_message(message.chat.id, 'Такого города не существует')
    bot.register_next_step_handler(message, city_game)


bot.polling(none_stop=True)
