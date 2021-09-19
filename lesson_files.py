# Прочитайте содержимое файла в переменную, подсчитайте длину получившейся строки
# Подсчитайте количество слов в тексте
# Замените точки в тексте на восклицательные знаки
# Сохраните результат в файл referat2.txt


def file_worker():
    with open('referat.txt', 'r', encoding='utf8') as file:
        text_from_file = file.read()
        
    len_text = len(text_from_file)
    count_words = len(text_from_file.split())
    text_to_file = text_from_file.replace('.', '!')

    with open('referat2.txt', 'w', encoding='utf8') as file:
        file.write(text_to_file)

    return len_text, count_words
print(file_worker())