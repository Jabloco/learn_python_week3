import logging
import re
import ephem
import settings
from datetime import datetime
import ephem

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
    else:
        print(user_text)
        update.message.reply_text(user_text)

def word_count(input_words):
    words_count = 0
    for elem in input_words:
        if not re.match("^[0-9_?!@#$%^&\"\'<>*()\-\+=~|\\/]*$", elem):
            words_count += 1
    return words_count


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