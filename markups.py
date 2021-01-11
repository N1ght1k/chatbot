from telebot import types


def main_menu():
    keyboard = types.InlineKeyboardMarkup()
    key_flights = types.InlineKeyboardButton(text=u'\u2708\uFE0F' + 'Рейсы: поиск и уведомления',
                                             callback_data='flights')
    keyboard.add(key_flights)
    return keyboard


def search_error():
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text=u'\u2139\ufe0f' + 'Основное меню', callback_data='main')
    keyboard.add(key_menu)
    return keyboard


def search_city():
    keyboard = types.InlineKeyboardMarkup()
    key_today = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
    key_tomorrow = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
    keyboard.add(key_today, key_tomorrow)
    return keyboard


def arr_dep():
    keyboard = types.InlineKeyboardMarkup()
    key_arrival = types.InlineKeyboardButton(text='Прилет в Анапу', callback_data='arrival')
    key_departure = types.InlineKeyboardButton(text='Вылет из Анапы', callback_data='departure')
    keyboard.add(key_arrival, key_departure)
    return keyboard


def subscribe(flight):
    keyboard = types.InlineKeyboardMarkup()
    key_subscribe = types.InlineKeyboardButton(text=u"\U0001F4E9" + 'Подписка на изменение статуса',
                                               callback_data='subscribe ' + flight)
    keyboard.add(key_subscribe)
    return keyboard


def suc_subscribe():
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text=u'\u2139\ufe0f' + 'Основное меню', callback_data='main')
    key_del_sub = types.InlineKeyboardButton(text=u'\u2139\ufe0f' + 'Удалить подписки', callback_data='del_sub')
    keyboard.add(key_menu, key_del_sub)
    return keyboard
