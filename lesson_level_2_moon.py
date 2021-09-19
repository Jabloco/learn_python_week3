import logging
import re
import ephem
import settings
# from datetime import datetime
# import datetime
from datetime import date, datetime

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
    update.message.reply_text(user_text)
        
    
    # 

    

    # elif user_text_list[0] == '/cities':
    #     length_user_text = len(user_text_list)

    #     if length_user_text == 1:
    #         if len(cities_stack) == 0:
    #             update.message.reply_text('Игра не начата')
    #         else:
    #             update.message.reply_text('\n'.join(cities_stack))
    #     elif length_user_text > 2:
    #         update.message.reply_text('Много лишних слов')
    #     else:
    #         update.message.reply_text(game_city(user_text_list[1]))
    
    # elif user_text_list[0] == '/calc':
    #     length_user_text = len(user_text_list)

    #     if length_user_text == 1:
    #         update.message.reply_text('Добавьте выражение')
    #     else:
    #         arifm = ''.join(user_text_list[1:])
    #         update.message.reply_text(calc(arifm))

       

# Задание третьего уровня
# КАЛЬКУЛЯТОР
def calc(update, context):
    length_context = len(context.args)
    if length_context == 0:
        update.message.reply_text('Добавьте выражение')
    else:
        arifm = ''.join(context.args)
    # убрать пробелы
    # input_arifm.replace(' ', '')
    # проверить строку на буквы
        if re.match("^[0-9*()\-\+.\s]*$", arifm):
            try:
                result = eval(arifm)
            # проймать деление на 0
            except ZeroDivisionError:
                update.message.reply_text('На ноль делить нельзя')
                return
            # поймать SintaxError
            except (SyntaxError, NameError):
                update.message.reply_text('Введите арифметическое выражение, например 4+5')
                return
            update.message.reply_text(result)
        else:
            update.message.reply_text('Введите арифметическое выражение, например 4+5')

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
def word_count(update, context):
    length_context = len(context.args)
    if length_context == 0:
        update.message.reply_text('Введите слова')
    else:
        words_count = 0
        for elem in context.args:
            if not re.match("^[0-9_?!@#№$%^&\"\'<>*()\-\+=~\|\\\/,.]*$", elem):
                words_count += 1
        update.message.reply_text(words_count)

# Задание второго уровня
# ДАТА ПОЛНОЛУНИЯ
def full_moon(update, context):
    length_context = len(context.args)
    if length_context == 0:
        update.message.reply_text('Не указана дата')
    elif length_context > 1:
        update.message.reply_text('Много лишних слов')
    else:         
        try:
            near_date = datetime.strptime(context.args[0], '%Y-%m-%d')
        except TypeError:
            update.message.reply_text('Не верный формат даты')
        except ValueError:
            update.message.reply_text('Не верный формат даты')
        update.message.reply_text(ephem.next_full_moon(near_date))

def planet(update, context):
    length_context = len(context.args)
    if  length_context > 1:
            update.message.reply_text('Много лишних слов')
    elif length_context == 0:
            update.message.reply_text('Не указана планета')
    else:
        sky_body_name = context.args[0]
        try:
            sky_body = getattr(ephem, sky_body_name)
        except AttributeError:
            update.message.reply_text('Я не знаю такой планеты')
        update.message.reply_text(ephem.constellation(sky_body(date.today()))[1])
    

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(CommandHandler("fullmoon", full_moon))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(CommandHandler("calc", calc))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()