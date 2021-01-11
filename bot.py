import config
import markups
import sql_queries
import telebot
import threading
import time

bot = telebot.TeleBot(config.token)
user_city = {}
user_data = {}
user_orient = {}
cur_subs = {}


def like_update(value):
    new_value = '%' + str(value) + '%'
    return new_value


def form_answer_dep(dep_flights, user):
    for item in dep_flights:
        answer_text = u"\U0001F6EB" + '\n%s %s\n%s\nВылет %s\n%s\nНачало регистрации %s\nНачало посадки %s\n%s' \
                      % (item['ru_flight_number'], item['ru_airline'], item['ru_airport'], item['plan'],
                         item['ru_aircraft'], item['checkin_dt_plan_begin'], item['gate_dt_plan_begin'],
                         item['status'])
        if item['status'] == 'РЕГИСТРАЦИЯ':
            answer_text = u"\U0001F6EB" + '\n%s %s\n%s\nВылет %s\n%s\n%s до %s\nСтойки регистрации %s' % \
                          (item['ru_flight_number'], item['ru_airline'], item['ru_airport'], item['plan'],
                           item['ru_aircraft'], item['status'], item['checkin_dt_plan_end'],
                           item['numbers_reg'])
        bot.send_message(user, text=answer_text, reply_markup=markups.subscribe(item['flight_id']))


def form_answer_arr(arr_flights, user):
    for item in arr_flights:
        answer_text = u"\U0001F6EC" + '\n%s %s\n%s\nПрилет %s\n%s\n%s' % (item['ru_flight_number'],
                                                                          item['ru_airline'],
                                                                          item['ru_airport'],
                                                                          item['plan'],
                                                                          item['ru_aircraft'],
                                                                          item['status'])
        bot.send_message(user, text=answer_text, reply_markup=markups.subscribe(item['flight_id']))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, text=u'\u2139\ufe0f' + 'Основное меню', reply_markup=markups.main_menu())


@bot.message_handler(content_types=["text"])
def wait_flight(message):
    if message.text.isdigit() and len(message.text) >= 2:
        dep_flights = sql_queries.dep_flight_number(message.text)
        arr_flights = sql_queries.arr_flight_number(message.text)
        if dep_flights:
            form_answer_dep(dep_flights, message.chat.id)
        if arr_flights:
            form_answer_arr(arr_flights, message.chat.id)
        if not dep_flights and not arr_flights:
            bot.send_message(message.chat.id, text=config.error, reply_markup=markups.search_error())
    elif message.text.isalpha() and len(message.text) >= 3:
        dep_flights = sql_queries.dep_city(message.text)
        arr_flights = sql_queries.arr_city(message.text)
        user_city[message.chat.id] = message.text
        if dep_flights or arr_flights:
            bot.send_message(message.from_user.id, text='.' + message.text + '.', reply_markup=markups.search_city())
        else:
            bot.send_message(message.chat.id, text=config.error, reply_markup=markups.search_error())
    else:
        bot.send_message(message.chat.id, text=config.error, reply_markup=markups.search_error())


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = call.message.chat.id
    text = call.message.text
    process_answer(user, text, call.data)


def process_answer(user, text, data):
    if data == 'flights':
        bot.send_message(user, config.main_menu)
    if data == 'main':
        bot.send_message(user, text='Основное меню', reply_markup=markups.main_menu())
    if data == 'today':
        user_data[user] = 'today'
        bot.send_message(user, text='.' + text + '.' + ' Сегодня', reply_markup=markups.arr_dep())
    if data == 'tomorrow':
        user_data[user] = 'tomorrow'
        bot.send_message(user, text='.' + text + '.' + ' Завтра', reply_markup=markups.arr_dep())
    if data == 'arrival':
        user_orient[user] = 'arrival'
        end_answer(user)
    if data == 'departure':
        user_orient[user] = 'departure'
        end_answer(user)
    if data.find('subscribe') != -1:
        flight_id = data.replace('subscribe ', '')
        is_subscribe = sql_queries.check_subscribe(user, flight_id)
        if not is_subscribe:
            sql_queries.add_subscribe(user, flight_id)
            bot.send_message(user, text='Успешная подписка', reply_markup=markups.suc_subscribe())
        else:
            bot.send_message(user, text='Вы уже подписаны на этот рейс', reply_markup=markups.suc_subscribe())
    if data == 'del_sub':
        sql_queries.del_sub(user)
        bot.send_message(user, text='Подписки удалены', reply_markup=markups.main_menu())


def end_answer(user):
    if user_data[user] == 'today':
        if user_orient[user] == 'arrival':
            arr_flights = sql_queries.arr_city_today(user_city[user])
            if arr_flights:
                form_answer_arr(arr_flights, user)
        elif user_orient[user] == 'departure':
            dep_flights = sql_queries.dep_city_today(user_city[user])
            if dep_flights:
                form_answer_dep(dep_flights, user)
    elif user_data[user] == 'tomorrow':
        if user_orient[user] == 'arrival':
            arr_flights = sql_queries.arr_city_tomorrow(user_city[user])
            if arr_flights:
                form_answer_arr(arr_flights, user)
        elif user_orient[user] == 'departure':
            dep_flights = sql_queries.dep_city_tomorrow(user_city[user])
            if dep_flights:
                form_answer_dep(dep_flights, user)


def form_status():
    while True:
        global cur_subs
        status = sql_queries.get_status()
        print(status)
        for elem in status['departure']:
            for sub in cur_subs['departure']:
                if elem['flight'] == sub['flight'] and elem['status'] != sub['status']:
                    print('измена')
                    flight = sql_queries.get_by_flight_id('departure', elem['flight'])
                    print(flight)
                    users = sql_queries.get_users(elem['flight'])
                    if flight and users:
                        answer_text = u"\U0001F6EB" + '\n%s %s\n%s\nВылет %s\n%s\nНачало регистрации %s\nНачало посадки %s\n%s' \
                                      % (flight['ru_flight_number'], flight['ru_airline'], flight['ru_airport'],
                                         flight['plan'],
                                         flight['ru_aircraft'], flight['checkin_dt_plan_begin'],
                                         flight['gate_dt_plan_begin'],
                                         flight['status'])
                        if flight['status'] == 'РЕГИСТРАЦИЯ':
                            answer_text = u"\U0001F6EB" + '\n%s %s\n%s\nВылет %s\n%s\n%s до %s\nСтойки регистрации %s' % \
                                          (flight['ru_flight_number'], flight['ru_airline'], flight['ru_airport'],
                                           flight['plan'],
                                           flight['ru_aircraft'], flight['status'], flight['checkin_dt_plan_end'],
                                           flight['numbers_reg'])
                        for user in users:
                            bot.send_message(user['user'], text=answer_text)
        for elem in status['arrival']:
            for item in cur_subs['arrival']:
                if elem['flight'] == item['flight'] and elem['status'] != item['status']:
                    print('измена')
                    flights = sql_queries.get_by_flight_id('arrival', elem['flight'])
                    users = sql_queries.get_users(elem['flight'])
                    print(flights)
                    print(users)
                    if flights and users:
                        for user in users:
                            print(user['user'])
                            bot.send_message(user['user'], text='ололоша')
        cur_subs = status
        time.sleep(10.0)


def delete_sub():
    sql_queries.del_all_subs()
    time.sleep(86400.0)


result = sql_queries.get_status()
if result:
    cur_subs = result
pam_status = threading.Thread(target=form_status)
del_subs = threading.Thread(target=delete_sub)
pam_status.start()
del_subs.start()


if __name__ == '__main__':
     bot.infinity_polling()
