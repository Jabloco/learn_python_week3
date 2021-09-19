from datetime import date, timedelta, datetime

# Напечатайте в консоль даты: вчера, сегодня, 30 дней назад
today = date.today()
yesterday = date.today() - timedelta(days=1)
days_ago = date.today() - timedelta(days=30)
print(f'Вчера {today}, сегодня {yesterday}, 30 дней назад {days_ago}')
    

# Превратите строку "01/01/25 12:10:03.234567" в объект datetime
date_time = "01/01/25 12:10:03.234567"
dt_format = datetime.strptime(date_time, "%d/%m/%y %H:%M:%S.%f")
print(dt_format)

