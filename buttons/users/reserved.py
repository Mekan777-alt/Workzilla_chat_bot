from datetime import date, timedelta

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def people():
    markup = ReplyKeyboardMarkup()
    for i in range(1, 11):
        i = str(i)
        markup.add(i)
    return markup


def date_day():
    markup = ReplyKeyboardMarkup()
    first_date = date.today() + timedelta(days=0)
    duration = timedelta(days=14)
    for d in range(duration.days + 1):
        day = first_date + timedelta(days=d)
        day_in = day.strftime("%d-%m-%y")
        markup.add(day_in)
    return markup


def phone_number():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📞 Отправить свой номер", request_contact=True))
    return markup


def time():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("10:00")
    markup.add("10:30")
    markup.add("11:00")
    markup.add("11:30")
    markup.add("12:00")
    markup.add("12:30")
    markup.add("13:00")
    markup.add("13:30")
    markup.add("14:00")
    markup.add("14:30")
    markup.add("15:00")
    markup.add("15:30")
    markup.add("16:00")
    markup.add("16:30")
    markup.add("17:00")
    markup.add("17:30")
    markup.add("18:00")
    markup.add("18:30")
    markup.add("19:00")
    markup.add("19:30")
    markup.add("20:00")
    markup.add("20:30")
    markup.add("21:00")
    markup.add("21:30")
    markup.add("22:00")
    return markup


def cancel_reserved():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("❌ Отменить")
    return markup


def done_or_cancel():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ Верно")
    markup.add("❌ Нет")
    return markup
