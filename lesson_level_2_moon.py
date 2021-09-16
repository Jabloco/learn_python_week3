import logging
import re
import ephem
import settings
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(update, context):
    user_text = update.message.text
    user_text_list = user_text.split()

    if user_text_list[0] == '/planet':
        length_user_text = len(user_text_list)
        if length_user_text == 2:
            update.message.reply_text(planet(user_text_list[1].capitalize()))
        elif length_user_text > 2:
            update.message.reply_text('Много лишних слов')
        elif length_user_text == 1:
            update.message.reply_text('Не указана планета')

    elif user_text_list[0] == '/next_full_moon':
        length_user_text = len(user_text_list)
        if length_user_text == 2:            
            update.message.reply_text(fool_moon(user_text_list[1]))
        elif length_user_text > 2:
            update.message.reply_text('Много лишних слов')
        elif length_user_text == 1:
            update.message.reply_text('Не указана дата')

    elif user_text_list[0] == '/wordcount':
        length_user_text = len(user_text_list)
        if length_user_text == 1:
            update.message.reply_text('Введите слова')
        else:
            update.message.reply_text(word_count(user_text_list[1:]))

    elif user_text_list[0] == '/cities':
        length_user_text = len(user_text_list)

        if length_user_text == 1:
            if len(cities_stack) == 0:
                update.message.reply_text('Игра не начата')
            else:
                update.message.reply_text('\n'.join(cities_stack))
        elif length_user_text > 2:
            update.message.reply_text('Много лишних слов')
        else:
            update.message.reply_text(game_city(user_text_list[1]))
    
    elif user_text_list[0] == '/calc':
        length_user_text = len(user_text_list)

        if length_user_text == 1:
            update.message.reply_text('Добавьте выражение')
        else:
            arifm = ''.join(user_text_list[1:])
            update.message.reply_text(calc(arifm))

    else:
        print(user_text)
        update.message.reply_text(user_text)

# Задание третьего уровня
# КАЛЬКУЛЯТОР
def calc(input_arifm:str):
    # убрать пробелы
    input_arifm.replace(' ', '')
    # проверить строку на буквы
    if re.match("^[0-9*()\-\+.]*$", input_arifm):
        try:
            result = eval(input_arifm)
        # проймать деление на 0
        except ZeroDivisionError:
            return 'На ноль делить нельзя'
        # поймать SintaxError
        except (SyntaxError, NameError):
            return 'Введите арифметическое выражение, например 4+5'
        return result
    else:
        return 'Введите арифметическое выражение, например 4+5'

# Задание третьего уровня
# ИГРА В ГРОДА
cities = ['Москва', 'Киров', 'Архангельск', 'Владивосток', 'Казань', 'Нолинск']  # список городов известных боту
cities_stack = []  # список использованых городов 
def game_city(input_city: str):
    input_city = input_city.capitalize()
    length_city = len(cities)
    length_city_stack = len(cities_stack)
    # если список городов и стек равны тоначинаем игру заново
    # очищаем стек и записываем в него пришедший город
    if length_city == length_city_stack:
        cities_stack.clear()
        cities_stack.append(input_city)
        return 'У бота не осталось городов.\nИгра сброшена\nВведеный город принят в качестве стартового'

    # проверяем есть ли введены город в списке использованых
    if input_city in cities_stack:
        return 'Город уже был назван'

    # проверяем известен ли город боту
    if input_city not in cities:
        return 'Я не знаю такого города'

    # если город не использовался и известен боту
    if input_city in cities:
        # проверяем что стек пустой
        if length_city_stack == 0:
            cities_stack.append(input_city)
            return 'Город принят'

        # проверка последней буквы
        # если заканчивается на ы или ь
        if cities_stack[-1][-1] in ('ыь') and input_city[0].lower() == cities_stack[-1][-2]:
            cities_stack.append(input_city)
            return 'Город принят'
        # если заканчивается на другие буквы
        if input_city[0].lower() == cities_stack[-1][-1]:
            cities_stack.append(input_city)
            return 'Город принят'
        # если город не прошел ни одной проверки
        return 'Город не принят'

# Задание второго уровня
# СЧЕТЧИК СЛОВ
def word_count(input_words:list):
    words_count = 0
    for elem in input_words:
        if not re.match("^[0-9_?!@#№$%^&\"\'<>*()\-\+=~\|\\\/,.]*$", elem):
            words_count += 1
    return words_count

# Задание второго уровня
# ДАТА ПОЛНОЛУНИЯ
def fool_moon(input_date):
    try:
        near_date = datetime.strptime(input_date, '%Y-%m-%d')
    except TypeError:
        return 'Не верный формат даты'
    except ValueError:
        return 'Не верный формат даты'
    return ephem.next_full_moon(near_date)

def planet(input_planet):
    try:
        sky_body = getattr(ephem, input_planet)
    except AttributeError:
        return 'Я не знаю такой планеты'
    return ephem.constellation(sky_body(datetime.date.today()))[1]
    

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()