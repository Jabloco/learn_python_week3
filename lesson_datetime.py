from datetime import date, timedelta, datetime

# Напечатайте в консоль даты: вчера, сегодня, 30 дней назад
def today_yesterday():
    today = date.today()
    yesterday = date.today() - timedelta(days = 1)
    days_ago = date.today() - timedelta(days = 30)
    return f'Вчера {today}, сегодня {yesterday}, 30 дней назад {days_ago}'
    

# Превратите строку "01/01/25 12:10:03.234567" в объект datetime
def string_to_date(input_date):
    dt_format = datetime.strptime(input_date, "%d/%m/%y %H:%M:%S.%f")
    return dt_format


if __name__ == "__main__":
    date_time = "01/01/25 12:10:03.234567"
    print(today_yesterday())
    print(string_to_date(date_time))
